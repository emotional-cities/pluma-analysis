import os
import warnings

import pandas as pd

from pluma.io.harp import _HARP_T0

_accelerometer_header = [
    'Orientation.X', 'Orientation.Y', 'Orientation.Z',
    'Gyroscope.X', 'Gyroscope.Y', 'Gyroscope.Z',
    'LinearAccl.X', 'LinearAccl.Y', 'LinearAccl.Z',
    'Magnetometer.X', 'Magnetometer.Y', 'Magnetometer.Z',
    'Accl.X', 'Accl.Y', 'Accl.Z',
    'Gravitiy.X', 'Gravitiy.Y', 'Gravitiy.Z',
    'SysCalibEnabled', 'GyroCalibEnabled',
    'AccCalibEnabled', 'MagCalibEnabled',
    'Temperature', 'Seconds', 'SoftwareTimestamp']


def load_accelerometer(
        filename: str = 'Accelerometer.csv',
        root: str = '') -> pd.DataFrame:

    """Loads the raw acceleromter data from file to a pandas DataFrame.

    Args:
        filename (str, optional): Input file name to target. Defaults to 'Accelerometer.csv'.
        root (str, optional): Root path where filename is expected to be found. Defaults to ''.

    Returns:
        pd.DataFrame: Dataframe with descriptive data indexed by time (Seconds)
    """
    path = os.path.join(root, filename)
    try:
        acc_df = pd.read_csv(
            path,
            header=None,
            names=_accelerometer_header)
    except FileNotFoundError:
        warnings.warn(f'Accelerometer stream file {path} could not be found.')
        return
    except FileExistsError:
        warnings.warn(f'Accelerometer stream file {path} could not be found.')
        return
    acc_df['Seconds'] = _HARP_T0 + pd.to_timedelta(acc_df['Seconds'].values, 's')
    acc_df['SoftwareTimestamp'] = \
        _HARP_T0 + pd.to_timedelta(acc_df['SoftwareTimestamp'].values, 's')
    acc_df.set_index('Seconds', inplace=True)
    return acc_df