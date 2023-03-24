from __future__ import annotations
import warnings
import nepy

from typing import Union, List, Optional

from pluma.io.harp import _HARP_T0
from pluma.io.path_helper import ComplexPath, ensure_complexpath

from pluma.io._nepy.NedfReader import NedfReader


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
             ) -> NedfReader:
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
        NedfReader: returns the loaded file as a reader
        object from the nepy package.
    """

    root = ensure_complexpath(root)
    if filename is None:
        filename = get_eeg_file(root)
    else:
        root.join(filename)
        filename = root

    return NedfReader(filename, **kwargs)
