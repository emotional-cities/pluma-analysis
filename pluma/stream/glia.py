import numpy as np

from pluma.stream import StreamType
from pluma.stream.zeromq import ZmqStream


class GliaEyeTrackingStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(GliaEyeTrackingStream, self).__init__(
            eventcode,
            streamtype=StreamType.GLIA,
            filenames=["Glia/EyeTracking_Frame1.bin", "Glia/EyeTracking_Frame2.bin"],
            dtypes=[
                [
                    ("HardwareTime", np.ulonglong),
                    ("OmniceptTime", np.ulonglong),
                    ("SystemTime", np.ulonglong),
                ],
                [
                    ("CombinedGaze.X", np.single),
                    ("CombinedGaze.Y", np.single),
                    ("CombinedGaze.Z", np.single),
                    ("LeftOpenness", np.single),
                    ("LeftOpennessConfidence", np.single),
                    ("LeftDilation", np.single),
                    ("LeftDilationConfidence", np.single),
                    ("LeftPosition.X", np.single),
                    ("LeftPosition.Y", np.single),
                    ("RightOpenness", np.single),
                    ("RightOpennessConfidence", np.single),
                    ("RightDilation", np.single),
                    ("RightDilationConfidence", np.single),
                    ("RightPosition.X", np.single),
                    ("RightPosition.Y", np.single),
                    ("Raycast.X", np.single),
                    ("Raycast.Y", np.single),
                    ("Raycast.Z", np.single),
                ],
            ],
            **kw,
        )


class GliaHeartRateStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(GliaHeartRateStream, self).__init__(
            eventcode,
            streamtype=StreamType.GLIA,
            filenames=["Glia/HeartRate_Frame1.bin", "Glia/HeartRate_Frame2.bin"],
            dtypes=[
                [
                    ("HardwareTime", np.ulonglong),
                    ("OmniceptTime", np.ulonglong),
                    ("SystemTime", np.ulonglong),
                ],
                [("HeartRate", np.uintc)],
            ],
            **kw,
        )


class GliaImuStream(ZmqStream):
    def __init__(self, eventcode: int, **kw):
        super(GliaImuStream, self).__init__(
            eventcode,
            streamtype=StreamType.GLIA,
            filenames=["Glia/IMU_Frame1.bin", "Glia/IMU_Frame2.bin"],
            dtypes=[
                [
                    ("HardwareTime", np.ulonglong),
                    ("OmniceptTime", np.ulonglong),
                    ("SystemTime", np.ulonglong),
                ],
                [
                    ("AccelX", np.single),
                    ("AccelY", np.single),
                    ("AccelZ", np.single),
                    ("GyroX", np.single),
                    ("GyroY", np.single),
                    ("GyroZ", np.single),
                ],
            ],
            **kw,
        )
