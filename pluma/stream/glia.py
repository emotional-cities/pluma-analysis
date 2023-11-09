import numpy as np
import pandas as pd

from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.io.glia import load_glia
from pluma.sync import ClockRefId
from pluma.export.streams import export_stream_to_csv


class GliaStream(Stream):
    def __init__(self,
                 filename: str,
                 dtypes: list[list[tuple[str, type]]],
                 data: pd.DataFrame = None,
                 si_conversion: SiUnitConversion = SiUnitConversion(),
                 clockreferenceid: ClockRefId = ClockRefId.HARP,
                 **kw):
        super(GliaStream, self).__init__(data=data, **kw)
        self.streamtype = StreamType.GLIA
        self.filename = filename
        self.dtypes = dtypes
        self.si_conversion = si_conversion
        self.clockreference.referenceid = clockreferenceid

        if self.autoload:
            self.load()

    def load(self):
        self.data = load_glia(self.filename, self.dtypes, root=self.rootfolder)

    def resample(self):
        pass

    def convert_to_si(self, data=None):
        pass

    def export_to_csv(self, export_path):
        self.data.to_csv(export_path)
