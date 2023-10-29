from dotmap import DotMap
from typing import Union

from pluma.stream.harp import HarpStream
from pluma.stream.accelerometer import AccelerometerStream
from pluma.stream.empatica import EmpaticaStream
from pluma.stream.ubx import UbxStream, _UBX_MSGIDS
from pluma.stream.microphone import MicrophoneStream
from pluma.stream.eeg import EegStream
from pluma.stream.glia import GliaStream

from pluma.io.path_helper import ComplexPath, ensure_complexpath


def build_schema(root: Union[str, ComplexPath],
                 parent_dataset = None,
                 autoload: bool = False) -> DotMap:
    """Builds a stream schema from a predefined structure.

    Args:
        root (str, optional): Path to the folder containing the full dataset raw data. Defaults to None.
        autoload (bool, optional): If True it will automatically attempt to load data from disk. Defaults to False.

    Returns:
        DotMap: DotMap with all the created data streams.
    """
    root = ensure_complexpath(root)
    streams = DotMap()

    # BioData streams
    streams.BioData.EnableStreams =               HarpStream(32, device='BioData', streamlabel='EnableStreams', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.BioData.DisableStreams =              HarpStream(33, device='BioData', streamlabel='DisableStreams', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.BioData.ECG =                         HarpStream(35, device='BioData', streamlabel='ECG', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.BioData.GSR =                         HarpStream(36, device='BioData', streamlabel='GSR', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.BioData.Accelerometer =               HarpStream(37, device='BioData', streamlabel='Accelerometer', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.BioData.DigitalIn =                   HarpStream(38, device='BioData', streamlabel='DigitalIn', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.BioData.Set =                         HarpStream(39, device='BioData', streamlabel='Set', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.BioData.Clear =                       HarpStream(40, device='BioData', streamlabel='Clear', root=root, autoload=autoload, parent_dataset=parent_dataset)

    # TinkerForge streams
    streams.TK.AmbientLight.AmbientLight =        HarpStream(223, device='TK', streamlabel='AmbientLight.AmbientLight', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.TK.CO2V2.CO2Conc =                    HarpStream(224, device='TK', streamlabel='CO2V2.CO2Conc', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.CO2V2.Temperature =                HarpStream(225, device='TK', streamlabel='CO2V2.Temperature', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.CO2V2.Humidity =                   HarpStream(226, device='TK', streamlabel='CO2V2.Humidity', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.TK.GPS.Latitude =                     HarpStream(227, device='TK', streamlabel='GPS.Latitude', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.GPS.Longitude =                    HarpStream(228, device='TK', streamlabel='GPS.Longitude', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.GPS.Altitude =                     HarpStream(229, device='TK', streamlabel='GPS.Altitude', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.GPS.Data =                         HarpStream(230, device='TK', streamlabel='GPS.Data', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.GPS.Time =                         HarpStream(231, device='TK', streamlabel='GPS.Time', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.GPS.HasFix =                       HarpStream(232, device='TK', streamlabel='GPS.HasFix', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.TK.AirQuality.IAQIndex =              HarpStream(233, device='TK', streamlabel='AirQuality.IAQIndex', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.AirQuality.Temperature =           HarpStream(234, device='TK', streamlabel='AirQuality.Temperature', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.AirQuality.Humidity =              HarpStream(235, device='TK', streamlabel='AirQuality.Humidity', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.AirQuality.AirPressure =           HarpStream(236, device='TK', streamlabel='AirQuality.AirPressure', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.TK.SoundPressureLevel.SPL =           HarpStream(237, device='TK', streamlabel='SoundPressureLevel.SPL', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.TK.Humidity.Humidity =                HarpStream(238, device='TK', streamlabel='Humidity.Humidity', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.TK.AnalogIn.Voltage =                 HarpStream(239, device='TK', streamlabel='AnalogIn.Voltage', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.TK.ParticulateMatter.PM1_0 =          HarpStream(240, device='TK', streamlabel='ParticulateMatter.PM1_0', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.ParticulateMatter.PM2_5 =          HarpStream(241, device='TK', streamlabel='ParticulateMatter.PM2_5', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.TK.ParticulateMatter.PM10_0 =         HarpStream(242, device='TK', streamlabel='ParticulateMatter.PM10_0', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.TK.Dual0_20mA.SolarLight =      	  HarpStream(243, device='TK', streamlabel='Dual0_20mA.SolarLight', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.TK.Thermocouple.Temperature =      	  HarpStream(244, device='TK', streamlabel='Thermocouple.Temperature', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.TK.PTC.AirTemp =      	  			  HarpStream(245, device='TK', streamlabel='PTC.AirTemp', root=root, autoload=autoload, parent_dataset=parent_dataset)

    # Accelerometer streams
    streams.Accelerometer =                       AccelerometerStream(device='Accelerometer', streamlabel='Accelerometer', root=root, autoload=autoload, parent_dataset=parent_dataset)

    # # Empatica streams
    # streams.Empatica =                            EmpaticaStream(device='Empatica', streamlabel='Empatica', root=root, autoload=autoload, parent_dataset=parent_dataset)

    # # Microphone streams
    # streams.Microphone.Audio =                    MicrophoneStream(device='Microphone', streamlabel='Audio', root=root, autoload=autoload, parent_dataset=parent_dataset)
    # streams.Microphone.BufferIndex =              HarpStream(222, device='Microphone', streamlabel='BufferIndex', root=root, autoload=autoload, parent_dataset=parent_dataset)

    # # EEG stream
    # streams.EEG =                                 EegStream(device='Enobio', streamlabel='EEG', root=root, autoload=autoload, parent_dataset=parent_dataset)

    # Glia streams
    streams.Glia.EyeTracking.Timestamps =         HarpStream(215, device='Glia', streamlabel='Glia.EyeTracking.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.Glia.EyeTracking.Data =               GliaStream('Glia/EyeTracking.bin',
                                                             ['q', 'q', 'q', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f'],
                                                             ["HardwareTime", "OmniceptTime", "SystemTime", "CombinedGaze.X", "CombinedGaze.Y", "CombinedGaze.Z",
                                                              "LeftOpenness", "LeftOpennessConfidence", "LeftDilation", "LeftDilationConfidence", "LeftPosition.X", "LeftPosition.Y",
                                                              "RightOpenness", "RightOpennessConfidence", "RightDilation", "RightDilationConfidence", "RightPosition.X", "RightPosition.Y"],
                                                             device='Glia',
                                                             streamlabel='Glia.EyeTracking.Data',
                                                             root=root, autoload=autoload,
                                                             parent_dataset=parent_dataset)

    streams.Glia.HeartRate.Timestamps =           HarpStream(216, device='Glia', streamlabel='Glia.HeartRate.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.Glia.HeartRate.Data =                 GliaStream('Glia/HeartRate.bin',
                                                             ['q', 'q', 'q', 'I'],
                                                             ["HardwareTime", "OmniceptTime", "SystemTime", "HeartRate"],
                                                             device='Glia',
                                                             streamlabel='Glia.HeartRate.Data',
                                                             root=root, autoload=autoload,
                                                             parent_dataset=parent_dataset)

    streams.Glia.IMU.Timestamps =                 HarpStream(217, device='Glia', streamlabel='Glia.IMU.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.Glia.IMU.Data =                       GliaStream('Glia/IMU.bin',
                                                             ['q', 'q', 'q', 'f', 'f', 'f', 'f', 'f', 'f'],
                                                             ["HardwareTime", "OmniceptTime", "SystemTime", "AccelX", "AccelY", "AccelZ", "GyroX", "GyroY", "GyroZ"],
                                                             device='Glia',
                                                             streamlabel='Glia.IMU.Data',
                                                             root=root, autoload=autoload,
                                                             parent_dataset=parent_dataset)

    streams.Glia.Mouth.Timestamp =                HarpStream(218, device='Glia', streamlabel='Glia.Mouth.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.Unity.Transform.Timestamp =           HarpStream(219, device='Unity', streamlabel='Unity.Transform.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.Unity.Transform.Data =                GliaStream('VRTransform.bin',
                                                             ['q', 'f', 'f', 'f', 'f', 'f', 'f'],
                                                             ["Timestamp", "Transform.Position.X", "Transform.Position.Y", "Transform.Position.Z",
                                                              "Transform.Forward.X", "Transform.Forward.Y", "Transform.Forward.Z"],
                                                             device='Unity',
                                                             streamlabel='Unity.Transform.Data',
                                                             root=root, autoload=autoload,
                                                             parent_dataset=parent_dataset)

    streams.Unity.Video.Timestamp =               HarpStream(220, device='Unity', streamlabel='Unity.Video.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)

    return streams