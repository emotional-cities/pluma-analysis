import numpy as np

from pluma.stream import StreamType
from pluma.stream.zeromq import ZmqStream


class UnityTransformStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(UnityTransformStream, self).__init__(
            eventcode,
            streamtype=StreamType.UNITY,
            clocksource="SystemDateTime",
            clockunit="us",
            filenames=["Unity/VRTransform_Frame1.bin", "Unity/VRTransform_Frame2.bin"],
            dtypes=[
                [("SystemDateTime", np.ulonglong)],
                [
                    ("Transform.Position.X", np.single),
                    ("Transform.Position.Y", np.single),
                    ("Transform.Position.Z", np.single),
                    ("Transform.Forward.X", np.single),
                    ("Transform.Forward.Y", np.single),
                    ("Transform.Forward.Z", np.single),
                ],
            ],
            **kw,
        )


class UnityGeoreferenceStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(UnityGeoreferenceStream, self).__init__(
            eventcode,
            streamtype=StreamType.UNITY,
            clocksource="SystemDateTime",
            clockunit="us",
            filenames=[
                "Unity/Georeference_Frame1.bin",
                "Unity/Georeference_Frame2.bin",
            ],
            dtypes=[
                [("SystemDateTime", np.ulonglong)],
                [
                    ("TargetPositionX", np.single),
                    ("TargetPositionY", np.single),
                    ("TargetPositionZ", np.single),
                    ("TargetLongitude", np.double),
                    ("TargetLatitude", np.double),
                    ("TargetAltitude", np.double),
                ],
            ],
            **kw,
        )


class ProtocolPointToOriginWorldStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(ProtocolPointToOriginWorldStream, self).__init__(
            eventcode,
            streamtype=StreamType.UNITY,
            clocksource="SystemDateTime",
            clockunit="us",
            filenames=[
                "Protocol/PointToOriginWorld_Frame1.bin",
                "Protocol/PointToOriginWorld_Frame2.bin",
            ],
            dtypes=[
                [("SystemDateTime", np.ulonglong)],
                [
                    ("Origin.Position.X", np.single),
                    ("Origin.Position.Y", np.single),
                    ("Origin.Position.Z", np.single),
                    ("Hand.Position.X", np.single),
                    ("Hand.Position.Y", np.single),
                    ("Hand.Position.Z", np.single),
                    ("HandAxis.Angle.X", np.single),
                    ("HandAxis.Angle.Y", np.single),
                    ("HandAxis.Angle.Z", np.single),
                    ("OriginAxis.Angle.X", np.single),
                    ("Transform.Angle.Y", np.single),
                    ("Transform.Angle.Z", np.single),
                ],
            ],
            **kw,
        )


class ProtocolPointToOriginMapStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(ProtocolPointToOriginMapStream, self).__init__(
            eventcode,
            streamtype=StreamType.UNITY,
            clocksource="SystemDateTime",
            clockunit="us",
            filenames=[
                "Protocol/PointToOriginMap_Frame1.bin",
                "Protocol/PointToOriginMap_Frame2.bin",
            ],
            dtypes=[
                [("SystemDateTime", np.ulonglong)],
                [
                    ("Origin.Position.X", np.single),
                    ("Origin.Position.Y", np.single),
                    ("Subject.Position.X", np.single),
                    ("Subject.Position.Y", np.single),
                    ("Point.Position.X", np.single),
                    ("Point.Position.Y", np.single),
                ],
            ],
            **kw,
        )


class ProtocolNewSceneStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(ProtocolNewSceneStream, self).__init__(
            eventcode,
            streamtype=StreamType.UNITY,
            clocksource="SystemDateTime",
            clockunit="us",
            filenames=["Protocol/NewScene_Frame1.bin", "Protocol/NewScene_Frame2.bin"],
            dtypes=[
                [("SystemDateTime", np.ulonglong)],
                [
                    ("SceneType", np.intc),
                    ("SpawnID", np.intc),
                    ("SceneDuration", np.intc),
                ],
            ],
            **kw,
        )


class ProtocolItiStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(ProtocolItiStream, self).__init__(
            eventcode,
            streamtype=StreamType.UNITY,
            clocksource="SystemDateTime",
            clockunit="us",
            filenames=["Protocol/ITI_Frame1.bin", "Protocol/ITI_Frame2.bin"],
            dtypes=[[("SystemDateTime", np.ulonglong)], [("InterTrialInterval", np.single)]],
            **kw,
        )
