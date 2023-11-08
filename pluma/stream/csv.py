import numpy as np
import os
import pandas as pd
import warnings
from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.sync import ClockRefId
from pluma.io.path_helper import ensure_complexpath


class CsvStream(Stream):
    def __init__(self,
                 filename: str,
                 data: np.array = np.empty(shape=(0, 1)),
                 si_conversion: SiUnitConversion = SiUnitConversion(),
                 clockreferenceid: ClockRefId = ClockRefId.HARP,
                 **kw):
        super(CsvStream, self).__init__(data=data, **kw)
        self.streamtype = StreamType.CSV
        self.filename = filename
        self.si_conversion = si_conversion
        self.clockreference.referenceid = clockreferenceid

        if self.autoload:
            self.load()

    def load(self):
        path = ensure_complexpath(self.rootfolder)._path
        path = os.path.join(path, self.filename)
        try:
            self.data = pd.read_csv(path)
        except FileNotFoundError:
            warnings.warn(f'Glia stream file\
                        {path} could not be found.')
        except FileExistsError:
            warnings.warn(f'Glia stream file\
                        {path} could not be found.')

    def resample(self):
        pass

    def convert_to_si(self, data=None):
        pass

    def export_to_csv(self):
        pass
