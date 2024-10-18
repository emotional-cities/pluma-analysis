from dotmap import DotMap
from typing import Union

from pluma.stream.ecg import EcgStream
from pluma.stream.eeg import EegStream
from pluma.stream.empatica import EmpaticaStream
from pluma.stream.harp import HarpStream
from pluma.stream.accelerometer import AccelerometerStream
from pluma.stream.zeromq import (
    GliaEyeTrackingStream,
    GliaHeartRateStream,
    GliaImuStream,
    ProtocolItiStream,
    ProtocolNewSceneStream,
    UnityGeoreferenceStream,
    UnityTransformStream,
    ProtocolPointToOriginWorldStream,
    ProtocolPointToOriginMapStream,
)

from pluma.io.path_helper import ComplexPath, ensure_complexpath


# fmt: off
def build_schema(root: Union[str, ComplexPath], parent_dataset=None, autoload: bool = False) -> DotMap:
    """Builds a stream schema from a predefined structure.

    Args:
        root (str, optional): Path to the folder containing the full dataset raw data. Defaults to None.
        autoload (bool, optional): If True it will automatically attempt to load data from disk. Defaults to False.

    Returns:
        DotMap: DotMap with all the created data streams.
    """
    root = ensure_complexpath(root)
    kwargs = dict(root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams = DotMap()

    # BioData streams
    streams.BioData.EnableStreams =         HarpStream(32, device="BioData", streamlabel="EnableStreams", **kwargs)
    streams.BioData.DisableStreams =        HarpStream(33, device="BioData", streamlabel="DisableStreams", **kwargs)
    streams.BioData.ECG =                   EcgStream (35, device="BioData", streamlabel="ECG", **kwargs)
    streams.BioData.GSR =                   HarpStream(36, device="BioData", streamlabel="GSR", **kwargs)
    streams.BioData.Accelerometer =         HarpStream(37, device="BioData", streamlabel="Accelerometer", **kwargs)
    streams.BioData.DigitalIn =             HarpStream(38, device="BioData", streamlabel="DigitalIn", **kwargs)
    streams.BioData.Set =                   HarpStream(39, device="BioData", streamlabel="Set", **kwargs)
    streams.BioData.Clear =                 HarpStream(40, device="BioData", streamlabel="Clear", **kwargs)

    # Accelerometer streams
    streams.Accelerometer =                 AccelerometerStream(device="Accelerometer", streamlabel="Accelerometer", **kwargs)

    # Empatica streams
    streams.Empatica =                      EmpaticaStream(device="Empatica", streamlabel="Empatica", **kwargs)

    # EEG stream    
    streams.EEG =                           EegStream(device="Enobio", streamlabel="EEG", **kwargs)

    # Glia streams
    streams.Glia.EyeTracking =              GliaEyeTrackingStream(215, device="Glia", streamlabel="EyeTracking", **kwargs)
    streams.Glia.HeartRate =                GliaHeartRateStream(216, device="Glia", streamlabel="HeartRate", **kwargs)
    streams.Glia.IMU =                      GliaImuStream(217, device="Glia", streamlabel="IMU", **kwargs)
    streams.Glia.Mouth.Timestamps =         HarpStream(218, device="Glia", streamlabel="Mouth_Timestamps", **kwargs)
    
    # Unity streams
    streams.Unity.Transform =               UnityTransformStream(219, device="Unity", streamlabel="Transform", **kwargs)
    streams.Unity.Video.Timestamps =        HarpStream(220, device="Unity", streamlabel="Video_Timestamps", **kwargs)
    streams.Unity.Georeference =            UnityGeoreferenceStream(221, device="Unity", streamlabel="Georeference", **kwargs)
    streams.Unity.SceneSequence =           ProtocolNewSceneStream(225, device="Unity", streamlabel="SceneSequence", **kwargs)
    streams.Unity.ITI =                     ProtocolItiStream(226, device="Unity", streamlabel="ITI", **kwargs)
    streams.Unity.PointToOriginWorld =      ProtocolPointToOriginWorldStream(227, device="Unity", streamlabel="PointToOriginWorld", **kwargs)
    streams.Unity.PointToOriginMap =        ProtocolPointToOriginMapStream(228, device="Unity", streamlabel="PointToOriginMap", **kwargs)

    return streams
