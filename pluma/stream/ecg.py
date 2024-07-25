import datetime
import pandas as pd

from dotmap import DotMap

from pluma.export.streams import resample_stream_ecg, shift_stream_index
from pluma.io.harp import load_harp_stream
from pluma.preprocessing.ecg import heartrate_from_ecg
from pluma.stream.harp import HarpStream
from pluma.stream.siconversion import SiUnitConversion
from pluma.sync import ClockRefId


class EcgStream(HarpStream):
    def __init__(
            self,
            eventcode: int,
            clockreferenceid: ClockRefId = ClockRefId.HARP,
            **kw):
        super().__init__(
            eventcode,
            data=pd.DataFrame(columns=['Seconds', 'Value']),
            si_conversion=SiUnitConversion(),
            clockreferenceid=clockreferenceid,
            **kw)

    def load(self):
        ecg = load_harp_stream(self.eventcode, root=self.rootfolder)
        heartrate, _, _, _ = heartrate_from_ecg(ecg)
        self.data = DotMap({
            'Raw': ecg,
            'HeartRate': heartrate
        })
        self.si_conversion.is_si = False

    def __str__(self):
        return f'ECG stream from device {self.device}, stream {self.streamlabel}'
    
    def resample(self, sampling_dt: datetime.timedelta) -> pd.DataFrame:
        return resample_stream_ecg(self, sampling_dt)
    
    def add_clock_offset(self, offset):
        for stream in self.data.values():
            shift_stream_index(stream, offset)