## Export streams to csv
from __future__ import annotations
import os
import datetime
import pandas as pd

from typing import Union, Optional, Callable, Dict

from pluma.stream import Stream, StreamType

from pluma.preprocessing.resampling import resample_temporospatial


def export_stream_to_csv(stream: Stream, export_path: str,
                         resampling_function: Callable = resample_temporospatial,
                         resampling_function_kws: Dict = None,
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

    if (stream.streamtype == StreamType.HARP or stream.streamtype == StreamType.ACCELEROMETER):
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


def export_uniform_table_stream(stream: Union[HarpStream, AccelerometerStream],
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


# def export_streams(schema, root_path, georeference):
#     if isinstance(schema, Stream):
#         print(schema)
#         if isinstance(schema.data, pd.DataFrame):
#             outdir = f"{root_path}\\{schema.device}"
#             if not os.path.exists(outdir):
#                 os.makedirs(outdir, exist_ok=True)
#             try:
#                 resampled = resample_temporospatial(schema.data,
#                                                     georeference,
#                                                     sampling_dt=datetime.timedelta(seconds = 1))
#                 resampled.to_csv(f"{outdir}\\{schema.streamlabel}.csv", date_format='%Y-%m-%dT%H:%M:%S.%fZ')
#             except:
#                 print(f"failed {schema.streamlabel}")
#         elif isinstance(schema.data, np.ndarray):
#             pass
#             #print(schema.device, schema.streamlabel)
#         else:
#             print(type(schema.data))
#     elif isinstance(schema, DotMap):
#         for _stream in schema.values():
#             export_streams(_stream, root_path=root_path, georeference=georeference)
#     else:
#         raise TypeError(f"Invalid type was found. Must be of {Union[DotMap, Stream]}")
    
# def export_streams_to_csv(stream: Union[HarpStream, AccelerometerStream],
#                           root_path, georeference):
#     export_streams(dataset, root_path, georeference)