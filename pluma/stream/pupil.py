import numpy as np

from pluma.stream import StreamType
from pluma.stream.zeromq import ZmqStream


class PupilGazeStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(PupilGazeStream, self).__init__(
            eventcode,
            streamtype=StreamType.PUPIL,
            filenames=[
                "PupilLabs/Gaze_Frame0.bin",
                "PupilLabs/Gaze_Frame1.bin",
                "PupilLabs/Gaze_Frame2.bin",
            ],
            dtypes=[
                [("SensorId", np.bytes_, 36)],
                [("PupilTime", np.uint64)],
                [("GazeX", np.single), ("GazeY", np.single)],
            ],
            **kw,
        )


class PupilWorldCameraStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(PupilWorldCameraStream, self).__init__(
            eventcode,
            streamtype=StreamType.PUPIL,
            filenames=[
                "PupilLabs/WorldCamera_Frame0.bin",
                "PupilLabs/WorldCamera_Frame1.bin",
                "PupilLabs/WorldCamera_Frame2.bin",
            ],
            dtypes=[
                [("SensorId", np.bytes_, 36)],
                [
                    ("Format", np.uint32),
                    ("Width", np.uint32),
                    ("Height", np.uint32),
                    ("Sequence", np.uint32),
                    ("PupilTime", np.uint64),
                    ("DataBytes", np.uint32),
                    ("Reserved", np.uint32),
                ],
                None,
            ],
            **kw,
        )
