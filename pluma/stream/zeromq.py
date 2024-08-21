import numpy as np
import pandas as pd

from pluma.stream import StreamType
from pluma.stream.harp import HarpStream
from pluma.io.zeromq import load_zeromq
from pluma.export.streams import shift_stream_index


class ZmqStream(HarpStream):
    def __init__(self,
                 eventcode: int,
                 streamtype: StreamType,
                 filenames: list[str],
                 dtypes: list[tuple[str, type]],
                 **kw):
        self.streamtype = streamtype
        self.filenames = filenames
        self.dtypes = dtypes
        super(ZmqStream, self).__init__(eventcode, **kw)

    def resample(self):
        pass

    def convert_to_si(self, data=None):
        pass

    def load(self):
        super(ZmqStream, self).load()
        self.data = pd.DataFrame(
            np.arange(len(self.data)),
            index=self.data.index,
            columns=['Counter'])
        zmq_data = load_zeromq(self.filenames, self.dtypes, root=self.rootfolder)
        self.data = self.data.join(zmq_data, on='Counter')

    def export_to_csv(self, export_path):
        self.data.to_csv(export_path)

    def add_clock_offset(self, offset):
        shift_stream_index(self.data, offset)


class PupilGazeStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(PupilGazeStream, self).__init__(
            eventcode,
            streamtype=StreamType.PUPIL,
            filenames=[
                'PupilLabs/Gaze_Frame0.bin',
                'PupilLabs/Gaze_Frame1.bin',
                'PupilLabs/Gaze_Frame2.bin'],
            dtypes=[
                [('SensorId', np.string_, 36)],
                [('Timestamp', np.uint64)],
                [('GazeX', np.single), ('GazeY', np.single)]],
            **kw)


class PupilWorldCameraStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(PupilWorldCameraStream, self).__init__(
            eventcode,
            streamtype=StreamType.PUPIL,
            filenames=[
                'PupilLabs/WorldCamera_Frame0.bin',
                'PupilLabs/WorldCamera_Frame1.bin',
                'PupilLabs/WorldCamera_Frame2.bin'],
            dtypes=[
                [('SensorId', np.string_, 36)],
                [('Format', np.uint32),
                 ('Width', np.uint32),
                 ('Height', np.uint32),
                 ('Sequence', np.uint32),
                 ('Timestamp', np.uint64),
                 ('DataBytes', np.uint32),
                 ('Reserved', np.uint32)],
                None],
            **kw)


class GliaEyeTrackingStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(GliaEyeTrackingStream, self).__init__(
            eventcode,
            streamtype=StreamType.GLIA,
            filenames=[
                'Glia/EyeTracking_Frame1.bin',
                'Glia/EyeTracking_Frame2.bin'],
            dtypes=[
                [('HardwareTime', np.ulonglong),
                 ('OmniceptTime', np.ulonglong),
                 ('SystemTime', np.ulonglong)],
                [('CombinedGaze.X', np.single),
                 ('CombinedGaze.Y', np.single),
                 ('CombinedGaze.Z', np.single),
                 ('LeftOpenness', np.single),
                 ('LeftOpennessConfidence', np.single),
                 ('LeftDilation', np.single),
                 ('LeftDilationConfidence', np.single),
                 ('LeftPosition.X', np.single),
                 ('LeftPosition.Y', np.single),
                 ('RightOpenness', np.single),
                 ('RightOpennessConfidence', np.single),
                 ('RightDilation', np.single),
                 ('RightDilationConfidence', np.single),
                 ('RightPosition.X', np.single),
                 ('RightPosition.Y', np.single)]],
            **kw)


class GliaHeartRateStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(GliaHeartRateStream, self).__init__(
            eventcode,
            streamtype=StreamType.GLIA,
            filenames=[
                'Glia/HeartRate_Frame1.bin',
                'Glia/HeartRate_Frame2.bin'],
            dtypes=[
                [('HardwareTime', np.ulonglong),
                 ('OmniceptTime', np.ulonglong),
                 ('SystemTime', np.ulonglong)],
                [('HeartRate', np.uintc)]],
            **kw)


class GliaImuStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(GliaImuStream, self).__init__(
            eventcode,
            streamtype=StreamType.GLIA,
            filenames=[
                'Glia/IMU_Frame1.bin',
                'Glia/IMU_Frame2.bin'],
            dtypes=[
                [('HardwareTime', np.ulonglong),
                 ('OmniceptTime', np.ulonglong),
                 ('SystemTime', np.ulonglong)],
                [('AccelX', np.single),
                 ('AccelY', np.single),
                 ('AccelZ', np.single),
                 ('GyroX', np.single),
                 ('GyroY', np.single),
                 ('GyroZ', np.single)]],
            **kw)


class UnityTransformStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(UnityTransformStream, self).__init__(
            eventcode,
            streamtype=StreamType.UNITY,
            filenames=[
                'VRTransform/Position_Frame1.bin',
                'VRTransform/Position_Frame2.bin'],
            dtypes=[
                [('Timestamp', np.ulonglong)],
                [('Transform.Position.X', np.single),
                 ('Transform.Position.Y', np.single),
                 ('Transform.Position.Z', np.single),
                 ('Transform.Forward.X', np.single),
                 ('Transform.Forward.Y', np.single),
                 ('Transform.Forward.Z', np.single)]],
            **kw)


class UnityPointToOriginWorldStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(UnityPointToOriginWorldStream, self).__init__(
            eventcode,
            streamtype=StreamType.UNITY,
            filenames=[
                'Unity_PointToOriginWorld/PointToOriginWorld_Frame1.bin',
                'Unity_PointToOriginWorld/PointToOriginWorld_Frame2.bin'],
            dtypes=[
                [('Timestamp', np.ulonglong)],
                [('Origin.Position.X', np.single),
                 ('Origin.Position.Y', np.single),
                 ('Origin.Position.Z', np.single),
                 ('Hand.Position.X', np.single),
                 ('Hand.Position.Y', np.single),
                 ('Hand.Position.Z', np.single),
                 ('HandAxis.Angle.X', np.single),
                 ('HandAxis.Angle.Y', np.single),
                 ('HandAxis.Angle.Z', np.single),
                 ('OriginAxis.Angle.X', np.single),
                 ('Transform.Angle.Y', np.single),
                 ('Transform.Angle.Z', np.single)]],
            **kw)


class UnityPointToOriginMapStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(UnityPointToOriginMapStream, self).__init__(
            eventcode,
            streamtype=StreamType.UNITY,
            filenames=[
                'Unity_PointToOriginMap/PointToOriginMap_Frame1.bin',
                'Unity_PointToOriginMap/PointToOriginMap_Frame2.bin'],
            dtypes=[
                [('Timestamp', np.ulonglong)],
                [('Origin.Position.X', np.single),
                 ('Origin.Position.Y', np.single),
                 ('Subject.Position.X', np.single),
                 ('Subject.Position.Y', np.single),
                 ('Point.Position.X', np.single),
                 ('Point.Position.Y', np.single)]],
            **kw)