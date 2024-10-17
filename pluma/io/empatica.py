import warnings
import datetime

import pandas as pd
from dotmap import DotMap
from typing import Union

from pluma.io.harp import _HARP_T0
from pluma.io.path_helper import ComplexPath, ensure_complexpath

_EMPATICA_T0 = datetime.datetime(1970, 1, 1)


def load_empatica(
    filename: str = "empatica_harp_ts.csv",
    root: Union[str, ComplexPath] = "",
    align_timestamps: bool = True,
) -> DotMap:
    """Loads the raw Empatica data stream, from a .csv file, to a DotMap structure.

    Args:
        filename (str, optional): Input file name to target. Defaults to 'empatica_harp_ts.csv'.
        root (Union[str, ComplexPath], optional): Root path where filename is expected to be found. Defaults to ''.
        align_timestamps (bool, optional): Specifies whether to align time to E4 sensor timestamps.

    Returns:
        DotMap: DotMap where each Empatica message type can be indexed.
    """

    path = ensure_complexpath(root)
    path.join(filename)
    try:
        with path.open("rb") as stream:
            df = pd.read_csv(
                stream, names=["Message", "Seconds"], delimiter=",", header=1
            )
    except FileNotFoundError:
        warnings.warn(f"Empatica stream file {filename} could not be found.")
        return
    except FileExistsError:
        warnings.warn(f"Empatica stream file {filename} could not be found.")
        return

    clock_offset = None
    df["Seconds"] = _HARP_T0 + pd.to_timedelta(df["Seconds"].values, "s")
    if align_timestamps:
        first_ts = next(
            (x for _, x in df.iterrows() if x["Message"].startswith("E4_")), None
        )
        if first_ts is not None:
            reference_ts = _EMPATICA_T0 + pd.to_timedelta(
                float(first_ts["Message"].split(" ")[1]), "s"
            )
            clock_offset = first_ts["Seconds"] - reference_ts

    df.set_index("Seconds", inplace=True)
    df["StreamId"] = df["Message"].apply(lambda x: x.split(" ")[0])
    _dict = {}
    for label, group in df.groupby("StreamId"):
        _dict[label] = parse_empatica_stream(group, clock_offset)
    return DotMap(_dict)


def parse_empatica_stream(
    empatica_stream: pd.DataFrame, clock_offset: pd.Timedelta = None
) -> pd.DataFrame:
    """Helper function to parse the messages from various empatica message types.

    Args:
        empatica_stream (pd.DataFrame): CSV data in DataFrame format
        clock_offset (pd.Timedelta, optional): Optional clock offset used to index time from E4 timestamps.

    Returns:
        pd.DataFrame: A DataFrame with parsed relevant empatica data indexed by time.
    """
    stream_id = empatica_stream["Message"][0].split(" ")[0]
    if stream_id == "E4_Acc":
        df = empatica_stream["Message"].str.split(pat=" ", expand=True)
        df_labels = ["Stream", "E4_Seconds", "AccX", "AccY", "AccZ"]
        df.columns = df_labels
        df[["AccX", "AccY", "AccZ"]] = df[["AccX", "AccY", "AccZ"]].astype(float)
        df["E4_Seconds"] = _EMPATICA_T0 + pd.to_timedelta(
            df["E4_Seconds"].values.astype(float), "s"
        )
        if clock_offset is not None:
            df.index = pd.DatetimeIndex(
                df["E4_Seconds"] + clock_offset, name=df.index.name
            )

    elif stream_id in [
        "E4_Hr",
        "E4_Bvp",
        "E4_Gsr",
        "E4_Battery",
        "E4_Ibi",
        "E4_Tag",
        "E4_Temperature",
    ]:
        df = empatica_stream["Message"].str.split(pat=" ", expand=True)
        df_labels = ["Stream", "E4_Seconds", "Value"]
        df.columns = df_labels
        df[["Value"]] = df[["Value"]].astype(float)
        df["E4_Seconds"] = _EMPATICA_T0 + pd.to_timedelta(
            df["E4_Seconds"].values.astype(float), "s"
        )
        if clock_offset is not None:
            df.index = pd.DatetimeIndex(
                df["E4_Seconds"] + clock_offset, name=df.index.name
            )
    elif stream_id == "R":
        df = pd.DataFrame(index=empatica_stream.index.copy())
        df["Message"] = empatica_stream["Message"].apply(lambda a: a[2:])
        df["StreamId"] = empatica_stream["Message"].apply(lambda x: x.split(" ")[0])
    else:
        raise (
            f"Unexpected empatica stream id label: {stream_id}.\
            No parse is currently set."
        )
    return df
