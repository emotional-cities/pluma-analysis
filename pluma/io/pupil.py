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
    sensor_id_path = ensure_complexpath(root)
    sensor_id_path.join(filename + '_Frame0.bin')
    data_header_path = ensure_complexpath(root)
    data_header_path.join(filename + '_Frame1.bin')
    data_path = ensure_complexpath(root)
    data_path.join(filename + '_Frame2.bin')

    try:
        sensor_id = np.fromfile(sensor_id_path.path, dtype=np.dtype(dtypes[0]))
        data_header = np.fromfile(data_header_path.path, dtype=np.dtype(dtypes[1]))
        data = np.fromfile(data_path.path, dtype=np.dtype(dtypes[2]))

        print(pd.DataFrame(data))
    except FileNotFoundError:
        warnings.warn(f'Pupil stream file could not be found.')
    except FileExistsError:
        warnings.warn(f'Pupil stream file could not be found.')

    return pd.DataFrame()