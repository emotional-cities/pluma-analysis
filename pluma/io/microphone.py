import warnings
import numpy as np

from typing import Union
from pluma.io.path_helper import ComplexPath, ensure_complexpath


def load_microphone(
    filename: str = "Microphone.bin",
    channels: int = 2,
    root: Union[str, ComplexPath] = "",
    dtype=np.int16,
) -> np.array:
    """Loads microphone waveform data from a file into a numpy array.

    Args:
        filename (str, optional): Input file name to target. Defaults to 'Microphone.bin'.
        channels (int, optional): Number of expected audio input channels. Defaults to 2.
        root (Union[str, ComplexPath], optional): Root path\
            where filename is expected to be found. Defaults to ''.
        dtype (_type_, optional): Data type of the binary file. Defaults to np.int16.

    Returns:
        np.array: Array with raw waveform data from the microphone stream.
    """

    path = ensure_complexpath(root)
    path.join(filename)

    try:
        with path.open("rb") as stream:
            micdata = np.frombuffer(stream.read(), dtype=dtype)
            micdata = micdata.reshape((-1, channels))
    except FileNotFoundError:
        warnings.warn(f"Microphone stream file {path} could not be found.")
    except FileExistsError:
        warnings.warn(f"Microphone stream file {path} could not be found.")
    return micdata
