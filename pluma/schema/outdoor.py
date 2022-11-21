from dotmap import DotMap

from pluma.stream.harp import HarpStream
from pluma.stream.accelerometer import AccelerometerStream
from pluma.stream.empatica import EmpaticaStream
from pluma.stream.ubx import UbxStream, _UBX_MSGIDS
from pluma.stream.microphone import MicrophoneStream


def build_schema(root: str = None, autoload: bool = False) -> DotMap:
    """Builds a stream schema from a predefined structure.

    Args:
        root (str, optional): Path to the folder containing the full dataset raw data. Defaults to None.
        autoload (bool, optional): If True it will automatically attempt to load data from disk. Defaults to False.

    Returns:
        DotMap: DotMap with all the created data streams.
    """
    streams = DotMap()
    # BioData streams
    streams.BioData.EnableStreams =               HarpStream(32, device='BioData', streamlabel='EnableStreams', root=root, autoload=autoload)
    streams.BioData.DisableStreams =              HarpStream(33, device='BioData', streamlabel='DisableStreams', root=root, autoload=autoload)
    streams.BioData.ECG =                         HarpStream(35, device='BioData', streamlabel='ECG', root=root, autoload=autoload)
    streams.BioData.GSR =                         HarpStream(36, device='BioData', streamlabel='GSR', root=root, autoload=autoload)
    streams.BioData.Accelerometer =               HarpStream(37, device='BioData', streamlabel='Accelerometer', root=root, autoload=autoload)
    streams.BioData.DigitalIn =                   HarpStream(38, device='BioData', streamlabel='DigitalIn', root=root, autoload=autoload)
    streams.BioData.Set =                         HarpStream(39, device='BioData', streamlabel='Set', root=root, autoload=autoload)
    streams.BioData.Clear =                       HarpStream(40, device='BioData', streamlabel='Clear', root=root, autoload=autoload)

    # PupilLabs streams
    streams.PupilLabs.LSLSampleTime =             HarpStream(220, device='PupilLabs', streamlabel='LSLSampleTime', root=root, autoload=autoload)
    streams.PupilLabs.LSLSampleArray =            HarpStream(221, device='PupilLabs', streamlabel='LSLSampleArray', root=root, autoload=autoload)


    # TinkerForge streams
    streams.TK.AmbientLight.AmbientLight =        HarpStream(223, device='TK', streamlabel='AmbientLight.AmbientLight', root=root, autoload=autoload)

    streams.TK.CO2V2.CO2Conc =                    HarpStream(224, device='TK', streamlabel='CO2V2.CO2Conc', root=root, autoload=autoload)
    streams.TK.CO2V2.Temperature =                HarpStream(225, device='TK', streamlabel='CO2V2.Temperature', root=root, autoload=autoload)
    streams.TK.CO2V2.Humidity =                   HarpStream(226, device='TK', streamlabel='CO2V2.Humidity', root=root, autoload=autoload)

    streams.TK.GPS.Latitude =                     HarpStream(227, device='TK', streamlabel='GPS.Latitude', root=root, autoload=autoload)
    streams.TK.GPS.Longitude =                    HarpStream(228, device='TK', streamlabel='GPS.Longitude', root=root, autoload=autoload)
    streams.TK.GPS.Altitude =                     HarpStream(229, device='TK', streamlabel='GPS.Altitude', root=root, autoload=autoload)
    streams.TK.GPS.Data =                         HarpStream(230, device='TK', streamlabel='GPS.Data', root=root, autoload=autoload)
    streams.TK.GPS.Time =                         HarpStream(231, device='TK', streamlabel='GPS.Time', root=root, autoload=autoload)
    streams.TK.GPS.HasFix =                       HarpStream(232, device='TK', streamlabel='GPS.HasFix', root=root, autoload=autoload)

    streams.TK.AirQuality.IAQIndex =              HarpStream(233, device='TK', streamlabel='AirQuality.IAQIndex', root=root, autoload=autoload)
    streams.TK.AirQuality.Temperature =           HarpStream(234, device='TK', streamlabel='AirQuality.Temperature', root=root, autoload=autoload)
    streams.TK.AirQuality.Humidity =              HarpStream(235, device='TK', streamlabel='AirQuality.Humidity', root=root, autoload=autoload)
    streams.TK.AirQuality.AirPressure =           HarpStream(236, device='TK', streamlabel='AirQuality.AirPressure', root=root, autoload=autoload)

    streams.TK.SoundPressureLevel.SPL =           HarpStream(237, device='TK', streamlabel='SoundPressureLevel.SPL', root=root, autoload=autoload)

    streams.TK.Humidity.Humidity =                HarpStream(238, device='TK', streamlabel='Humidity.Humidity', root=root, autoload=autoload)

    streams.TK.AnalogIn.Voltage =                 HarpStream(239, device='TK', streamlabel='AnalogIn.Voltage', root=root, autoload=autoload)

    streams.TK.ParticulateMatter.PM1_0 =          HarpStream(240, device='TK', streamlabel='ParticulateMatter.PM1_0', root=root, autoload=autoload)
    streams.TK.ParticulateMatter.PM2_5 =          HarpStream(241, device='TK', streamlabel='ParticulateMatter.PM2_5', root=root, autoload=autoload)
    streams.TK.ParticulateMatter.PM10_0 =         HarpStream(242, device='TK', streamlabel='ParticulateMatter.PM10_0', root=root, autoload=autoload)

    streams.TK.Dual0_20mA.SolarLight =      	  HarpStream(243, device='TK', streamlabel='Dual0_20mA.SolarLight', root=root, autoload=autoload)

    streams.TK.Thermocouple.Temperature =      	  HarpStream(244, device='TK', streamlabel='Thermocouple.Temperature', root=root, autoload=autoload)

    streams.TK.PTC.AirTemp =      	  			  HarpStream(245, device='TK', streamlabel='PTC.AirTemp', root=root, autoload=autoload)

    # ATMOS streams
    streams.Atmos.NorthWind =               	  HarpStream(246, device='Atoms', streamlabel='NorthWind', root=root, autoload=autoload)
    streams.Atmos.EastWind =              		  HarpStream(247, device='Atoms', streamlabel='EastWind', root=root, autoload=autoload)
    streams.Atmos.GustWind =                      HarpStream(248, device='Atoms', streamlabel='GustWind', root=root, autoload=autoload)
    streams.Atmos.AirTemperature =			  	  HarpStream(249, device='Atoms', streamlabel='AirTemperature', root=root, autoload=autoload)
    streams.Atmos.XOrientation =                  HarpStream(250, device='Atoms', streamlabel='XOrientation', root=root, autoload=autoload)
    streams.Atmos.YOrientation =                  HarpStream(251, device='Atoms', streamlabel='YOrientation', root=root, autoload=autoload)
    streams.Atmos.NullValue =                     HarpStream(252, device='Atoms', streamlabel='NullValue', root=root, autoload=autoload)

    # Accelerometer streams
    streams.Accelerometer =                       AccelerometerStream(device='Accelerometer', streamlabel='Accelerometer', root=root, autoload=autoload)

    # Empatica streams
    streams.Empatica =                            EmpaticaStream(device='Empatica', streamlabel='Empatica', root=root, autoload=autoload)

    # Microphone streams
    streams.Microphone.Audio =                    MicrophoneStream(device='Microphone', streamlabel='Audio', root=root, autoload=autoload)
    streams.Microphone.BufferIndex =              HarpStream(222, device='Microphone', streamlabel='BufferIndex', root=root, autoload=autoload)

    # UBX streams
    streams.UBX =                                 UbxStream(device='UBX', streamlabel='UBX', root=root, autoload=autoload,
                                                            autoload_messages=[
                                                                _UBX_MSGIDS.NAV_HPPOSLLH,
                                                                _UBX_MSGIDS.TIM_TM2,
                                                                _UBX_MSGIDS.TIM_TP,
                                                                ])

    return streams


