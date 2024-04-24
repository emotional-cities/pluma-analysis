import numpy as np
import pandas as pd

from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.io.pupil import load_pupil
from pluma.sync import ClockRefId


class PupilStream(Stream):
    def __init__(self,
                 filename: str,
                 data: pd.DataFrame = None,
                 si_conversion: SiUnitConversion = SiUnitConversion(),
                 clockreferenceid: ClockRefId = ClockRefId.HARP,
                 frame0: list[tuple[str, type]] = [('SensorId', np.string_, 36)],
                 frame1: list[tuple[str, type]] = [('Timestamp', np.uint64)],
                 frame2: list[tuple[str, type]] = [('GazeX', np.single), ('GazeY', np.single)],
                 **kw):
        super(PupilStream, self).__init__(data=data, **kw)
        self.streamtype = StreamType.PUPIL
        self.filename = filename
        self.si_conversion = si_conversion
        self.clockreference.referenceid = clockreferenceid
        self.frame0 = frame0
        self.frame1 = frame1
        self.frame2 = frame2

        if self.autoload:
            self.load()

    def load(self):
        self.data = load_pupil(self.filename, frame0=self.frame0, frame1=self.frame1, frame2=self.frame2, root=self.rootfolder)
    def resample(self):
        pass

    def convert_to_si(self, data=None):
        pass

    def export_to_csv(self, export_path):
        self.data.to_csv(export_path)

    
