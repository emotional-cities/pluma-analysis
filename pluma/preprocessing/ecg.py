import numpy as np
import pandas as pd

from scipy import signal

from pluma.preprocessing import utils

def heartrate_from_ecg(ecg_data_stream,
                       fs : float = 250, skip_slice : int = 4, max_heartrate_bpm : float = 200.0,
                       peak_height : float = 800, smooth_win : int = 10, invert : bool = False) -> tuple:
    ## Load biodata
    """Calculates heart rate from the raw ECG waveform signal

    Args:
        ecg_data_stream (_type_): ECG input data
        fs (float, optional): ECG sampling rate (Hz). Defaults to 250.
        skip_slice (int, optional): How to slice the incoming raw array. Fs corresponds to the sampling rate post-slicing. Defaults to 4.
        max_heartrate_bpm (float, optional): Maximum theoretical heartrate. Defaults to 200.0.
        peak_height (float, optional): Height of ECG peaks. Defaults to 800.
        smooth_win (int, optional): Smoothing window size (in samples) used to convolve the data. Defaults to 10.
        invert (bool, optional): If True, it will invert the raw signal (i.e. Signal * -1 ). Defaults to False.

    Returns:
        tuple: Tuple with a DataFrame containing timestamped heartbeats, and an array with the processed waveform signal, respectively.
    """
    ecg = ecg_data_stream.data
    if invert:
        ecg = ecg * (-1.0)
    ecg = ecg["Value0"].iloc[np.arange(len(ecg))[::skip_slice]].astype(np.float64) # sensor acquires at 250hz but saves at 1khz

    resampled = utils.butter_highpass_filter(ecg,5,fs)

    #Assume maximum heartrate of max_heartrate_bpm
    peaks, _  = signal.find_peaks(resampled, height = peak_height, distance = (1.0/(max_heartrate_bpm/60.0)) * fs )
    heartrate = (fs/np.diff(peaks)) * 60
    heartrate = np.convolve(heartrate, np.ones(smooth_win), 'same') / smooth_win
    heartrate[0:int(smooth_win/2)+1] = np.NaN # pad the invalid portion of the conv with NaN
    heartrate[-int(smooth_win/2)-1:-1] = np.NaN
    df = pd.DataFrame(index = ecg.index[peaks[1:]], copy = True)
    df['HeartRate'] = heartrate
    return (df, resampled)