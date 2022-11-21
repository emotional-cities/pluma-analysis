import datetime
import numpy as np
import pandas as pd

from scipy.stats import circmean


def resample_temporospatial(input_data: pd.DataFrame,
                            georeference: pd.DataFrame,
                            sampling_dt:
                                datetime.timedelta
                                = datetime.timedelta(seconds=2))\
                                    -> pd.DataFrame:
    """Temporally resamples a temporally indexed data stream and aligns it to a spatial reference.

    Args:
        input_data (pd.DataFrame): DataFrame with data index by time
        georeference (pd.DataFrame): a geoference, usually the output of Streams.ubxStream.UbxStream.parseposition, or equivalent.
        sampling_dt (datetime.timedelta, optional): _description_. Defaults to datetime.timedelta(seconds = 2).

    Raises:
        ValueError: Raises an error if the input DataFrame is empty.

    Returns:
        pd.DataFrame: Returns a resampled DataFrame.
    """
    if input_data.empty:
        raise ValueError("Input dataframe is empty.")

    resampled = georeference.spacetime.loc\
        [:, "Latitude":"Elevation"].resample(
            sampling_dt, origin='start').mean()
    resampled['Data'] = np.NAN
    for i in np.arange(len(resampled)-1):
        resampled['Data'].iloc[i] = (input_data[
            (input_data.index >= resampled.index[i]) &
            (input_data.index < resampled.index[i+1])]).mean()
    resampled['Data'].iloc[i+1] = (
        input_data[input_data.index >= resampled.index[i+1]]).mean()
    return resampled


def resample_temporospatial_circ(input_data,
                                 georeference,
                                 sampling_dt=datetime.timedelta(seconds=2)):
    resampled = georeference.spacetime.loc[:, "Latitude":"Elevation"].\
        resample(sampling_dt, origin='start').mean()
    resampled['Data'] = np.NAN
    for i in np.arange(len(resampled)-1):
        resampled['Data'].iloc[i] = circular_mean((input_data[
            (input_data.index >= resampled.index[i]) &
            (input_data.index < resampled.index[i+1])]))
    resampled['Data'].iloc[i+1] = circular_mean(
        input_data[input_data.index >= resampled.index[i+1]]
        )
    return resampled


def circular_mean(x):
    return round(np.rad2deg(circmean(np.deg2rad(x))), 2)
