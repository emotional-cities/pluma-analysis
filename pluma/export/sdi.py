from __future__ import annotations
import os
import datetime
import pandas as pd
from dotmap import DotMap

from pluma.stream import Stream, StreamType


exclude_devices = ["PupilLabs", "Microphone", "Empatica", "BioData", "UBX"]


def export_dataset_to_sdi(
        dataset,
        sampling_dt: datetime.timedelta = datetime.timedelta(seconds=2),
        outdir=None
        ):

    streams_to_export = {}
    for stream in dataset.streams:
        _ = recurvise_resample_stream(
            streams_to_export, dataset.streams[stream], sampling_dt)

    exclude = ['Latitude', 'Longitude', 'Elevation']

    out = streams_to_export[list(streams_to_export.keys())[0]].copy()
    out = out.iloc[:, 0:3]

    for stream in streams_to_export:
        cols = list(streams_to_export[stream].columns)
        for idx, entry in enumerate(cols):
            if entry not in exclude:
                cols[idx] = f"{stream}.{entry}"
        streams_to_export[stream].columns = cols
        out = pd.merge(out, streams_to_export[stream], how='outer')

    if outdir is None:
        outdir = dataset.rootfolder.path
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
    out.to_csv(os.path.join(outdir, "sdi.csv"), date_format='%Y-%m-%dT%H:%M:%S.%fZ')

def recurvise_resample_stream(acc_dict, stream, sampling_dt):
    ret = None
    if isinstance(stream, DotMap):
        for key in stream:
            recurvise_resample_stream(acc_dict, stream[key], sampling_dt)
    elif isinstance(stream, Stream):
        if stream.device not in exclude_devices:
            try:
                ret = stream.resample(sampling_dt)
            except NotImplementedError as E:
                pass
            except:
                print(f"Failed Stream {stream}")
        else:
            pass
    else:
        print(type(stream))

    if ret is not None:
        acc_dict[f"{stream.device}.{stream.streamlabel}"] = ret
    return ret