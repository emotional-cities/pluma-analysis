from enum import Enum
import matplotlib.pyplot as plt
from typing import Union

from pluma.io.path_helper import ComplexPath, ensure_complexpath

class StreamType(Enum):
	NONE = None
	UBX = 'UbxStream'
	HARP = 'HarpStream'
	ACCELEROMETER = 'AccelerometerStream'
	MICROPHONE = 'MicrophoneStream'
	EMPATICA = 'EmpaticaStream'
	EEG = 'EegStream'


class Stream:
	"""Based class for all stream types
	"""
	def __init__(self,
              device: str,
              streamlabel: str,
              root: Union[str, ComplexPath] = '',
              data: any = None,
              autoload: bool = True):
		"""_summary_
		Args:
			device (str): Device label
			streamlabel (str): Stream label
			root (str, optional): Root path where the files of the stream are expected to be found. Defaults to ''.
			data (any, optional): Data to initially populate the stream. Defaults to None.
			autoload (bool, optional): If True, it will attempt to automatically load the data when instantiated. Defaults to True.
		"""

		self.device = device
		self.streamlabel = streamlabel
		self._rootfolder = self.rootfolder = ensure_complexpath(root)
		self.data = data
		self.autoload = autoload
		self.streamtype = StreamType.NONE

	@property
	def rootfolder(self):
		return self._rootfolder

	@rootfolder.setter
	def rootfolder(self, value: Union[str, ComplexPath]):
		self._rootfolder = ensure_complexpath(value)

	def load(self):
		raise NotImplementedError("load() method is not implemented for the Stream base class.")

	def plot(self, col=None, **kwargs):
		if self.data.empty:
			raise ValueError("Input dataframe is empty.")
		thisfigure = plt.figure()
		label = self.device + "." + self.streamlabel
		if col is None:
			plt.plot(self.data, **kwargs, label=label)
		else:
			plt.plot(self.data.loc[col], **kwargs, labe=label)
		plt.xlabel("Time")
		plt.ylabel("Sensor value (a.u.)")
		plt.title(label)
		return thisfigure

	def slice(self, start=None, end=None):
		if (start is not None) & (end is not None):
			return self.data.loc[start:end]
		elif (start is None) & (end is not None):
			return self.data.loc[:end]
		elif (start is not None) & (end is None):
			return self.data.loc[start:]
		else:
			return self.data