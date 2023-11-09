import numpy as np

from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.io.glia import load_glia
from pluma.sync import ClockRefId


class GliaStream(Stream):
    def __init__(self,
                 filename: str,
                 dtypes: list[list[tuple[str, type]]],
                 data: np.array = np.empty(shape=(0, 1)),
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

    def export_to_csv(self):
        pass
