import warnings

import pyubx2 as ubx
import pandas as pd

from enum import Enum
from typing import Union

from pluma.io.path_helper import ComplexPath, ensure_complexpath
from pluma.io.harp import _HARP_T0


_UBX_CLASSES = Enum(
    "_UBX_CLASSES",
    {x.replace("-", "_"): x.replace("-", "_") for x in ubx.UBX_CLASSES.values()},
)
_UBX_MSGIDS = Enum(
    "_UBX_MSGIDS",
    {x.replace("-", "_"): x.replace("-", "_") for x in ubx.UBX_MSGIDS.values()},
)


def load_ubx_bin_event(
    root: Union[str, ComplexPath],
    ubxmsgid: _UBX_MSGIDS,
    ubxfolder: str = "UBX",
    ext: str = "bin",
) -> pd.DataFrame:
    """Helper function to generate a full file path to \
        a binary file, and load the stream of a \
            specific UBX event

    Args:
        root (Union[str, ComplexPath]): Root path where \
            filename is expected to be found.
        ubxmsgid (_UBX_MSGIDS): ID of the event to be loaded.
        ubxfolder (str, optional): Folder, nested inside root,\
            where all events are expected to be found. Defaults to 'UBX'.
        ext (str, optional): Expected file extension. Defaults to 'bin'.

    Returns:
        pd.DataFrame: Output of read_ubx_file()
    """
    root = ensure_complexpath(root)
    root.join([ubxfolder, f"{ubxmsgid.value.upper()}.{ext}"])
    return read_ubx_file(root)


def read_ubx_file(path: Union[str, ComplexPath]) -> pd.DataFrame:
    """Outputs a dataframe with all messages\
        from single UBX binary file.

    Args:
        path (Union[str, ComplexPath]): Absolute path to the UBX binary file.

    Returns:
        pd.DataFrame: Output DataFrame with minimally processed UBX messages.
    """
    out = []
    path = ensure_complexpath(path)
    try:
        with path.open("rb") as fstream:
            out = read(fstream)
    except FileNotFoundError:
        warnings.warn(f"UBX file\
            {path} could not be found.")
        return pd.DataFrame()
    except FileExistsError:
        warnings.warn(f"UBX file\
            {path} could not be found.")
        return pd.DataFrame()

    df = pd.DataFrame({"Message": out})
    df["Identity"] = df["Message"].apply(lambda x: x.identity)
    df["Class"] = df["Message"].apply(lambda x: x.identity.split("-")[0])
    df["Id"] = df["Message"].apply(lambda x: x.identity.split("-")[1])
    df["Length"] = df["Message"].apply(lambda x: x.length)
    return df


def load_ubx_harp_ts_event(
    root: Union[str, ComplexPath],
    ubxmsgid: _UBX_MSGIDS,
    ubxfolder: str = "UBX",
    ext: str = "csv",
) -> pd.DataFrame:
    """Helper function to generate a full file path to \
        a .csv file, and load the stream of a \
            specific UBX-Bonsai-timestamped event

    Args:
        root (Union[str, ComplexPath]): Root path where \
            filename is expected to be found.
        ubxmsgid (_UBX_MSGIDS): ID of the event to be loaded.
        ubxfolder (str, optional): Folder, nested inside root,\
            where all events are expected to be found. Defaults to 'UBX'.
        ext (str, optional): Expected file extension. Defaults to 'csv'.

    Returns:
        pd.DataFrame: output of load_ubx_harp_ts()
    """
    root = ensure_complexpath(root)
    root.join([ubxfolder, f"{ubxmsgid.value.upper()}.{ext}"])
    return load_ubx_harp_ts(root)


def load_ubx_harp_ts(path: Union[str, ComplexPath] = "") -> pd.DataFrame:
    """Reads the software timestamped data of all UBX messages in a single\
        .csv file.

    Args:
        path (Union[str, ComplexPath]): Absolute path to the .csv binary file.

    Returns:
        pd.DataFrame: DataFrame with relevant data index by time.
    """

    path = ensure_complexpath(path)
    try:
        with path.open("rb") as stream:
            df = pd.read_csv(stream, header=None, names=("Seconds", "Class", "Identity"))
    except FileNotFoundError:
        warnings.warn(f"UBX stream alignment file {path} could not be found.")
        return
    except FileExistsError:
        warnings.warn(f"UBX stream alignment file {path} could not be found.")
        return
    df["Seconds"] = _HARP_T0 + pd.to_timedelta(df["Seconds"].values, "s")
    df.set_index("Seconds", inplace=True)
    return df


def load_ubx_event_stream(
    ubxmsgid: _UBX_MSGIDS, root: Union[str, ComplexPath] = "", ubxfolder: str = "UBX"
) -> pd.DataFrame:
    """Helper function that returns a merged DataFrame with the outputs
    of load_ubx_bin_event() and load_ubx_harp_ts_event().
    It additionally checks if, for each binary messages there
    exists the corresponding timestamped event.

    Args:
        ubxmsgid (_UBX_MSGIDS): Id of the UBX message to be loaded.
        root (str, optional): Root path for both .csv and .bin files. Defaults to ''.
        ubxfolder (str, optional): Folder, nested inside root,\
            where all events are expected to be found. Defaults to 'UBX'.
    Raises:
        ValueError: Raises an error if there is a mismatch between the two files.

    Returns:
        pd.DataFrame: DataFrame indexed by the message times found
        in the output of load_ubx_harp_ts()
    """
    root = ensure_complexpath(root)
    bin_file = load_ubx_bin_event(ubxmsgid=ubxmsgid, root=root, ubxfolder=ubxfolder)
    csv_file = load_ubx_harp_ts_event(ubxmsgid=ubxmsgid, root=root, ubxfolder=ubxfolder)
    if (bin_file["Class"].values == csv_file["Class"].values).all():
        bin_file["Seconds"] = csv_file.index
        bin_file = bin_file.set_index("Seconds")
        return bin_file
    else:
        raise ValueError("Misalignment found between CSV and UBX arrays.")


def errhandler(err):
    """
    Handles errors output by iterator.
    """
    print(f"\nERROR: {err}\n")


def read(
    stream,
    errorhandler=errhandler,
    protfilter=2,
    quitonerror=3,
    validate=True,
    msgmode=0,
):
    """
    Reads and parses UBX message data from stream.
    """
    ubr = ubx.UBXReader(
        stream,
        protfilter=protfilter,
        quitonerror=quitonerror,
        errorhandler=errorhandler,
        validate=validate,
        msgmode=msgmode,
        parsebitfield=True,
    )
    return [parsed_data for (_, parsed_data) in ubr]
