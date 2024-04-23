import struct
import warnings
import numpy as np

from typing import Union

import pandas as pd
import os
from pluma.io.path_helper import ComplexPath, ensure_complexpath


def load_pupil(filename: str,
               dtypes: list[list[tuple[str, type]]],
               root: Union[str, ComplexPath] = '') -> pd.DataFrame:
    """Reads data from the specified Pupil binary file set. \
        Assumes data frames have uniform length / data type.

    Args:
        filename (str): Input base file name to target.
        dtypes (list[list[tuple[str, type]]]): List of data types for each frame. Outer list is usually length 3 (for each NetMQ frame). Each inner list contains tuple of channel name and data type.
        root (Union[str, ComplexPath]): Base data location.

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
        sensor_id_df = pd.DataFrame(np.fromfile(sensor_id_path.path, dtype=np.dtype(dtypes[0])))
        data_header_df = pd.DataFrame(np.fromfile(data_header_path.path, dtype=np.dtype(dtypes[1])))

        data_df = None
        if len(dtypes) > 2:
            data_df = pd.DataFrame(np.fromfile(data_path.path, dtype=np.dtype(dtypes[2])))
    except FileNotFoundError:
        warnings.warn(f'Pupil stream file could not be found.')
    except FileExistsError:
        warnings.warn(f'Pupil stream file could not be found.')

    if data_df is not None:
        print(pd.concat([sensor_id_df, data_header_df, data_df], axis=1))
        return pd.concat([sensor_id_df, data_header_df, data_df], axis=1)
    else:
        print(pd.concat([sensor_id_df, data_header_df], axis=1))
        return pd.concat([sensor_id_df, data_header_df], axis=1)