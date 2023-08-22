## Export streams to csv
from __future__ import annotations
import os
import datetime
import pandas as pd

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


def export_uniform_table_stream(stream: HarpStream,
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
                         sampler: Callable = resampling.resample_temporospatial,
                         **kwargs) -> pd.DataFrame:
    check_stream_data_integrity(stream)
    return sampler(stream.data, _get_georef(stream), sampling_dt)


def resample_stream_accelerometer(stream: Stream,
                                  sampling_dt: datetime.timedelta = datetime.timedelta(seconds=2),
                                  **kwargs) -> pd.DataFrame:
    check_stream_data_integrity(stream)
    col_sampler = {
        'Orientation.X': resampling.resample_temporospatial_circ,
        'Orientation.Y': resampling.resample_temporospatial_circ,
        'Orientation.Z': resampling.resample_temporospatial_circ,
        'Gyroscope.X': resampling.resample_temporospatial,
        'Gyroscope.Y': resampling.resample_temporospatial,
        'Gyroscope.Z': resampling.resample_temporospatial,
        'LinearAccl.X': resampling.resample_temporospatial,
        'LinearAccl.Y': resampling.resample_temporospatial,
        'LinearAccl.Z': resampling.resample_temporospatial,
        'Magnetometer.X': resampling.resample_temporospatial,
        'Magnetometer.Y': resampling.resample_temporospatial,
        'Magnetometer.Z': resampling.resample_temporospatial,
        'Accl.X': resampling.resample_temporospatial,
        'Accl.Y': resampling.resample_temporospatial,
        'Accl.Z': resampling.resample_temporospatial,
        'Gravity.X': resampling.resample_temporospatial,
        'Gravity.Y': resampling.resample_temporospatial,
        'Gravity.Z': resampling.resample_temporospatial}
    georef = _get_georef(stream)
    resampled_data = {k: resampling_method(stream.data[k], georef, sampling_dt)
                      for k, resampling_method in col_sampler.items()
                      if k in stream.data.columns}
    out = resampled_data[list(col_sampler.keys())[0]].copy()
    out.drop(columns=['Data'], axis=1)

    for key in resampled_data.keys():
        out[key] = resampled_data[key]["Data"]
    return out


def resample_stream_empatica(stream: Stream,
                            sampling_dt: datetime.timedelta = datetime.timedelta(seconds=2),
                             **kwargs) -> pd.DataFrame:
    check_stream_data_integrity(stream)
    col_sampler = {
        'E4_Gsr': resampling.resample_temporospatial,
        'E4_Hr': resampling.resample_temporospatial,
        'E4_Ibi': resampling.resample_temporospatial}
    georef = _get_georef(stream)
    resampled_data = {k: resampling_method(stream.data[k]["Value"], georef, sampling_dt)
                      for k, resampling_method in col_sampler.items()
                      if k in stream.data}
    out = resampled_data[list(col_sampler.keys())[0]].copy()
    out.drop(columns=['Data'], axis=1)

    for key in resampled_data.keys():
        out[key] = resampled_data[key]["Data"]
    return out


def check_stream_data_integrity(stream: Stream):
    if stream.data is None:
        raise ValueError("The stream does not have valid data.")


def _get_georef(stream: Stream) -> pd.DataFrame:
    if hasattr(stream, "parent_dataset") is False:
        raise AttributeError("The stream does not have a valid parent Dataset.")
    if stream.parent_dataset is None:
        raise ValueError("The stream does not have a valid parent Dataset.")
    if stream.parent_dataset.has_calibration is False:
        raise ValueError(
            "The stream's parent Dataset does not have a valid calibration.\
                Calibrate the Dataset before exporting the stream by\
                    calling Dataset.add_georeference_and_calibrate()")
    return stream.parent_dataset.georeference
