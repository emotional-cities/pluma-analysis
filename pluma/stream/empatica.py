from pluma.stream import Stream, StreamType
from pluma.io.empatica import load_empatica
from pluma.sync import ClockRefId


class EmpaticaStream(Stream):
	"""_summary_

	Args:
		Stream (_type_): _description_
	"""
	def __init__(self,
              clockreferenceid: ClockRefId = ClockRefId.HARP,
              **kw):
		super(EmpaticaStream, self).__init__(**kw)
		self.streamtype = StreamType.EMPATICA
		self.clockreferencering.reference = clockreferenceid

		if self.autoload:
			self.load()

	def load(self):
		self.data = load_empatica(root=self.rootfolder)

	def __str__(self):
		return f'Empatica stream from device {self.device}, stream {self.streamlabel}'