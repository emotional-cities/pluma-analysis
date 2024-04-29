import numpy as np
import pandas as pd

from pluma.stream import StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.sync import ClockRefId
from pluma.stream.zeromq import ZmqStream
from pluma.io.zeromq import load_zeromq


class PupilStream(ZmqStream):
    def __init__(self,
                 frame1_dtypes: list[tuple[str, type]],
                 frame2_dtypes: list[tuple[str, type]],  
                 data: pd.DataFrame = None, 
                 si_conversion: SiUnitConversion = ..., 
                 clockreferenceid: ClockRefId = ClockRefId.HARP, 
                 **kw):
        super(PupilStream,self).__init__(
                         [[('SensorId', np.string_, 36)], frame1_dtypes, frame2_dtypes], 
                         data, 
                         si_conversion, 
                         clockreferenceid,
                        **kw)
        self.streamtype = StreamType.PUPIL

    def load(self):
        self.data = load_zeromq([self.device + '_Frame0.bin', self.device + '_Frame1.bin', self.device + '_Frame2.bin'], 
                                self.dtypes, root=self.rootfolder)
