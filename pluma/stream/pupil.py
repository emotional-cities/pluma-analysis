import numpy as np
import pandas as pd

from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.sync import ClockRefId
from pluma.stream.zeromq import ZmqStream


class PupilStream(ZmqStream):
    def __init__(self, filenames: str, 
                 frame1_dtypes: list[tuple[str, type]],
                 frame2_dtypes: list[tuple[str, type]],  
                 data: pd.DataFrame = None, 
                 si_conversion: SiUnitConversion = ..., 
                 clockreferenceid: ClockRefId = ClockRefId.HARP, 
                 **kw):
        super(PupilStream,self).__init__(filenames, 
                         [[('SensorId', np.string_, 36)], frame1_dtypes, frame2_dtypes], 
                         data, 
                         si_conversion, 
                         clockreferenceid,
                        **kw)
        self.streamtype = StreamType.PUPIL

    
