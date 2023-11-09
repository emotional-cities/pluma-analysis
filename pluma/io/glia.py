import struct
import warnings
import numpy as np

from typing import Union

import pandas as pd
import os
from pluma.io.path_helper import ComplexPath


def load_glia(filename: str,
              dtypes: list[list[tuple[str, type]]],
              root: Union[str, ComplexPath] = ''
              ) -> pd.DataFrame:
    path = os.path.join(root._path, filename+'_Frame1.bin')

    df_timestamps = pd.DataFrame(columns=[chan[0] for chan in dtypes[0]])
    df_data = pd.DataFrame(columns=[chan[0] for chan in dtypes[1]])

    try:
        # unpack timestamps
        t_data = np.fromfile(path, dtype=np.dtype(dtypes[0]))
        df_timestamps = pd.DataFrame(t_data)

        # unpack data
        path = os.path.join(root._path, filename + '_Frame2.bin')
        d_data = np.fromfile(path, dtype=np.dtype(dtypes[1]))
        df_data = pd.DataFrame(d_data)
    except FileNotFoundError:
        warnings.warn(f'Glia stream file\
                {path} could not be found.')
    except FileExistsError:
        warnings.warn(f'Glia stream file\
                {path} could not be found.')

    return pd.concat([df_timestamps, df_data], axis=1)

