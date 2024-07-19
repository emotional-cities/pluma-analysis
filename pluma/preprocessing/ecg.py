import numpy as np
import pandas as pd
import heartpy as hp
from typing import Union
from pluma.stream import Stream

def heartrate_from_ecg(ecg : Union[Stream, pd.DataFrame],
                       sample_rate : float = 50,
                       skip_slice : int = 20,
                       bpmmax : float = 200.0,
                       highpass_cutoff : float = 5,
                       invert : bool = False,
                       bpm_method : str = 'heartpy') -> tuple:
    ## Load biodata
    """Calculates heart rate from the raw ECG waveform signal

    Args:
        ecg_data (Stream or DataFrame): ECG input data
        sample_rate (float, optional): ECG sampling rate (Hz). Defaults to 50.
        skip_slice (int, optional): How to slice the incoming raw array. Fs corresponds to the sampling rate post-slicing. Defaults to 4.
        bpmmax (float, optional): Maximum theoretical heartrate. Defaults to 200.0.
        highpass_cutoff (float, optional): Cutoff frequency of the high-pass filter (Hz). Defaults to 5.
        segment_width (int, optional): Segment window size (in seconds) over which to compute heartrate. Defaults to 5.
        invert (bool, optional): If True, it will invert the raw signal (i.e. Signal * -1 ). Defaults to False.

    Returns:
        tuple: Tuple with a DataFrame containing timestamped heartbeats, an array with
        the processed waveform signal, and the heartpy working_data and measures, respectively.
    """

    if isinstance(ecg, Stream):
        ecg = ecg.data

    if invert:
        ecg = ecg * (-1.0)

    # sensor acquires at 50hz but saves at 1khz
    ecg = ecg.Value0[::skip_slice].astype(np.float64)

    # high-pass filter seems to give consistently less rejected peaks than notch
    filtered = hp.filter_signal(ecg, cutoff=highpass_cutoff, sample_rate=sample_rate, filtertype='highpass')

    # find peaks and compute overall beat statistics
    working_data, measures = hp.process(ecg, sample_rate=sample_rate, bpmmax=bpmmax)
    
    if bpm_method == 'heartpy':
        heartrate = 60000 / np.array(working_data['RR_list_cor'])
        peak_index = np.array(working_data['RR_indices'])[:, 1] # align to end peak
        peak_mask = np.array(working_data['RR_masklist']) == 0
        peak_index = ecg.index[peak_index][peak_mask]
    elif bpm_method == 'rolling':
        peaklist = working_data['peaklist']
        peak_index = ecg.index[peaklist]
        ibi = peak_index.to_series().diff().dt.total_seconds()
        heartrate = 60 / ibi.rolling(window=pd.to_timedelta(60, 's')).mean()
    else:
        raise ValueError("The specified heartrate calculation method is not supported.")

    bpm = pd.DataFrame(index = peak_index, copy = True)
    bpm['Bpm'] = heartrate
    return (bpm, filtered, working_data, measures)