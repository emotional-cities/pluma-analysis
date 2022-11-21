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
        filename: str = 'accelerometer.csv',
        root: str = '') -> pd.DataFrame:

    """Loads the raw acceleromter data from file to a pandas DataFrame.

    Args:
        filename (str, optional): Input file name to target. Defaults to 'accelerometer.csv'.
        root (str, optional): Root path where filename is expected to be found. Defaults to ''.

    Returns:
        pd.DataFrame: Dataframe with descriptive data indexed by time (Seconds)
    """
    try:
        df = pd.read_csv(
            os.path.join(root, filename),
            header=None,
            names=_accelerometer_header)
    except FileNotFoundError:
        warnings.warn(f'Accelerometer stream file\
            {filename} could not be found.')
        return
    except FileExistsError:
        warnings.warn(f'Accelerometer stream file\
            {filename} could not be found.')
        return
    df['Seconds'] = _HARP_T0 + pd.to_timedelta(df['Seconds'].values, 's')
    df['SoftwareTimestamp'] = \
        _HARP_T0 + pd.to_timedelta(df['SoftwareTimestamp'].values, 's')
    df.set_index('Seconds', inplace=True)
    return df