import os
import warnings

import numpy as np


def load_microphone(filename: str = 'Microphone.bin',
                    channels: int = 2,
                    root: str = ''
                    ) -> np.array:
    """Loads microphone waveform data from a file into a numpy array.

    Args:
        filename (str, optional): Input file name to target. Defaults to 'Microphone.bin'.
        channels (int, optional): Number of expected audio input channels. Defaults to 2.
        root (str, optional): Root path where filename is expected to be found. Defaults to ''.

    Returns:
        np.array: Array with raw waveform data from the microphone stream.
    """
    try:
        micdata = np.fromfile(os.path.join(root, filename), dtype='int16')\
            .reshape(-1, channels)
    except FileExistsError:
        warnings.warn(f'Microphone stream file {filename} could not be found.')
    except FileNotFoundError:
        warnings.warn(f'Microphone stream file {filename} could not be found.')
    return micdata
