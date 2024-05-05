import numpy as np
import pandas as pd

from pluma.stream import StreamType
from pluma.stream import Stream
from pluma.io.zeromq import load_zeromq
from pluma.export.streams import offset_stream_index


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

    def offset_clock(self, offset):
        offset_stream_index(self.data, offset)


class GliaStream(Stream):
    def __init__(self, **kw):
        super(GliaStream, self).__init__(**kw)

        self.streamtype = StreamType.GLIA
        if self.autoload:
            self.load()

    def resample(self):
        pass

    def convert_to_si(self, data=None):
        pass

    def export_to_csv(self, export_path):
        self.data.to_csv(export_path)

    def offset_clock(self, offset):
        offset_stream_index(self.data, offset)


class UnityStream(Stream):
    def __init__(self, **kw):
        super(UnityStream, self).__init__(**kw)

        self.streamtype = StreamType.UNITY
        if self.autoload:
            self.load()

    def resample(self):
        pass

    def convert_to_si(self, data=None):
        pass

    def export_to_csv(self, export_path):
        self.data.to_csv(export_path)

    def offset_clock(self, offset):
        offset_stream_index(self.data, offset)


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


class GliaEyeTrackingStream(GliaStream):
    def __init__(self, **kw):
        super(GliaEyeTrackingStream, self).__init__(**kw)

    def load(self):
        self.data = load_zeromq(
            ['Glia/EyeTracking_Frame1.bin', 'Glia/EyeTracking_Frame2.bin'],
            [[('HardwareTime', np.ulonglong), ('OmniceptTime', np.ulonglong), ('SystemTime', np.ulonglong)], 
             [('CombinedGaze.X', np.single), ('CombinedGaze.Y', np.single), ('CombinedGaze.Z', np.single), ('LeftOpenness', np.single), ('LeftOpennessConfidence', np.single), ('LeftDilation', np.single), ('LeftDilationConfidence', np.single), ('LeftPosition.X', np.single), ('LeftPosition.Y', np.single), ('RightOpenness', np.single), ('RightOpennessConfidence', np.single), ('RightDilation', np.single), ('RightDilationConfidence', np.single), ('RightPosition.X', np.single), ('RightPosition.Y', np.single)]],
            root=self.rootfolder
        )


class GliaHeartRateStream(GliaStream):
    def __init__(self, **kw):
        super(GliaEyeTrackingStream, self).__init__(**kw)

    def load(self):
        self.data = load_zeromq(
            ['Glia/HeartRate_Frame1.bin', 'Glia/HeartRate_Frame2.bin'],
            [[('HardwareTime', np.ulonglong), ('OmniceptTime', np.ulonglong), ('SystemTime', np.ulonglong)], 
             [('HardwareTime', np.uintc)]],
            root=self.rootfolder
        )


class GliaImuStream(GliaStream):
    def __init__(self, **kw):
        super(GliaImuStream, self).__init__(**kw)

    def load(self):
        self.data = load_zeromq(
            ['Glia/IMU_Frame1.bin', 'Glia/IMU_Frame2.bin'],
            [[('HardwareTime', np.ulonglong), ('OmniceptTime', np.ulonglong), ('SystemTime', np.ulonglong)], 
             [('AccelX', np.single), ('AccelY', np.single), ('AccelZ', np.single), ('GyroX', np.single), ('GyroY', np.single), ('GyroZ', np.single)]],
            root=self.rootfolder
        )


class UnityTransformStream(UnityStream):
    def __init__(self, **kw):
        super(UnityTransformStream, self).__init__(**kw)

    def load(self):
        self.data = load_zeromq(
            ['VRTransform/Position_Frame1.bin', 'VRTransform/Position_Frame2.bin'],
            [[('Timestamp', np.ulonglong)], 
             [('Transform.Position.X', np.single), ('Transform.Position.Y', np.single), ('Transform.Position.Z', np.single), ('Transform.Forward.X', np.single), ('Transform.Forward.Y', np.single), ('Transform.Forward.Z', np.single)]],
            root=self.rootfolder
        )


class UnityPointToOriginWorldStream(UnityStream):
    def __init__(self, **kw):
        super(UnityPointToOriginWorldStream, self).__init__(**kw)

    def load(self):
        self.data = load_zeromq(
            ['Unity_PointToOriginWorld/PointToOriginWorld_Frame1.bin', 'Unity_PointToOriginWorld/PointToOriginWorld_Frame2.bin'],
            [[('Timestamp', np.ulonglong)], 
             [('Origin.Position.X', np.single), ('Origin.Position.Y', np.single), ('Origin.Position.Z', np.single), ('Hand.Position.X', np.single), ('Hand.Position.Y', np.single), ('Hand.Position.Z', np.single), ('HandAxis.Angle.X', np.single), ('HandAxis.Angle.Y', np.single), ('HandAxis.Angle.Z', np.single), ('OriginAxis.Angle.X', np.single), ('Transform.Angle.Y', np.single), ('Transform.Angle.Z', np.single)]],
            root=self.rootfolder
        )


class UnityPointToOriginMapStream(UnityStream):
    def __init__(self, **kw):
        super(UnityPointToOriginMapStream, self).__init__(**kw)

    def load(self):
        self.data = load_zeromq(
            ['Unity_PointToOriginMap/PointToOriginMap_Frame1.bin', 'Unity_PointToOriginMap/PointToOriginMap_Frame2.bin'],
            [[('Timestamp', np.ulonglong)], 
             [('Origin.Position.X', np.single), ('Origin.Position.Y', np.single), ('Subject.Position.X', np.single), ('Subject.Position.Y', np.single), ('Point.Position.X', np.single), ('Point.Position.Y', np.single)]],
            root=self.rootfolder
        )