import numpy as np
import pandas as pd

from pluma.stream import StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.sync import ClockRefId
from pluma.stream import Stream
from pluma.io.zeromq import load_zeromq


class PupilStream(Stream):
    def __init__(self, **kw):
        super(PupilStream, self).__init__(**kw)

        self.streamtype = StreamType.PUPIL
        if self.autoload:
            self.load()

    def resample(self):
        pass

    def convert_to_si(self, data=None):
        pass

    def export_to_csv(self, export_path):
        self.data.to_csv(export_path)


class PupilGazeStream(PupilStream):
    def __init__(self, **kw):
        super(PupilGazeStream, self).__init__(**kw)

    def load(self):
        self.data = load_zeromq(
            ['PupilLabs/Gaze_Frame0.bin', 'PupilLabs/Gaze_Frame1.bin', 'PupilLabs/Gaze_Frame2.bin'],
            [[('SensorId', np.string_, 36)], [('Timestamp', np.uint64)], [('GazeX', np.single), ('GazeY', np.single)]],
            root=self.rootfolder
        )


class PupilWorldCameraStream(PupilStream):
    def __init__(self, **kw):
        super(PupilWorldCameraStream, self).__init__(**kw)

    def load(self):
        self.data = load_zeromq(
            ['PupilLabs/WorldCamera_Frame0.bin', 'PupilLabs/WorldCamera_Frame1.bin', 'PupilLabs/WorldCamera_Frame2.bin'],
            [[('SensorId', np.string_, 36)], [('Format', np.uint32), ('Width', np.uint32), ('Height', np.uint32), ('Sequence', np.uint32), ('Timestamp', np.uint64), ('DataBytes', np.uint32), ('Reserved', np.uint32)], None],
            root=self.rootfolder
        )