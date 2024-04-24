import struct
import warnings
import numpy as np

from typing import Union

import pandas as pd
import os
from pluma.io.path_helper import ComplexPath, ensure_complexpath


def load_pupil(filename: str,
               frame0: list[tuple[str, type]],
               frame1: list[tuple[str, type]],
               frame2: list[tuple[str, type]],
               root: Union[str, ComplexPath] = '') -> pd.DataFrame:
    """Reads data from the specified Pupil binary file set. \
        Assumes data frames have uniform length / data type.

    Args:
        filename (str): Input base file name to target.
        root (Union[str, ComplexPath]): Base data location.
        frame0 (tuple[str, type], optional): Channel name and expected type of first frame of a pupil message. In NDSI spec should be a string of length 36
        frame1 (list[tuple[str, type]], optional): List of channel names and expected types for frame 1, which should contain the data header. 
        frame2 (list[tuple[str, type]], optional): List of channel names and expected types for frame 2, which should contain the raw data. Set to None for variable length data types.

    Returns:
        pd.DataFrame: Dataframe with pupil stream.
    """
    sensor_id_path = ensure_complexpath(root)
    sensor_id_path.join(filename + '_Frame0.bin')
    data_header_path = ensure_complexpath(root)
    data_header_path.join(filename + '_Frame1.bin')
    data_path = ensure_complexpath(root)
    data_path.join(filename + '_Frame2.bin')

    try:
        sensor_id_df = pd.DataFrame(np.fromfile(sensor_id_path.path, dtype=np.dtype(frame0)))
        data_header_df = pd.DataFrame(np.fromfile(data_header_path.path, dtype=np.dtype(frame1)))

        data_df = None
        if frame2 is not None:
            data_df = pd.DataFrame(np.fromfile(data_path.path, dtype=np.dtype(frame2)))
    except FileNotFoundError:
        warnings.warn(f'Pupil stream file could not be found.')
    except FileExistsError:
        warnings.warn(f'Pupil stream file could not be found.')

    if data_df is not None:
        return pd.concat([sensor_id_df, data_header_df, data_df], axis=1)
    else:
        return pd.concat([sensor_id_df, data_header_df], axis=1)