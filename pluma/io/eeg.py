from __future__ import annotations
import warnings
import nepy
import pandas as pd
import numpy as np

from typing import Union, List, Optional, Tuple
from sklearn.linear_model import LinearRegression

from pluma.io.harp import _HARP_T0
from pluma.io.path_helper import ComplexPath, ensure_complexpath

from pluma.io._nepy.NedfReader import NedfReader
from pluma.stream.harp import HarpStream


def get_eeg_file(root: Union[str, ComplexPath] = '',
                 if_multiple_load_index: int = -1) -> List[str]:
    """Lists all Empatica files in the root folder.
    If multiple sessions are found, throws a warning and loads
    if_multiple_load_index nth session."""

    root = ensure_complexpath(root)
    filename = root
    filename.join("*.nedf")

    expected_files = filename.glob(filename.path)
    if len(expected_files) == 0:
        raise FileNotFoundError(f"No *.nedf files found in {root}.")
    elif len(expected_files) > 1:
        warnings.warn(f"Multiple *.nedf files found in {root}. "
                      f"Loading {expected_files[if_multiple_load_index]}.")
        ret = expected_files[if_multiple_load_index]
    else:
        ret = expected_files[0]

    return ret


def load_eeg(filename: Optional[str] = None,
             root: Union[str, ComplexPath] = '',
             **kwargs
             ) -> Tuple[NedfReader, pd.DataFrame]:
    """_summary_
    Args:
        filename (Optional[str], optional): The name of the file to be loaded.
        Defaults to None. If None, an automatic routine will be attempted to
        find the file.
        root (Union[str, ComplexPath], optional): _description_. Defaults to ''.
        Defaults to 'nedf'. Also determines the return type of the function.

    Raises:
        ValueError: Wrong file_extension was given. Must be .nedf.
    Returns:
        Tuple[NedfReader, pd.DataFrame]: where:

        - NedfReader: returns the loaded file as a reader
        object from the nepy package.
        - pd.DataFrame: returns a dataframe with the server lsl markers
    """

    root = ensure_complexpath(root)
    if filename is None:
        filename = get_eeg_file(root)
    else:
        root.join(filename)
        filename = root

    _out = NedfReader(filename, **kwargs)
    _server_lsl_markers = load_server_lsl_markers(root=root)
    _server_lsl_markers["EegSample"] = -1
    _server_lsl_markers["EegTimestamp"] = np.nan

    _server_lsl_markers["EegSample"] = [
        (np.where(_out.np_markers == marker)[0][0])\
            if marker in _out.np_markers else -1\
                for marker in _server_lsl_markers["MarkerIdx"].values
                ]
    _server_lsl_markers["EegTimestamp"] = [
        _out.np_time[sample] if sample != -1 else np.nan\
            for sample in _server_lsl_markers["EegSample"].values]

    return (_out, _server_lsl_markers)


def load_server_lsl_markers(
        filename: str = "eeg_markers.csv",
        root: Union[str, ComplexPath] = '') -> pd.DataFrame:

    path = ensure_complexpath(root)
    path.join(filename)
    try:
        with path.open('rb') as stream:
            df = pd.read_csv(stream,
                             names=['Seconds', 'LslTimestamp', 'MarkerIdx'],
                             delimiter=',', header=None, skiprows=1)
    except FileNotFoundError:
        print(f'Eeg server lsl tags file  {filename} could not be found.')
    except FileExistsError:
        print(f'Eeg server lsl tags file {filename} could not be found.')

    df['Seconds'] = _HARP_T0 + pd.to_timedelta(
            df['Seconds'].values, 's')
    return df


def synchronize_eeg_to_harp(
        server_lsl_markers: pd.DataFrame,
        min_q_r2: float = 0.999
        ) -> LinearRegression:

    valid_samples = \
        pd.notna(server_lsl_markers["EegTimestamp"].values)\
        & pd.notna(server_lsl_markers["Seconds"].values)
    raw_harp_time = HarpStream.to_seconds(server_lsl_markers["Seconds"].values)
    eeg_time = server_lsl_markers["EegTimestamp"].values
    eeg_time = eeg_time.reshape(-1, 1)
    raw_harp_time = raw_harp_time.reshape(-1, 1)

    model = LinearRegression(fit_intercept=True).fit(
        eeg_time[valid_samples], raw_harp_time[valid_samples, :])
    r2 = model.score(
        eeg_time[valid_samples], raw_harp_time[valid_samples, :])
    if r2 < min_q_r2:
        raise AssertionError(
            f"The quality of the linear fit is lower than expected {r2}")
    else:
        return model