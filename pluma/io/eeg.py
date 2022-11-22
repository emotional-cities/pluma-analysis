import os
import warnings

import pandas as pd

from nepy import easyReader, nedfReader

from pluma.io.harp import _HARP_T0

_eeg_header = []


def load_eeg(
        filename: str = 'todo.csv',
        root: str = '') -> pd.DataFrame:

    try:
        df = pd.read_csv(
            os.path.join(root, filename),
            header=None,
            names=_eeg_header)
    except FileNotFoundError:
        warnings.warn(f'Eeg stream file\
            {filename} could not be found.')
        return
    except FileExistsError:
        warnings.warn(f'Eeg stream file\
            {filename} could not be found.')
        return
    df['Seconds'] = _HARP_T0 + pd.to_timedelta(df['Seconds'].values, 's')
    df['SoftwareTimestamp'] = \
        _HARP_T0 + pd.to_timedelta(df['SoftwareTimestamp'].values, 's')
    df.set_index('Seconds', inplace=True)
    return df