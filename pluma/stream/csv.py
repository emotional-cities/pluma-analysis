import numpy as np
import os
import pandas as pd
import warnings
from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.sync import ClockRefId
from pluma.io.path_helper import ensure_complexpath
from pluma.export.streams import offset_stream_index


class CsvStream(Stream):
    def __init__(self,
                 filename: str,
                 data: pd.DataFrame = None,
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
        path = ensure_complexpath(self.rootfolder)
        path.join(self.filename)
        try:
            self.data = pd.read_csv(path.path)
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

    def export_to_csv(self, export_path):
        self.data.to_csv(export_path)

    def offset_clock(self, offset):
        offset_stream_index(self.data, offset)
