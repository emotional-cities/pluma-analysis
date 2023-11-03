import numpy as np

from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.io.glia import load_glia
from pluma.sync import ClockRefId


class GliaStream(Stream):
    def __init__(self,
                 filename: str,
                 dtypes: list[list[chr]],  # list of list of char formats within each frame after topic
                 channel_names: list[list[str]],  # list of list of string channel names within each frame after topic
                 data: np.array = np.empty(shape=(0, 1)),
                 si_conversion: SiUnitConversion = SiUnitConversion(),
                 clockreferenceid: ClockRefId = ClockRefId.HARP,
                 **kw):
        super(GliaStream, self).__init__(data=data, **kw)
        self.streamtype = 'Glia'  # TODO this should be a defined stream type in pluma analysis
        self.filename = filename
        self.dtypes = dtypes
        self.channel_names = channel_names
        self.si_conversion = si_conversion
        self.clockreference.referenceid = clockreferenceid

        assert(len(self.dtypes) == len(self.channel_names)), "Number of data types does not match number of channel names."

        if self.autoload:
            self.load()

    def load(self):
        self.data = load_glia(self.filename, self.dtypes, self.channel_names, root=self.rootfolder)

    def resample(self):
        pass

    def convert_to_si(self, data=None):
        pass

    def export_to_csv(self):
        pass