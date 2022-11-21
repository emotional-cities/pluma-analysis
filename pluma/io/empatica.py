import os
import warnings

import pandas as pd
from dotmap import DotMap

from pluma.io.harp import _HARP_T0


def load_empatica(filename: str = 'empatica_harp_ts.csv',
                  root: str = '') -> DotMap:
    """Loads the raw Empatica data, from a .csv file, to a DotMap structure.

    Args:
        filename (str, optional): Input file name to target. Defaults to 'empatica_harp_ts.csv'.
        root (str, optional): Root path where filename is expected to be found. Defaults to ''.

    Returns:
        DotMap: DotMap where each Empatica message type can be indexed.
    """
    try:
        df = pd.read_csv(os.path.join(root, filename),
                         names=['Message', 'Seconds'],
                         delimiter=',', header=1)
    except FileNotFoundError:
        warnings.warn(f'Empatica stream file {filename} could not be found.')
        return
    except FileExistsError:
        warnings.warn(f'Empatica stream file {filename} could not be found.')
        return
    df['Seconds'] = _HARP_T0 + pd.to_timedelta(df['Seconds'].values, 's')
    df.set_index('Seconds', inplace=True)
    df['StreamId'] = df['Message'].apply(lambda x: x.split(' ')[0])
    _dict = {}
    for label, group in df.groupby('StreamId'):
        _dict[label] = parse_empatica_stream(group)
    return DotMap(_dict)


def parse_empatica_stream(empatica_stream: pd.DataFrame) -> pd.DataFrame:
    """Helper function to parse the messages from various empatica message types

    Args:
        empatica_stream (pd.DataFrame): CSV data in DataFrame format

    Returns:
        pd.DataFrame: A DataFrame with parsed relevant empatica data indexed by time.
    """
    stream_id = empatica_stream['Message'][0].split(' ')[0]
    if stream_id == 'E4_Acc':
        df = empatica_stream['Message'].str.split(pat=' ', expand=True)
        df_labels = ['Stream', 'E4_Seconds', 'AccX', 'AccY', 'AccZ']
        df.columns = df_labels
        df[['AccX', 'AccY', 'AccZ']] =\
            df[['AccX', 'AccY', 'AccZ']].astype(float)
        df['E4_Seconds'] = _HARP_T0 + \
            pd.to_timedelta(df['E4_Seconds'].values.astype(float), 's')

    elif stream_id in \
        ['E4_Hr', 'E4_Bvp',
         'E4_Gsr', 'E4_Battery',
         'E4_Ibi', 'E4_Tag',
         'E4_Temperature']:

        df = empatica_stream['Message'].str.split(pat=' ', expand=True)
        df_labels = ['Stream', 'E4_Seconds', 'Value']
        df.columns = df_labels
        df[['Value']] = df[['Value']].astype(float)
        df['E4_Seconds'] = _HARP_T0 +\
            pd.to_timedelta(df['E4_Seconds'].values.astype(float), 's')

    elif stream_id == 'R':
        df = pd.DataFrame(index=empatica_stream.index.copy())
        df['Message'] = empatica_stream['Message'].apply(
            lambda a: a[2:])
        df['StreamId'] = empatica_stream['Message'].apply(
            lambda x: x.split(' ')[0])
    else:
        raise (f'Unexpected empatica stream id label: {stream_id}.\
            No parse is currently set.')
    return df
