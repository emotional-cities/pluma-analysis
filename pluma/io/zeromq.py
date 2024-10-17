import warnings
import numpy as np

from typing import Union

import pandas as pd
from pluma.io.path_helper import ComplexPath, ensure_complexpath


def load_zeromq(filenames: list[str],
                dtypes: list[tuple[str, type]],
                root: Union[str, ComplexPath] = '') -> pd.DataFrame:
    
    assert len(filenames) == len(dtypes), "Length of filename and dtypes must be the same."

    try:
        data_frames = []
        for i, f in enumerate(filenames):
            if dtypes[i] is None:
                continue

            path = ensure_complexpath(root)
            path.join(f)

            data_frames.append(pd.DataFrame(np.fromfile(path.path, dtype=np.dtype(dtypes[i]))))
    except FileNotFoundError:
        warnings.warn(f'Stream file\
                {path} could not be found.')
    except FileExistsError:
        warnings.warn(f'Stream file\
                {path} could not be found.')
        
    return pd.concat(data_frames, axis=1)
        
