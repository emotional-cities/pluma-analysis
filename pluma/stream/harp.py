import pandas as pd
import datetime

from pluma.stream import Stream, StreamType
from pluma.io.harp import load_harp_stream

from pluma.stream.siconversion import SiUnitConversion

from pluma.sync import ClockRefId

from pluma.export.streams import (
    export_stream_to_csv,
    resample_stream_harp,
    shift_stream_index,
)


class HarpStream(Stream):
    """_summary_

    Args:
            Stream (_type_): _description_
    """

    def __init__(
        self,
        eventcode: int,
        data: pd.DataFrame = pd.DataFrame(columns=["Timestamp", "Value"]),
        si_conversion: SiUnitConversion = SiUnitConversion(),
        clockreferenceid: ClockRefId = ClockRefId.HARP,
        **kw,
    ):
        super(HarpStream, self).__init__(data=data, **kw)
        self.eventcode = eventcode
        self.streamtype = StreamType.HARP
        self.si_conversion = si_conversion
        self.clockreference.referenceid = clockreferenceid

        if self.autoload:
            self.load()

        if self.si_conversion.attempt_conversion:
            self.convert_to_si()

    def convert_to_si(self, data=None):
        """Method to convert data to SI units"""
        if data is None:  # Default to the instance's data if None is provided
            self.data = self.si_conversion.convert_to_si(self.data)
            self.si_conversion.is_si = True
        else:  # if some other data source is provided
            return self.si_conversion.convert_to_si(data)

    def load(self):
        self.data = load_harp_stream(self.eventcode, root=self.rootfolder)
        self.si_conversion.is_si = False

    def __str__(self):
        return f"Harp stream from device \
		{self.device}, stream {self.streamlabel}({self.eventcode})"

    def export_to_csv(self, root_path, **kwargs):
        export_stream_to_csv(self, root_path, **kwargs)

    def resample(self, sampling_dt: datetime.timedelta) -> pd.DataFrame:
        return resample_stream_harp(self, sampling_dt)

    def add_clock_offset(self, offset):
        shift_stream_index(self.data, offset)
