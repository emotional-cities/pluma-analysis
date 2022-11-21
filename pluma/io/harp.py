import os
import warnings
import datetime

import numpy as np
import pandas as pd

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
    68: np.dtype(np.float32)
}


def read_harp_bin(file: str, time_offset: float = 0) -> pd.DataFrame:
    """Reads data from the specified Harp binary file. Ideally, from a single address and stable format.
    Args:
        file (str): Input file name to target.
        time_offset (float, optional): time offset to add to the harp timestamp. Defaults to 0.

    Returns:
        pd.DataFrame: Dataframe with address data indexed by time (Seconds)
    """
    data = np.fromfile(file, dtype=np.uint8)

    if len(data) == 0:
        return None

    stride = data[1] + 2
    length = len(data) // stride
    payloadsize = stride - 12
    payloadtype = _payloadtypes[data[4] & ~0x10]
    elementsize = payloadtype.itemsize
    payloadshape = (length, payloadsize // elementsize)
    seconds = np.ndarray(length, dtype=np.uint32,
                         buffer=data, offset=5, strides=stride)
    ticks = np.ndarray(length, dtype=np.uint16,
                       buffer=data, offset=9, strides=stride)

    seconds = ticks * _SECONDS_PER_TICK + seconds
    seconds += time_offset
    seconds = _HARP_T0 + pd.to_timedelta(seconds, 's')
    seconds.name = 'Seconds'

    payload = np.ndarray(
        payloadshape,
        dtype=payloadtype,
        buffer=data, offset=11,
        strides=(stride, elementsize))

    if payload.shape[1] == 1:
        return pd.DataFrame(
            payload,
            index=seconds,
            columns=['Value'])

    else:
        return pd.DataFrame(
            payload,
            index=seconds,
            columns=['Value' + str(x) for x in np.arange(payload.shape[1])])


def get_stream_path(streamID: int,
                    root: str = '', suffix: str = 'Streams_', ext: str = '') -> str:
    """Helper function to generate a full path of the harp stream binary file.

    Args:
        streamID (int): Integer ID of the harp stream (aka address).
        root (str, optional): Root path where filename is expected to be found. Defaults to ''.
        suffix (str, optional): Suffix of the binary file name. Defaults to 'Streams_'.
        ext (str, optional): Extension. Defaults to ''.

    Returns:
        str: The absolute path of the binary file
    """
    _suffix = f'{suffix}{streamID}{ext}'
    return os.path.join(root, _suffix)


def load_harp_stream(streamID: int,
                     root: str = '',
                     throwFileError: bool = True) -> pd.DataFrame:
    """Helper function that runs read_harp_bin() with arguments built using get_stream_path()

    Args:
        streamID (int): Integer ID of the harp stream (aka address).
        root (str, optional): Root path where filename is expected to be found. Defaults to ''.
        throwFileError (bool, optional): Default behavior if a file is not found. Defaults to True.

    Raises:
        FileExistsError: Error if a binary file is not found.

    Returns:
        pd.DataFrame: Dataframe with address data indexed by time (Seconds)
    """

    path = get_stream_path(streamID, root)
    if os.path.isfile(path):
        data = read_harp_bin(path)
        return data
    else:
        if throwFileError:
            raise FileExistsError
        else:
            warnings.warn(f'Harp stream with Id {streamID} not found')
            return pd.DataFrame()

