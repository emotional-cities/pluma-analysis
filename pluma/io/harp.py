import warnings
from datetime import datetime

import numpy as np
import pandas as pd

from pluma.io.path_helper import ComplexPath, ensure_complexpath
from typing import Sequence, Union

_HARP_T0 = datetime(1904, 1, 1)

_SECONDS_PER_TICK = 32e-6

_payloadtypes = {
    1: np.dtype(np.uint8),
    2: np.dtype(np.uint16),
    4: np.dtype(np.uint32),
    8: np.dtype(np.uint64),
    129: np.dtype(np.int8),
    130: np.dtype(np.int16),
    132: np.dtype(np.int32),
    136: np.dtype(np.int64),
    68: np.dtype(np.float32),
}


def to_datetime(seconds: Union[float, np.ndarray, Sequence[float]]) -> datetime:
    """Convert harp timestamp to datetime.

    Parameters
    ----------
    seconds: scalar or ndarray or list-like
        The harp timestamp data to be converted to datetime.

    Returns
    -------
    datetime:
        Return type depends on input.
          - scalar: datetime value
          - list-like: DatetimeIndex
    """
    return _HARP_T0 + pd.to_timedelta(seconds, "s")


def to_harptime(
    datetime: Union[datetime, np.ndarray, pd.DatetimeIndex],
) -> Union[float, np.ndarray, pd.TimedeltaIndex]:
    """Convert datetime to harp timestamp.

    Parameters
    ----------
    datetime: datetime or ndarray or list-like
        The datetime data to be converted to harp timestamp.

    Returns
    -------
    float or ndarray:
        Return type depends on input.
          - scalar: float harp timestamp in seconds
          - ndarray: ndarray of float timestamps
          - DatetimeIndex: harp timestamps in TimedeltaIndex
    """
    return (datetime - np.datetime64(_HARP_T0)) / np.timedelta64(1, "s")


def read_harp_bin(file: Union[str, ComplexPath], time_offset: float = 0) -> pd.DataFrame:
    """Reads data from the specified Harp binary file. \
        Expects a stable message format.

    Parameters
    ----------
        file: str or ComplexPath
            Input file name to target.
        time_offset: float
            Time offset to add to the harp timestamp. Defaults to 0.

    Returns
    -------
        DataFrame
            Dataframe with data stream indexed by time
    """
    path = ensure_complexpath(file)
    try:
        with path.open("rb") as stream:
            data = np.frombuffer(stream.read(), dtype=np.uint8)
    except FileNotFoundError:
        warnings.warn(f"Harp stream file {path} could not be found.")
        return pd.DataFrame()
    except FileExistsError:
        warnings.warn(f"Harp stream file {path} could not be found.")
        return pd.DataFrame()
    if len(data) == 0:
        return None

    stride = int(data[1] + 2)
    length = len(data) // stride
    payloadsize = stride - 12
    payloadtype = _payloadtypes[data[4] & ~np.uint8(0x10)]
    elementsize = payloadtype.itemsize
    payloadshape = (length, payloadsize // elementsize)
    seconds = np.ndarray(length, dtype=np.uint32, buffer=data, offset=5, strides=stride)
    ticks = np.ndarray(length, dtype=np.uint16, buffer=data, offset=9, strides=stride)

    seconds = ticks * _SECONDS_PER_TICK + seconds
    seconds += time_offset
    timestamp = to_datetime(seconds)
    timestamp.name = "Timestamp"

    payload = np.ndarray(
        payloadshape,
        dtype=payloadtype,
        buffer=data,
        offset=11,
        strides=(stride, elementsize),
    )

    if payload.shape[1] == 1:
        return pd.DataFrame(payload, index=timestamp, columns=["Value"])

    else:
        return pd.DataFrame(
            payload,
            index=timestamp,
            columns=["Value" + str(x) for x in np.arange(payload.shape[1])],
        )


def load_harp_stream(
    streamID: int,
    root: Union[str, ComplexPath] = "",
    suffix: str = "Streams_",
    ext: str = "",
) -> pd.DataFrame:
    """Helper function that runs assembles the expected path to the\
        binary harp file.

    Parameters
    ----------
        streamID: int
            Integer ID of the harp stream (aka address).
        root: str or ComplexPath
            Root path where filename is expected to be found. Defaults to ''.
        suffix: str
            Expected file suffix. Defaults to 'Streams_'.
        ext: str
            Expected file extension. Defaults to ''.

    Returns
    -------
        DataFrame
            Dataframe with data stream indexed by time
    """
    path = ensure_complexpath(root)
    path.join(f"{suffix}{streamID}{ext}")
    return read_harp_bin(path)
