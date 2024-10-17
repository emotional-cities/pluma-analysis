from __future__ import annotations
import datetime
import pandas as pd
import geopandas as gpd
import pluma.preprocessing.resampling as resampling

from dotmap import DotMap
from pluma.stream import Stream


exclude_devices = ["PupilLabs", "Microphone", "BioData", "Enobio", "UBX"]


def convert_dataset_to_geoframe(dataset, sampling_dt: datetime.timedelta = datetime.timedelta(seconds=1)):
    georef = resampling.resample_georeference(dataset.georeference.spacetime, sampling_dt)
    streams_to_export = {}
    for stream in dataset.streams:
        _ = recursive_resample_stream(streams_to_export, dataset.streams[stream], georef)

    exclude = ["Latitude", "Longitude", "Elevation"]
    out_columns = []
    for stream in streams_to_export:
        cols = list(streams_to_export[stream].columns)
        for idx, entry in enumerate(cols):
            if entry in exclude:
                continue

            cols[idx] = (stream if entry.lower() == "data" else f"{stream}_{entry}").lower()
        streams_to_export[stream].columns = cols
        out_columns.append(streams_to_export[stream])

    geometry = out_columns[0][out_columns[0].columns[-1]]
    out = gpd.GeoDataFrame(
        pd.concat([d.drop(d.columns[-1], axis=1) for d in out_columns], axis=1),
        geometry=geometry,
    )
    out.index.name = "time"
    return out


def export_dataset_to_geojson(
    dataset, filename, sampling_dt: datetime.timedelta = datetime.timedelta(seconds=1)
):
    out = convert_dataset_to_geoframe(dataset, sampling_dt)
    export_geoframe_to_geojson(out, filename)


def export_geoframe_to_geojson(frame, filename):
    micro_format = ".%f"
    try:
        if frame.index.freq.delta.to_pytimedelta().microseconds == 0:
            micro_format = ""
    except Exception:
        pass
    out = frame.reset_index(names="time")
    out.time = out.time.dt.strftime(f"%Y-%m-%dT%H:%M:%S{micro_format}Z")
    out.index.name = "id"
    out.to_file(filename, driver="GeoJSON", index=True)


def recursive_resample_stream(acc_dict, stream, sampling_dt):
    ret = None
    if isinstance(stream, DotMap):
        for key in stream:
            recursive_resample_stream(acc_dict, stream[key], sampling_dt)
    elif isinstance(stream, Stream):
        if stream.device not in exclude_devices:
            try:
                ret = stream.resample(sampling_dt)
            except NotImplementedError:
                pass
            except Exception as E:
                print(f"Failed Stream {stream}: {E}")
    else:
        print(type(stream))

    if ret is not None:
        acc_key = stream.device
        if stream.streamlabel != acc_key:
            acc_key = f"{acc_key}_{stream.streamlabel}"
        acc_dict[acc_key] = ret
    return ret
