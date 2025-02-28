import numpy as np
import pandas as pd

from pluma.stream import StreamType
from pluma.stream.harp import HarpStream
from pluma.io.zeromq import load_zeromq
from pluma.export.streams import shift_stream_index


class ZmqStream(HarpStream):
    def __init__(
        self,
        eventcode: int,
        streamtype: StreamType,
        filenames: list[str],
        dtypes: list[tuple[str, type]],
        clocksource: str | None = None,
        clockunit: str | None = None,
        **kw,
    ):
        self.filenames = filenames
        self.dtypes = dtypes
        super(ZmqStream, self).__init__(eventcode, **kw)
        self.streamtype = streamtype
        self.clocksource = clocksource
        self.clockunit = clockunit

    def resample(self):
        pass

    def convert_to_si(self, data=None):
        pass

    def load(self):
        super(ZmqStream, self).load()
        self.data = pd.DataFrame(np.arange(len(self.data)), index=self.data.index, columns=["Counter"])
        zmq_data = load_zeromq(self.filenames, self.dtypes, root=self.rootfolder)
        self.data = self.data.join(zmq_data, on="Counter")
        if self.clocksource is not None:
            index_name = self.data.index.name
            counter_timedelta = pd.to_timedelta(self.data[self.clocksource] - self.data[self.clocksource][0], self.clockunit)
            self.data.index = self.data.index[0] + counter_timedelta
            self.data.index.name = index_name

    def export_to_csv(self, export_path):
        self.data.to_csv(export_path)

    def add_clock_offset(self, offset):
        shift_stream_index(self.data, offset)
