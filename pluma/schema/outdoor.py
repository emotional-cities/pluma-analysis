from dotmap import DotMap
from typing import Union

from pluma.stream.ecg import EcgStream
from pluma.stream.harp import HarpStream
from pluma.stream.accelerometer import AccelerometerStream
from pluma.stream.empatica import EmpaticaStream
from pluma.stream.ubx import UbxStream, _UBX_MSGIDS
from pluma.stream.microphone import MicrophoneStream
from pluma.stream.eeg import EegStream
from pluma.stream.zeromq import PupilGazeStream, PupilWorldCameraStream

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
    streams.BioData.Accelerometer =         HarpStream(37, device="BioData", streamlabel="Accelerometer", **kwargs)
    streams.BioData.DigitalIn =             HarpStream(38, device="BioData", streamlabel="DigitalIn", **kwargs)
    streams.BioData.Set =                   HarpStream(39, device="BioData", streamlabel="Set", **kwargs)
    streams.BioData.Clear =                 HarpStream(40, device="BioData", streamlabel="Clear", **kwargs)

    # Pluma streams
    streams.Pluma.ECG =                     EcgStream (35, device="Pluma", streamlabel="ECG", **kwargs)
    streams.Pluma.GSR =                     HarpStream(36, device="Pluma", streamlabel="GSR", **kwargs)

    # Pupil streams
    streams.PupilLabs.DecodedFrames =       HarpStream(209, device="PupilLabs", streamlabel="Pupil_RawFrames", **kwargs)
    streams.PupilLabs.RawFrames =           PupilWorldCameraStream(210, device="PupilLabs", streamlabel="Pupil_RawFrames", **kwargs)
    streams.PupilLabs.Counter.IMU =         HarpStream(211, device="PupilLabs", streamlabel="Counter_IMU", **kwargs)
    streams.PupilLabs.PupilGaze =           PupilGazeStream(212, device="PupilLabs", streamlabel="Pupil_Gaze", **kwargs)
    streams.PupilLabs.Counter.Audio =       HarpStream(213, device="PupilLabs", streamlabel="Counter_Audio", **kwargs)
    streams.PupilLabs.Counter.Key =         HarpStream(214, device="PupilLabs", streamlabel="Counter_Key", **kwargs)

    # TinkerForge streams
    streams.TK.GPS.Latitude =               HarpStream(227, device="TK", streamlabel="GPS_Latitude", **kwargs)
    streams.TK.GPS.Longitude =              HarpStream(228, device="TK", streamlabel="GPS_Longitude", **kwargs)
    streams.TK.GPS.Altitude =               HarpStream(229, device="TK", streamlabel="GPS_Altitude", **kwargs)
    streams.TK.GPS.Data =                   HarpStream(230, device="TK", streamlabel="GPS_Data", **kwargs)
    streams.TK.GPS.Time =                   HarpStream(231, device="TK", streamlabel="GPS_Time", **kwargs)
    streams.TK.GPS.HasFix =                 HarpStream(232, device="TK", streamlabel="GPS_HasFix", **kwargs)
  
    streams.TK.AirQuality.IAQIndex =        HarpStream(233, device="TK", streamlabel="AirQuality_IAQIndex", **kwargs)
    streams.TK.AirQuality.Temperature =     HarpStream(234, device="TK", streamlabel="AirQuality_Temperature", **kwargs)
    streams.TK.AirQuality.Humidity =        HarpStream(235, device="TK", streamlabel="AirQuality_Humidity", **kwargs)
    streams.TK.AirQuality.AirPressure =     HarpStream(236, device="TK", streamlabel="AirQuality_AirPressure", **kwargs)
  
    streams.TK.SoundPressureLevel.SPL =     HarpStream(237, device="TK", streamlabel="SoundPressureLevel_SPL", **kwargs)
  
    streams.TK.Humidity.Humidity =          HarpStream(238, device="TK", streamlabel="Humidity_Humidity", **kwargs)
  
    streams.TK.AnalogIn.Voltage =           HarpStream(239, device="TK", streamlabel="AnalogIn_Voltage", **kwargs)
  
    streams.TK.ParticulateMatter.PM1_0 =    HarpStream(240, device="TK", streamlabel="ParticulateMatter_PM1_0", **kwargs)
    streams.TK.ParticulateMatter.PM2_5 =    HarpStream(241, device="TK", streamlabel="ParticulateMatter_PM2_5", **kwargs)
    streams.TK.ParticulateMatter.PM10_0 =   HarpStream(242, device="TK", streamlabel="ParticulateMatter_PM10_0", **kwargs)
  
    streams.TK.Dual0_20mA.SolarLight =      HarpStream(243, device="TK", streamlabel="Dual0_20mA_SolarLight", **kwargs)
  
    streams.TK.Thermocouple.Temperature =   HarpStream(244, device="TK", streamlabel="Thermocouple_Temperature", **kwargs)
  
    streams.TK.PTC.AirTemp =                HarpStream(245, device="TK", streamlabel="PTC_AirTemp", **kwargs)
  
    # ATMOS streams
    streams.Atmos.NorthWind =               HarpStream(246, device="Atmos", streamlabel="NorthWind", **kwargs)
    streams.Atmos.EastWind =                HarpStream(247, device="Atmos", streamlabel="EastWind", **kwargs)
    streams.Atmos.GustWind =                HarpStream(248, device="Atmos", streamlabel="GustWind", **kwargs)
    streams.Atmos.AirTemperature =          HarpStream(249, device="Atmos", streamlabel="AirTemperature", **kwargs)
    streams.Atmos.XOrientation =            HarpStream(250, device="Atmos", streamlabel="XOrientation", **kwargs)
    streams.Atmos.YOrientation =            HarpStream(251, device="Atmos", streamlabel="YOrientation", **kwargs)
    streams.Atmos.NullValue =               HarpStream(252, device="Atmos", streamlabel="NullValue", **kwargs)
  
    # Accelerometer streams
    streams.Accelerometer =                 AccelerometerStream(device="Accelerometer", streamlabel="Accelerometer", **kwargs)
  
    # Empatica streams
    streams.Empatica =                      EmpaticaStream(device="Empatica", streamlabel="Empatica", **kwargs)
  
    # Microphone streams
    streams.Microphone.Audio =              MicrophoneStream(device="Microphone", streamlabel="Audio", **kwargs)
    streams.Microphone.BufferIndex =        HarpStream(222, device="Microphone", streamlabel="BufferIndex", **kwargs)
  
    # UBX streams
    streams.UBX =                           UbxStream(device="UBX", streamlabel="UBX", **kwargs,
                                                      autoload_messages=[
                                                          _UBX_MSGIDS.NAV_HPPOSLLH,
                                                          _UBX_MSGIDS.TIM_TM2,
                                                          _UBX_MSGIDS.TIM_TP,
                                                      ])

    # EEG stream
    streams.EEG =                           EegStream(device="Enobio", streamlabel="EEG", **kwargs)
    return streams
