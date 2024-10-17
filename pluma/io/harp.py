import warnings
import datetime

import numpy as np
import pandas as pd

from pluma.io.path_helper import ComplexPath, ensure_complexpath
from typing import Union

_HARP_T0 = datetime.datetime(1904, 1, 1)

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


def read_harp_bin(file: Union[str, ComplexPath], time_offset: float = 0) -> pd.DataFrame:
    """Reads data from the specified Harp binary file. \
        Expects a stable message format.

    Args:
        file (Union[str, ComplexPath]): Input file name to target.
        time_offset (float, optional): Time offset to add to the harp timestamp. Defaults to 0.

    Returns:
        pd.DataFrame: Dataframe with data stream indexed by time (Seconds)
    """
    path = ensure_complexpath(file)
    try:
        with path.open("rb") as stream:
            data = np.frombuffer(stream.read(), dtype=np.uint8)
    except FileNotFoundError:
        warnings.warn(f"Harp stream file\
            {path} could not be found.")
        return pd.DataFrame()
    except FileExistsError:
        warnings.warn(f"Harp stream file\
            {path} could not be found.")
        return pd.DataFrame()
    if len(data) == 0:
        return None

    stride = data[1] + 2
    length = len(data) // stride
    payloadsize = stride - 12
    payloadtype = _payloadtypes[data[4] & ~0x10]
    elementsize = payloadtype.itemsize
    payloadshape = (length, payloadsize // elementsize)
    seconds = np.ndarray(length, dtype=np.uint32, buffer=data, offset=5, strides=stride)
    ticks = np.ndarray(length, dtype=np.uint16, buffer=data, offset=9, strides=stride)

    seconds = ticks * _SECONDS_PER_TICK + seconds
    seconds += time_offset
    seconds = _HARP_T0 + pd.to_timedelta(seconds, "s")
    seconds.name = "Seconds"

    payload = np.ndarray(
        payloadshape,
        dtype=payloadtype,
        buffer=data,
        offset=11,
        strides=(stride, elementsize),
    )

    if payload.shape[1] == 1:
        return pd.DataFrame(payload, index=seconds, columns=["Value"])

    else:
        return pd.DataFrame(
            payload,
            index=seconds,
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

    Args:
        streamID (int): Integer ID of the harp stream (aka address).
        root (Union[str, ComplexPath], optional): Root path where \
            filename is expected to be found. Defaults to ''.
        suffix (str, optional): Expected file suffix. Defaults to 'Streams_'.
        ext (str, optional): Expected file extension Defaults to ''.

    Returns:
        pd.DataFrame: Dataframe with data stream indexed by time (Seconds)
    """
    path = ensure_complexpath(root)
    path.join(f"{suffix}{streamID}{ext}")
    return read_harp_bin(path)
