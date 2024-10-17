# fmt: off
from dotmap import DotMap
from typing import Union

from pluma.stream.harp import HarpStream
from pluma.stream.accelerometer import AccelerometerStream
from pluma.stream.zeromq import GliaEyeTrackingStream, GliaHeartRateStream, GliaImuStream, UnityTransformStream, ProtocolPointToOriginWorldStream, ProtocolPointToOriginMapStream
from pluma.stream.csv import CsvStream

from pluma.io.path_helper import ComplexPath, ensure_complexpath


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
    streams.BioData.EnableStreams =               HarpStream(32, device="BioData", streamlabel="EnableStreams", **kwargs)
    streams.BioData.DisableStreams =              HarpStream(33, device="BioData", streamlabel="DisableStreams", **kwargs)
    streams.BioData.ECG =                         HarpStream(35, device="BioData", streamlabel="ECG", **kwargs)
    streams.BioData.GSR =                         HarpStream(36, device="BioData", streamlabel="GSR", **kwargs)
    streams.BioData.Accelerometer =               HarpStream(37, device="BioData", streamlabel="Accelerometer", **kwargs)
    streams.BioData.DigitalIn =                   HarpStream(38, device="BioData", streamlabel="DigitalIn", **kwargs)
    streams.BioData.Set =                         HarpStream(39, device="BioData", streamlabel="Set", **kwargs)
    streams.BioData.Clear =                       HarpStream(40, device="BioData", streamlabel="Clear", **kwargs)

    # TinkerForge streams
    streams.TK.AmbientLight.AmbientLight =        HarpStream(223, device="TK", streamlabel="AmbientLight.AmbientLight", **kwargs)

    streams.TK.CO2V2.CO2Conc =                    HarpStream(224, device="TK", streamlabel="CO2V2.CO2Conc", **kwargs)
    streams.TK.CO2V2.Temperature =                HarpStream(225, device="TK", streamlabel="CO2V2.Temperature", **kwargs)
    streams.TK.CO2V2.Humidity =                   HarpStream(226, device="TK", streamlabel="CO2V2.Humidity", **kwargs)

    streams.TK.GPS.Latitude =                     HarpStream(227, device="TK", streamlabel="GPS.Latitude", **kwargs)
    streams.TK.GPS.Longitude =                    HarpStream(228, device="TK", streamlabel="GPS.Longitude", **kwargs)
    streams.TK.GPS.Altitude =                     HarpStream(229, device="TK", streamlabel="GPS.Altitude", **kwargs)
    streams.TK.GPS.Data =                         HarpStream(230, device="TK", streamlabel="GPS.Data", **kwargs)
    streams.TK.GPS.Time =                         HarpStream(231, device="TK", streamlabel="GPS.Time", **kwargs)
    streams.TK.GPS.HasFix =                       HarpStream(232, device="TK", streamlabel="GPS.HasFix", **kwargs)

    streams.TK.AirQuality.IAQIndex =              HarpStream(233, device="TK", streamlabel="AirQuality.IAQIndex", **kwargs)
    streams.TK.AirQuality.Temperature =           HarpStream(234, device="TK", streamlabel="AirQuality.Temperature", **kwargs)
    streams.TK.AirQuality.Humidity =              HarpStream(235, device="TK", streamlabel="AirQuality.Humidity", **kwargs)
    streams.TK.AirQuality.AirPressure =           HarpStream(236, device="TK", streamlabel="AirQuality.AirPressure", **kwargs)

    streams.TK.SoundPressureLevel.SPL =           HarpStream(237, device="TK", streamlabel="SoundPressureLevel.SPL", **kwargs)

    streams.TK.Humidity.Humidity =                HarpStream(238, device="TK", streamlabel="Humidity.Humidity", **kwargs)

    streams.TK.AnalogIn.Voltage =                 HarpStream(239, device="TK", streamlabel="AnalogIn.Voltage", **kwargs)

    streams.TK.ParticulateMatter.PM1_0 =          HarpStream(240, device="TK", streamlabel="ParticulateMatter.PM1_0", **kwargs)
    streams.TK.ParticulateMatter.PM2_5 =          HarpStream(241, device="TK", streamlabel="ParticulateMatter.PM2_5", **kwargs)
    streams.TK.ParticulateMatter.PM10_0 =         HarpStream(242, device="TK", streamlabel="ParticulateMatter.PM10_0", **kwargs)

    streams.TK.Dual0_20mA.SolarLight =            HarpStream(243, device="TK", streamlabel="Dual0_20mA.SolarLight", **kwargs)

    streams.TK.Thermocouple.Temperature =         HarpStream(244, device="TK", streamlabel="Thermocouple.Temperature", **kwargs)

    streams.TK.PTC.AirTemp =                      HarpStream(245, device="TK", streamlabel="PTC.AirTemp", **kwargs)

    # Accelerometer streams
    streams.Accelerometer =                       AccelerometerStream(device="Accelerometer", streamlabel="Accelerometer", **kwargs)

    # # Empatica streams
    # streams.Empatica =                            EmpaticaStream(device='Empatica', streamlabel='Empatica', **kwargs)

    # # Microphone streams    
    # streams.Microphone.Audio =                    MicrophoneStream(device='Microphone', streamlabel='Audio', **kwargs)
    # streams.Microphone.BufferIndex =              HarpStream(222, device='Microphone', streamlabel='BufferIndex', **kwargs)

    # # EEG stream    
    # streams.EEG =                                 EegStream(device='Enobio', streamlabel='EEG', **kwargs)

    # Glia streams
    streams.Glia.EyeTracking.Timestamps =         HarpStream(215, device="Glia", streamlabel="Glia.EyeTracking.Timestamps", **kwargs)
    streams.Glia.EyeTracking.Data =               GliaEyeTrackingStream(device="Glia", streamlabel="Glia.EyeTracking.Data", **kwargs)

    streams.Glia.HeartRate.Timestamps =           HarpStream(216, device="Glia", streamlabel="Glia.HeartRate.Timestamps", **kwargs)
    streams.Glia.HeartRate.Data =                 GliaHeartRateStream(device="Glia", streamlabel="Glia.HeartRate.Data", **kwargs)

    streams.Glia.IMU.Timestamps =                 HarpStream(217, device="Glia", streamlabel="Glia.IMU.Timestamps", **kwargs)
    streams.Glia.IMU.Data =                       GliaImuStream(device="Glia", streamlabel="Glia.IMU.Data", **kwargs)

    streams.Glia.Mouth.Timestamps =               HarpStream(218, device="Glia", streamlabel="Glia.Mouth.Timestamps", **kwargs)

    streams.Unity.Transform.Timestamps =          HarpStream(219, device="Unity", streamlabel="Transform.Timestamps", **kwargs)
    streams.Unity.Transform.Data =                UnityTransformStream(device="Unity", streamlabel="Transform.Data", **kwargs)

    streams.Unity.Video.Timestamps =              HarpStream(220, device="Unity", streamlabel="Video.Timestamps", **kwargs)

    streams.Unity.PointToOriginWorld.Timestamps = HarpStream(227, device="Unity", streamlabel="PointToOriginWorld.Timestamps", **kwargs)
    streams.Unity.PointToOriginWorld.Data =       ProtocolPointToOriginWorldStream(device="Unity", streamlabel="PointToOriginWorld.Data", **kwargs)

    streams.Unity.PointToOriginMap.Timestamps =   HarpStream(228, device="Unity", streamlabel="PointToOriginMap.Timestamps", **kwargs)
    streams.Unity.PointToOriginMap.Data =         ProtocolPointToOriginMapStream(device="Unity", streamlabel="PointToOriginMap.Data", **kwargs)

    streams.Unity.SceneSequence =                 CsvStream("Unity_SceneSequence.csv", device="Unity", streamlabel="SceneSequence", **kwargs)

    return streams
