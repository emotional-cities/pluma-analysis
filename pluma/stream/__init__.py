from enum import Enum
import matplotlib.pyplot as plt

class StreamType(Enum):
	NONE = None
	UBX = 'UbxStream'
	HARP = 'HarpStream'
	ACCELEROMETER = 'AccelerometerStream'
	MICROPHONE = 'MicrophoneStream'
	EMPATICA = 'EmpaticaStream'


class Stream:
	"""Based class for all stream types
	"""
	def __init__(self, device : str, streamlabel : str, root = '', data : any = None, autoload : bool = True):
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
		self.rootfolder = root
		self.data = data
		self.autoload = autoload
		self.streamtype = StreamType.NONE

	def plot(self, col = None , **kwargs):
		if self.data.empty:
			raise ValueError("Input dataframe is empty.")
		thisfigure = plt.figure()
		label = self.device + "." + self.streamlabel
		if col is None:
			plt.plot(self.data, **kwargs, label = label)
		else:
			plt.plot(self.data.loc[col], **kwargs, label = label)
		plt.xlabel("Time")
		plt.ylabel("Sensor value (a.u.)")
		plt.title(label)
		return thisfigure

	def slice(self, start = None, end = None):
		if (start is not None) & (end is not None):
			return self.data.loc[start:end]
		elif (start is None) & (end is not None):
			return self.data.loc[:end]
		elif (start is not None) & (end is None):
			return self.data.loc[start:]
		else:
			return self.data