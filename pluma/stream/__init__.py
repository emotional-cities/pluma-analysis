from enum import Enum
import matplotlib.pyplot as plt
from typing import Union, Optional

from pluma.io.path_helper import ComplexPath
from pluma.sync import ClockReference, ClockRefId


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
              clockreference: ClockReference=ClockReference(referenceid=ClockRefId.NONE),
			  parent_dataset=None,
			  autoload: bool = True):
		"""_summary_
		Args:
			device (str): Device label
			streamlabel (str): Stream label
			root (Union[str, ComplexPath], optional): Root path where the files of the stream are expected to be found. Defaults to ''.
			data (any, optional): Data to initially populate the stream. Defaults to None.
   			autoload (bool, optional): If True, it will attempt to automatically load the data when instantiated. Defaults to True.
		"""

		self.device = device
		self.streamlabel = streamlabel
		self._rootfolder = self.rootfolder = root
		self.data = data
		self.clockreference = clockreference
		self.parent_dataset = parent_dataset
		self.autoload = autoload
		self.streamtype = StreamType.NONE

	@property
	def rootfolder(self):
		return self._rootfolder

	@rootfolder.setter
	def rootfolder(self, value: Union[str, ComplexPath]):
		self._rootfolder = value

	def load(self):
		raise NotImplementedError("load() method is not implemented for the Stream base class.")

	def resample(self):
		raise NotImplementedError("resample() method is not implemented for the Stream base class.")

	def reload(self):
		self.load()

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

	def convert_to_si(self, data=None):
		raise NotImplementedError("convert_to_si() method is not implemented for the Stream base class.")

	def export_to_csv(self):
		raise NotImplementedError("export_to_csv() method is not implemented for the Stream base class.")
