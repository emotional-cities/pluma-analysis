## Export streams to csv
from __future__ import annotations
import os
import datetime
import pandas as pd
import geopandas as gpd

from typing import Union, Optional, Callable, Dict

from pluma.stream import Stream, StreamType

import pluma.preprocessing.resampling as resampling

def export_stream_to_csv(stream: Stream, export_path: str,
                         resampling_function: Callable = resampling.resample_temporospatial,
                         resampling_function_kws: Optional[Dict] = None,
                         ):

    """Export a stream to a csv file."""

    if hasattr(stream, "parent_dataset") is False:
        raise AttributeError("The stream does not have a valid parent Dataset.")
    if stream.parent_dataset is None:
        raise ValueError("The stream does not have a valid parent Dataset.")
    if stream.parent_dataset.has_calibration is False:
        raise ValueError(
            "The stream's parent Dataset does not have a valid calibration.\
                Calibrate the Dataset before exporting the stream by\
                    calling Dataset.add_georeference_and_calibrate()")

    georef = stream.parent_dataset.georeference

    if (stream.streamtype == StreamType.HARP):
        if resampling_function_kws is None:
            resampling_function_kws = {
                "sampling_dt": datetime.timedelta(seconds=1)
                }
        export_uniform_table_stream(
            stream=stream,
            georeference=georef,
            outdir=export_path,
            resampling_function=resampling_function,
            resampling_function_kws=resampling_function_kws)
    else:
        raise NotImplementedError(f"Export of stream type\
                                  {type(stream)} is not yet supported.")


def export_uniform_table_stream(stream: Stream,
                                georeference: pd.DataFrame,
                                outdir: str,
                                resampling_function: Callable[[pd.DataFrame, pd.DataFrame], pd.DataFrame],
                                resampling_function_kws: Dict = None):

    outdir = os.path.join(outdir, stream.device)
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
    resampled = resampling_function(stream.data,
                                    georeference,
                                    **resampling_function_kws)
    resampled.to_csv(f"{outdir}\\{stream.streamlabel}.csv", date_format='%Y-%m-%dT%H:%M:%S.%fZ')


def resample_stream_harp(stream: Stream,
                         sampling_dt: datetime.timedelta = datetime.timedelta(seconds=2),
                         sampler: Callable = resampling.resample_temporospatial) -> gpd.GeoDataFrame:
    check_stream_data_integrity(stream)
    return sampler(stream.data, _get_resampled_georef(stream, sampling_dt), sampling_dt=None)


def resample_stream_accelerometer(stream: Stream,
                                  sampling_dt: Union[pd.DataFrame, datetime.timedelta]
                                  ) -> gpd.GeoDataFrame:
    check_stream_data_integrity(stream)
    col_sampler = {
        'Orientation_X': resampling.resample_temporospatial_circ,
        'Orientation_Y': resampling.resample_temporospatial_circ,
        'Orientation_Z': resampling.resample_temporospatial_circ,
        'Gyroscope_X': resampling.resample_temporospatial,
        'Gyroscope_Y': resampling.resample_temporospatial,
        'Gyroscope_Z': resampling.resample_temporospatial,
        'LinearAccl_X': resampling.resample_temporospatial,
        'LinearAccl_Y': resampling.resample_temporospatial,
        'LinearAccl_Z': resampling.resample_temporospatial,
        'Magnetometer_X': resampling.resample_temporospatial,
        'Magnetometer_Y': resampling.resample_temporospatial,
        'Magnetometer_Z': resampling.resample_temporospatial,
        'Accl_X': resampling.resample_temporospatial,
        'Accl_Y': resampling.resample_temporospatial,
        'Accl_Z': resampling.resample_temporospatial,
        'Gravity_X': resampling.resample_temporospatial,
        'Gravity_Y': resampling.resample_temporospatial,
        'Gravity_Z': resampling.resample_temporospatial}
    return _resample_multistream(stream, col_sampler, sampling_dt)


def resample_stream_empatica(stream: Stream,
                             sampling_dt: datetime.timedelta = datetime.timedelta(seconds=2)
                             ) -> gpd.GeoDataFrame:
    col_sampler = {
        'E4_Gsr': resampling.resample_temporospatial,
        'E4_Hr': resampling.resample_temporospatial,
        'E4_Ibi': resampling.resample_temporospatial}
    return _resample_multistream(stream, col_sampler, sampling_dt)


def _resample_multistream(
        stream: Stream,
        col_sampler: dict[str, Callable],
        sampling_dt: Union[pd.DataFrame, datetime.timedelta]) -> gpd.GeoDataFrame:
    check_stream_data_integrity(stream)
    resampled = _get_resampled_georef(stream, sampling_dt)
    resampled_data = [sampler(stream.data[key], resampled, sampling_dt=None)
                      for key, sampler in col_sampler.items()
                      if key in stream.data]
    geometry = resampled_data[0].geometry
    return gpd.GeoDataFrame(pd.concat([d.drop('geometry', axis=1)
                                       for d in resampled_data], axis=1),
                                       geometry=geometry)


def check_stream_data_integrity(stream: Stream):
    if stream.data is None:
        raise ValueError("The stream does not have valid data.")


def _get_resampled_georef(stream: Stream, sampler: Union[pd.DataFrame, datetime.timedelta]) -> pd.DataFrame:
    if isinstance(sampler, pd.DataFrame):
        return sampler
    
    if hasattr(stream, "parent_dataset") is False:
        raise AttributeError("The stream does not have a valid parent Dataset.")
    if stream.parent_dataset is None:
        raise ValueError("The stream does not have a valid parent Dataset.")
    if stream.parent_dataset.has_calibration is False:
        raise ValueError(
            "The stream's parent Dataset does not have a valid calibration.\
                Calibrate the Dataset before exporting the stream by\
                    calling Dataset.add_georeference_and_calibrate()")
    georef = stream.parent_dataset.georeference.spacetime
    return resampling.resample_georeference(georef, sampler)


def shift_stream_index(data, offset):
    """Offsets the specified stream data index."""
    if len(data) > 0:
        data.index += offset
