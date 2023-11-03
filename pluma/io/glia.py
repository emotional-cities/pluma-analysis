import struct
import warnings
import numpy as np

from typing import Union

import pandas as pd
from pluma.io.path_helper import ComplexPath, ensure_complexpath


def load_glia(filename: str,
              dtypes: list[list[chr]],
              channel_names: list[list[str]],
              root: Union[str, ComplexPath] = ''
              ) -> pd.DataFrame:

    path = ensure_complexpath(root)
    path.join(filename+'_Frame1.bin')

    df_timestamps = pd.DataFrame(columns=channel_names[0])
    df_data = pd.DataFrame(columns=channel_names[1])

    try:
        # unpack timestamps
        data_bytes = sum([struct.calcsize(f) for f in dtypes[0]])
        format_string = ''.join(dtypes[0])
        with path.open('rb') as stream:
            while True:
                chunk = stream.read(data_bytes)
                if not chunk:
                    break

                unpacked = list(struct.unpack(format_string, chunk))
                df_timestamps.loc[len(df_timestamps.index)] = unpacked

        # unpack data
        path = ensure_complexpath(root)
        path.join(filename + '_Frame2.bin')
        data_bytes = sum([struct.calcsize(f) for f in dtypes[1]])
        format_string = ''.join(dtypes[1])
        with path.open('rb') as stream:
            while True:
                chunk = stream.read(data_bytes)
                if not chunk:
                    break

                unpacked = list(struct.unpack(format_string, chunk))
                df_data.loc[len(df_data.index)] = unpacked
    except FileNotFoundError:
        warnings.warn(f'Glia stream file\
                {path} could not be found.')
    except FileExistsError:
        warnings.warn(f'Glia stream file\
                {path} could not be found.')

    return pd.concat([df_timestamps, df_data], axis=1)

