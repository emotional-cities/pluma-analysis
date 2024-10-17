import pandas as pd
import datetime

from pluma.stream import Stream, StreamType
from pluma.io.empatica import load_empatica
from pluma.sync import ClockRefId
from pluma.export.streams import shift_stream_index, resample_stream_empatica


class EmpaticaStream(Stream):
    """_summary_

    Args:
            Stream (_type_): _description_
    """

    def __init__(
        self,
        clockreferenceid: ClockRefId = ClockRefId.HARP,
        align_timestamps: bool = True,
        **kw,
    ):
        super(EmpaticaStream, self).__init__(**kw)
        self.streamtype = StreamType.EMPATICA
        self.clockreference.referenceid = clockreferenceid
        self.align_timestamps = align_timestamps

        if self.autoload:
            self.load()

    def load(self):
        self.data = load_empatica(root=self.rootfolder, align_timestamps=self.align_timestamps)

    def __str__(self):
        return f"Empatica stream from device {self.device}, stream {self.streamlabel}"

    def resample(self, sampling_dt: datetime.timedelta) -> pd.DataFrame:
        return resample_stream_empatica(self, sampling_dt)

    def add_clock_offset(self, offset):
        for stream in self.data.values():
            shift_stream_index(stream, offset)
