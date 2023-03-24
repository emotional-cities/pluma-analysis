from typing import Union, Optional

from pluma.stream import Stream, StreamType
from pluma.io.eeg import load_eeg
from pluma.sync import ClockRefId

from pluma.io._nepy.NedfReader import NedfReader


class EegStream(Stream):
	"""_summary_

	Args:
		Stream (_type_): _description_
	"""
	def __init__(self,
			data: Optional[NedfReader] = None,
			clockreferenceid: ClockRefId = ClockRefId.HARP,
			**kw):

		super(EegStream, self).__init__(data=data, **kw)
		self.streamtype = StreamType.EEG
		self.clockreferencering.reference = clockreferenceid

		if self.autoload:
			self.load()

	def load(self):
		self.data = load_eeg(
			filename=None,
			root=self.rootfolder)

	def __str__(self):
		return f'EEG stream from device {self.device}, stream {self.streamlabel}'