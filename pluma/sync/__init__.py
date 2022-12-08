import pandas as pd
from enum import Enum
from typing import Callable, Union
from sklearn.linear_model import LinearRegression



class ClockRefId(Enum):
	NONE = None
	GNSS = 'gnss'
	HARP = 'harp'
	CPU = 'cpu'


class ClockReferencering:
	"""Abstract class that allows synchronization across Streams
	"""

	def __init__(self,
              referenceid: ClockRefId = ClockRefId.NONE):

		self._clockreference = referenceid  # Tracks the reference clock
		self._clockreference_history = []
		self._conversion_model = None

	@property
	def reference(self):
		return self._clockreference

	@reference.setter
	def reference(self, value: ClockRefId):
		if not(value == self._clockreference):
			self._clockreference = value
			self._clockreference_history.append(value)

	@property
	def conversion_model(self):
		return self._conversion_model

	@conversion_model.setter
	def conversion_model(self, value: Union[Callable, LinearRegression]):
		if isinstance(value, LinearRegression):
			self._conversion_model = value.predict
		else:
			self._conversion_model = value

	def rereference_time(self, timearray):
		"""Takes the index column in the dataframe and applies a correction model.

		Returns:
			_type_: _description_
		"""
		conversion_fun = self.conversion_model
		if conversion_fun is None:
			raise ValueError("No valid model was instantiated.")
		return conversion_fun(timearray)