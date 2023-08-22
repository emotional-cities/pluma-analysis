import pandas as pd
import datetime

from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.io.accelerometer import load_accelerometer, _accelerometer_header
from pluma.sync import ClockRefId
from pluma.export.streams import resample_stream_accelerometer

class AccelerometerStream(Stream):
	"""_summary_

	Args:
		Stream (_type_): _description_
	"""
	def __init__(self,
              data: pd.DataFrame = pd.DataFrame(
                  columns=_accelerometer_header),
              si_conversion: SiUnitConversion = SiUnitConversion(),
              clockreferenceid: ClockRefId = ClockRefId.HARP,
              **kw):

		super(AccelerometerStream, self).__init__(
                                            data=data,
                                            **kw)
		self.streamtype = StreamType.ACCELEROMETER
		self.si_conversion = si_conversion
		self.clockreference.referenceid = clockreferenceid

		if self.autoload:
			self.load()

		if self.si_conversion.attempt_conversion:
			self.convert_to_si()

	def convert_to_si(self, data=None):
		"""Method to convert data to SI units
		"""
		if data is None:  # Default to the instance's data if None is provided
			self.data = self.si_conversion.convert_to_si(self.data)
			self.si_conversion.is_si = True
		else:  # if some other data source is provided...
			return self.si_conversion.convert_to_si(data)

	def load(self):
		self.data = load_accelerometer(root=self.rootfolder)
		self.si_conversion.is_si = False

	def __str__(self):
		return f'Accelerometer stream from device {self.device},\
      stream {self.streamlabel}'

	def resample(self,
	      sampling_dt: datetime.timedelta,
		  **kwargs) -> pd.DataFrame:
		return resample_stream_accelerometer(self, sampling_dt, **kwargs)
