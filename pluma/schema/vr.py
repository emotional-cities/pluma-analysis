from dotmap import DotMap
from typing import Union
import numpy as np

from pluma.stream.harp import HarpStream
from pluma.stream.accelerometer import AccelerometerStream
from pluma.stream.empatica import EmpaticaStream
from pluma.stream.ubx import UbxStream, _UBX_MSGIDS
from pluma.stream.microphone import MicrophoneStream
from pluma.stream.eeg import EegStream
from pluma.stream.zeromq import ZeromqStream
from pluma.stream.csv import CsvStream

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

    glia_t_types = [('HardwareTime', np.ulonglong), ('OmniceptTime', np.ulonglong), ('SystemTime', np.ulonglong)]  # timestamp data types and labels for glia streams

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
    streams.Glia.EyeTracking.Data =               ZeromqStream(['Glia/EyeTracking_Frame1.bin', 'Glia/EyeTracking_Frame2.bin'],
                                                               [glia_t_types,
                                                               [('CombinedGaze.X', np.single), ('CombinedGaze.Y', np.single), ('CombinedGaze.Z', np.single), ('LeftOpenness', np.single), ('LeftOpennessConfidence', np.single), ('LeftDilation', np.single), ('LeftDilationConfidence', np.single), ('LeftPosition.X', np.single), ('LeftPosition.Y', np.single), ('RightOpenness', np.single), ('RightOpennessConfidence', np.single), ('RightDilation', np.single), ('RightDilationConfidence', np.single), ('RightPosition.X', np.single), ('RightPosition.Y', np.single)]],
                                                               device='Glia',
                                                               streamlabel='Glia.EyeTracking.Data',
                                                               root=root, autoload=autoload,
                                                               parent_dataset=parent_dataset)

    streams.Glia.HeartRate.Timestamps =           HarpStream(216, device='Glia', streamlabel='Glia.HeartRate.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.Glia.HeartRate.Data =                 ZeromqStream(['Glia/HeartRate_Frame1.bin', 'Glia/HeartRate_Frame2.bin'],
                                                               [glia_t_types, 
                                                               [('HardwareTime', np.uintc)]],
                                                               device='Glia',
                                                               streamlabel='Glia.HeartRate.Data',
                                                               root=root, autoload=autoload,
                                                               parent_dataset=parent_dataset)

    streams.Glia.IMU.Timestamps =                 HarpStream(217, device='Glia', streamlabel='Glia.IMU.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.Glia.IMU.Data =                       ZeromqStream(['Glia/IMU_Frame1.bin', 'Glia/IMU_Frame2.bin'],
                                                               [glia_t_types, 
                                                               [('AccelX', np.single), ('AccelY', np.single), ('AccelZ', np.single), ('GyroX', np.single), ('GyroY', np.single), ('GyroZ', np.single)]],
                                                               device='Glia',
                                                               streamlabel='Glia.IMU.Data',
                                                               root=root, autoload=autoload,
                                                               parent_dataset=parent_dataset)

    streams.Glia.Mouth.Timestamps =                HarpStream(218, device='Glia', streamlabel='Glia.Mouth.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.Unity.Transform.Timestamps =           HarpStream(219, device='Unity', streamlabel='Unity.Transform.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.Unity.Transform.Data =                 ZeromqStream(['VRTransform/Position_Frame1.bin', 'VRTransform/Position_Frame2.bin'],
                                                                [[('Timestamp', np.ulonglong)], 
                                                                [('Transform.Position.X', np.single), ('Transform.Position.Y', np.single), ('Transform.Position.Z', np.single),
                                                                ('Transform.Forward.X', np.single), ('Transform.Forward.Y', np.single), ('Transform.Forward.Z', np.single)]],
                                                                device='Unity',
                                                                streamlabel='Unity.Transform.Data',
                                                                root=root, autoload=autoload,
                                                                parent_dataset=parent_dataset)

    streams.Unity.Video.Timestamps =               HarpStream(220, device='Unity', streamlabel='Unity.Video.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)

    streams.Unity.PointToOriginWorld.Timestamps =  HarpStream(227, device='Unity', streamlabel='Unity.PointToOriginWorld.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.Unity.PointToOriginWorld.Data =        ZeromqStream(['Unity_PointToOriginWorld/PointToOriginWorld_Frame1.bin', 'Unity_PointToOriginWorld/PointToOriginWorld_Frame2.bin'],
                                                                [[('Timestamp', np.ulonglong)], 
                                                                [('Origin.Position.X', np.single), ('Origin.Position.Y', np.single), ('Origin.Position.Z', np.single),
                                                                ('Hand.Position.X', np.single), ('Hand.Position.Y', np.single), ('Hand.Position.Z', np.single),
                                                                ('HandAxis.Angle.X', np.single), ('HandAxis.Angle.Y', np.single), ('HandAxis.Angle.Z', np.single),
                                                                ('OriginAxis.Angle.X', np.single), ('Transform.Angle.Y', np.single), ('Transform.Angle.Z', np.single)]],
                                                                device='Unity',
                                                                streamlabel='Unity.PointToOriginWorld.Data',
                                                                root=root, autoload=autoload,
                                                                parent_dataset=parent_dataset)

    streams.Unity.PointToOriginMap.Timestamps =    HarpStream(228, device='Unity', streamlabel='Unity.PointToOriginMap.Timestamps', root=root, autoload=autoload, parent_dataset=parent_dataset)
    streams.Unity.PointToOriginMap.Data =          ZeromqStream(['Unity_PointToOriginMap/PointToOriginMap_Frame1.bin', 'Unity_PointToOriginMap/PointToOriginMap_Frame2.bin'],
                                                                [[('Timestamp', np.ulonglong)], 
                                                                [('Origin.Position.X', np.single), ('Origin.Position.Y', np.single),
                                                                ('Subject.Position.X', np.single), ('Subject.Position.Y', np.single),
                                                                ('Point.Position.X', np.single), ('Point.Position.Y', np.single)]],
                                                                device='Unity',
                                                                streamlabel='Unity.PointToOriginMap.Data',
                                                                root=root, autoload=autoload,
                                                                parent_dataset=parent_dataset)

    streams.Unity.SceneSequence =                  CsvStream('Unity_SceneSequence.csv', device='Unity',
                                                             streamlabel='Unity.SceneSequence',
                                                             root=root, autoload=autoload,
                                                             parent_dataset=parent_dataset)

    return streams

