import datetime
import numpy as np
import pandas as pd
import geopandas as gpd

from typing import Union
from scipy.stats import circmean
from pluma.stream.georeference import Georeference


def resample_temporospatial(
    data: pd.DataFrame,
    georeference: Union[Georeference, pd.DataFrame],
    sampling_dt: datetime.timedelta = datetime.timedelta(seconds=2),
    aggregate_func=None,
) -> gpd.GeoDataFrame:
    """Temporally resamples a temporally indexed data stream and aligns it to a spatial reference.

    Args:
        data (pd.DataFrame): DataFrame with data index by time
        georeference (pd.DataFrame): a geoference, usually the output of Streams.ubxStream.UbxStream.parseposition, or equivalent.
        sampling_dt (datetime.timedelta, optional): _description_. Defaults to datetime.timedelta(seconds = 2).

    Raises:
        ValueError: Raises an error if the input DataFrame is empty.

    Returns:
        gpd.GeoDataFrame: Returns a resampled GeoDataFrame.
    """
    if data.empty:
        raise ValueError("Input dataframe is empty.")

    if isinstance(georeference, Georeference):
        georeference = georeference.spacetime

    if sampling_dt is None:
        resampled = georeference
    else:
        resampled = resample_georeference(georeference, sampling_dt)

    resampled_indices = resampled.index.searchsorted(data.index) - 1
    valid_data_values = resampled_indices >= 0
    resampled_data_index = resampled.index[resampled_indices[valid_data_values]]
    resampled_data = data[valid_data_values].groupby(resampled_data_index)

    if aggregate_func is None:
        resampled_data = resampled_data.mean()
    else:
        resampled_data = resampled_data.apply(aggregate_func)

    resampled_data = resampled_data.reindex(resampled.index)
    return gpd.GeoDataFrame(resampled_data, geometry=resampled.geometry)


def resample_temporospatial_circ(data, georeference, sampling_dt=datetime.timedelta(seconds=2)):
    return resample_temporospatial(data, georeference, sampling_dt, circular_mean)


def resample_georeference(georeference: pd.DataFrame, sampling_dt: datetime.timedelta) -> gpd.GeoDataFrame:
    georeference = georeference.loc[:, "Latitude":"Elevation"].resample(sampling_dt, origin="start").mean()
    geometry = gpd.points_from_xy(
        x=georeference["Longitude"],
        y=georeference["Latitude"],
        z=georeference["Elevation"],
    )
    gdf = gpd.GeoDataFrame(georeference, geometry=geometry)
    gdf.crs = "epsg:4326"
    return gdf


def circular_mean(x):
    return round(np.rad2deg(circmean(np.deg2rad(x))), 2)
