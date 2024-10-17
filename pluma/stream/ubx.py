import pandas as pd

from dotmap import DotMap

from pluma.stream import Stream, StreamType
from pluma.stream.harp import HarpStream
from pluma.io.ubx import load_ubx_event_stream, _UBX_MSGIDS
from pluma.sync import ClockRefId


class UbxStream(Stream):
    def __init__(
        self,
        data: DotMap = DotMap(),
        autoload_messages: list = [],
        clockreferenceid: ClockRefId = ClockRefId.GNSS,
        **kw,
    ):
        super(UbxStream, self).__init__(data=data, **kw)
        self.positiondata = None
        self.streamtype = StreamType.UBX
        self.clockreference.referenceid = clockreferenceid
        self.clock_calib_model = None  # Store the model here

        self.autoload_messages = autoload_messages
        if self.autoload:
            self.load_event_list(self.autoload_messages)

    def load(self):
        self.load_event_list(self.autoload_messages)

    def load_event(self, event: _UBX_MSGIDS):
        self._update_dotmap(event, load_ubx_event_stream(event, root=self.rootfolder))

    def _update_dotmap(self, event: _UBX_MSGIDS, df: pd.DataFrame):
        self.data[event.value] = df

    def has_event(self, event: _UBX_MSGIDS):
        return self.data.has_key(event.value)

    def load_event_list(self, events: list):
        for event in events:
            self.load_event(event)

    def parseposition(
        self,
        event: _UBX_MSGIDS = _UBX_MSGIDS.NAV_HPPOSLLH,
        calibrate_clock: bool = True,
        decode_utc_time: bool = True,
    ):
        NavData = self.data[event.value].copy()
        NavData.insert(
            NavData.shape[1],
            "Latitude",
            NavData.apply(lambda x: x.Message.lat, axis=1),
            False,
        )
        NavData.insert(
            NavData.shape[1],
            "Longitude",
            NavData.apply(lambda x: x.Message.lon, axis=1),
            False,
        )
        NavData.insert(
            NavData.shape[1],
            "Elevation",
            NavData.apply(lambda x: x.Message.height, axis=1),
            False,
        )
        NavData.insert(
            NavData.shape[1],
            "Time_iTow",
            NavData.apply(lambda x: x.Message.iTOW, axis=1),
            False,
        )
        if calibrate_clock is True:
            iTow = NavData["Time_iTow"].values.reshape(-1, 1)
            iTowCorrected = self.calibrate_itow(iTow)
            iTowCorrected = pd.DataFrame(HarpStream.from_seconds(iTowCorrected))
            iTowCorrected.columns = ["Seconds"]
            NavData.set_index(iTowCorrected["Seconds"], inplace=True)
        if decode_utc_time is True:
            # GPS epoch
            epoch = pd.Timestamp(1980, 1, 6)
            reference = self.data["TIM_TM2"].Message[0]
            offset = epoch + pd.Timedelta(weeks=reference.wnR)
            NavData["Time_UTC"] = offset + NavData["Time_iTow"].astype("timedelta64[ms]")
        self.positiondata = NavData
        return NavData

    def calibrate_itow(self, input_itow_array):
        return self.clockreference.conversion_model(input_itow_array)

    def __str__(self):
        return f"Ubx stream from device {self.device}, stream {self.streamlabel}"
