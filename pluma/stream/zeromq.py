import numpy as np
import pandas as pd

from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.io.zeromq import load_zeromq
from pluma.sync import ClockRefId


class ZmqStream(Stream):
    def __init__(self, 
                 dtypes: list[list[tuple[str, type]]],
                 data: pd.DataFrame = None, 
                 si_conversion: SiUnitConversion = SiUnitConversion(),
                 clockreferenceid: ClockRefId = ClockRefId.HARP,
                 **kw):
        super(ZmqStream, self).__init__(data=data, **kw)

        self.streamtype = StreamType.ZMQ
        self.dtypes = dtypes
        self.si_conversion = si_conversion
        self.clockreference.referenceid = clockreferenceid

        if self.autoload:
            self.load()

    def load(self):
        self.data = load_zeromq([self.device + '_Frame0.bin'], self.dtypes, root=self.rootfolder)

    def resample(self):
        pass

    def convert_to_si(self, data=None):
        pass

    def export_to_csv(self, export_path):
        self.data.to_csv(export_path)