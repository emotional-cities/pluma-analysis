import struct
import warnings
import numpy as np

from typing import Union

import pandas as pd
from pluma.io.path_helper import ComplexPath, ensure_complexpath


def load_glia(filename: str,
              dtypes: list[chr],
              channel_names: list[str],
              root: Union[str, ComplexPath] = ''
              ) -> pd.DataFrame:

    path = ensure_complexpath(root)
    path.join(filename)

    df = pd.DataFrame(columns=channel_names)

    try:
        header = ''
        with path.open('rb') as stream:
            # we first need to find the header string for this glia stream
            decoded = ''
            while decoded != '\x00':
                header += decoded
                chunk = stream.read(struct.calcsize('1s'))
                decoded = chunk.decode()

        header_bytes = len(header)
        separator_bytes = 1
        data_bytes = sum([struct.calcsize(f) for f in dtypes])
        format_string = ''.join(dtypes)

        with path.open('rb') as stream:
            while True:
                header_chunk = stream.read(header_bytes + separator_bytes)
                header_string = header_chunk.decode('unicode-escape')
                chunk = stream.read(data_bytes)
                if not header_chunk:
                    break

                unpacked = list(struct.unpack(format_string, chunk))
                df.loc[len(df.index)] = unpacked
    except FileNotFoundError:
        warnings.warn(f'Microphone stream file\
                {path} could not be found.')
    except FileExistsError:
        warnings.warn(f'Microphone stream file\
                {path} could not be found.')

    return df