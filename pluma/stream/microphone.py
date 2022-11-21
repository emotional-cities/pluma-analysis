import numpy as np

from pluma.stream import Stream, StreamType
from pluma.stream.siconversion import SiUnitConversion
from pluma.io.microphone import load_microphone

class MicrophoneStream (Stream):
	"""_summary_

	Args:
		Stream (_type_): _description_
	"""
	def __init__(self,
              data: np.array = np.empty(shape=(0, 2)),
              fs: float = None,
              channels: int = 2,
              si_conversion: SiUnitConversion = SiUnitConversion(),
              **kw):
		super(MicrophoneStream, self).__init__(data=data, **kw)
		self.streamtype = StreamType.MICROPHONE
		self.fs = fs
		self.channels = channels
		self.si_conversion = si_conversion

		if self.autoload:
			self.load()

	def load(self):
		self.data = load_microphone(root=self.rootfolder, channels=self.channels)

	def __str__(self):
		return f'Microphone stream from device {self.device},\
      stream {self.streamlabel}'
