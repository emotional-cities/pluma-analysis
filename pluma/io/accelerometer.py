import warnings

import pandas as pd

from typing import Union
from pluma.io.harp import _HARP_T0
from pluma.io.path_helper import ComplexPath, ensure_complexpath

_accelerometer_header = [
    "Orientation_X",
    "Orientation_Y",
    "Orientation_Z",
    "Gyroscope_X",
    "Gyroscope_Y",
    "Gyroscope_Z",
    "LinearAccl_X",
    "LinearAccl_Y",
    "LinearAccl_Z",
    "Magnetometer_X",
    "Magnetometer_Y",
    "Magnetometer_Z",
    "Accl_X",
    "Accl_Y",
    "Accl_Z",
    "Gravity_X",
    "Gravity_Y",
    "Gravity_Z",
    "SysCalibEnabled",
    "GyroCalibEnabled",
    "AccCalibEnabled",
    "MagCalibEnabled",
    "Temperature",
    "Seconds",
    "SoftwareTimestamp",
]


def load_accelerometer(
    filename: str = "Accelerometer.csv", root: Union[str, ComplexPath] = ""
) -> pd.DataFrame:
    """Loads the raw accelerometer data from file to a pandas DataFrame.

    Args:
        filename (str, optional): Input file name to target. Defaults to 'Accelerometer.csv'.
        root (Union[str, ComplexPath], optional): Root path where filename is expected to be found. Defaults to ''.

    Returns:
        pd.DataFrame: Dataframe with descriptive data indexed by time (Seconds)
    """
    path = ensure_complexpath(root)
    path.join(filename)
    try:
        with path.open("rb") as stream:
            acc_df = pd.read_csv(stream, header=None, names=_accelerometer_header)
    except FileNotFoundError:
        warnings.warn(f"Accelerometer stream file {path} could not be found.")
        return
    except FileExistsError:
        warnings.warn(f"Accelerometer stream file {path} could not be found.")
        return

    acc_df["Seconds"] = _HARP_T0 + pd.to_timedelta(acc_df["Seconds"].values, "s")
    acc_df["SoftwareTimestamp"] = _HARP_T0 + pd.to_timedelta(acc_df["SoftwareTimestamp"].values, "s")
    acc_df.set_index("Seconds", inplace=True)
    return acc_df
