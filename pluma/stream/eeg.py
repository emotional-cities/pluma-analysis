import pandas as pd

from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.io.eeg import load_eeg, _eeg_header, _eeg_header


class EegStream(Stream):
	"""_summary_

	Args:
		Stream (_type_): _description_
	"""
	def __init__(self,
              data: pd.DataFrame = pd.DataFrame(
                  columns=_eeg_header),
              si_conversion: SiUnitConversion = SiUnitConversion(),
              **kw):
		super(EegStream, self).__init__(data=data, **kw)
		self.streamtype = StreamType.EEG
		self.si_conversion = si_conversion

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
		self.data = load_eeg(root=self.rootfolder)

	def __str__(self):
		return f'EEG stream from device {self.device},\
      stream {self.streamlabel}'