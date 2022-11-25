import warnings

import pyubx2 as ubx
import pandas as pd

from enum import Enum
from typing import Union

from pluma.io.path_helper import ComplexPath, ensure_complexpath
from pluma.io.harp import _HARP_T0


_UBX_CLASSES = Enum('_UBX_CLASSES',
                    {x.replace('-', '_'): x.replace('-', '_')
                     for x in ubx.UBX_CLASSES.values()})
_UBX_MSGIDS = Enum('_UBX_MSGIDS',
                   {x.replace('-', '_'): x.replace('-', '_')
                    for x in ubx.UBX_MSGIDS.values()})


def load_ubx_bin_event(root: Union[str, ComplexPath],
                       ubxmsgid: _UBX_MSGIDS,
                       ubxfolder: str = 'UBX',
                       ext: str = 'bin') -> pd.DataFrame:
    root = ensure_complexpath(root)
    root.join([ubxfolder, f'{ubxmsgid.value.upper()}.{ext}'])
    return read_ubx_file(root)


def read_ubx_file(path: Union[str, ComplexPath]) -> pd.DataFrame:
    """Outputs a dataframe with all messages from UBX binary file.

    Args:
        path (str): Absolute path to the UBX binary file.

    Returns:
        pd.DataFrame: Output DataFrame with minimally parsed UBX messages.
    """
    out = []
    path = ensure_complexpath(path)
    try:
        with path.open('rb') as fstream:
            out = read(fstream)
    except FileNotFoundError:
        warnings.warn(f'UBX file\
            {path} could not be found.')
        return pd.DataFrame()
    except FileExistsError:
        warnings.warn(f'UBX file\
            {path} could not be found.')
        return pd.DataFrame()

    df = pd.DataFrame({'Message': out})
    df['Identity'] = df['Message'].apply(lambda x: x.identity)
    df['Class'] = df['Message'].apply(lambda x: x.identity.split('-')[0])
    df['Id'] = df['Message'].apply(lambda x: x.identity.split('-')[1])
    df['Length'] = df['Message'].apply(lambda x: x.length)
    return df

def load_ubx_harp_ts_event(root: Union[str, ComplexPath],
                           ubxmsgid: _UBX_MSGIDS,
                           ubxfolder: str = 'UBX',
                           ext: str = 'csv') -> pd.DataFrame:
    root = ensure_complexpath(root)
    root.join([ubxfolder, f'{ubxmsgid.value.upper()}.{ext}'])
    return load_ubx_harp_ts(root)

def load_ubx_harp_ts(path: Union[str, ComplexPath] = '') -> pd.DataFrame:
    """Reads the software timestamped data of all UBX messages

    Args:
        path (str, optional): Relative path of the expected .csv file
        wherein each line is a received UBX message. Defaults to 'ubx_harp_ts.csv'.
        root (str, optional): Root path for the .csv file. Defaults to ''.

    Returns:
        pd.DataFrame: DataFrame with relevant data index by time.
    """
    path = ensure_complexpath(path)
    try:
        with path.open('rb') as stream:
            df = pd.read_csv(stream,
                             header=None,
                             names=('Seconds', 'Class', 'Identity'))
    except FileNotFoundError:
        warnings.warn(
            f'UBX stream alignment file {path} could not be found.')
        return
    except FileExistsError:
        warnings.warn(
            f'UBX stream alignment file {path} could not be found.')
        return
    df['Seconds'] = _HARP_T0 + pd.to_timedelta(df['Seconds'].values, 's')
    df.set_index('Seconds', inplace=True)
    return df


def load_ubx_event_stream(ubxmsgid: _UBX_MSGIDS,
                          root: Union[str, ComplexPath] = '',
                          ubxfolder: str = 'UBX') -> pd.DataFrame:
    """Helper function that outputs the merge the outputs of
    load_ubx_bin_event() and load_ubx_harp_ts_event().
    It additionally checks if, for each binary messages
    there exists the corresponding timestamped event.

    Args:
        ubxmsgid (_UBX_MSGIDS): _description_
        root (str, optional): Root path for both .csv and .bin files. Defaults to ''.
        ubxfolder (str, optional): Folder name of containing all
        ubxmsgid-separated binary files. Defaults to 'ubx'.
    Raises:
        ValueError: Raises an error if there is a mismatch between the two files.

    Returns:
        pd.DataFrame: DataFrame indexed by the message times found in the output of load_ubx_harp_ts()
    """
    root = ensure_complexpath(root)
    bin_file = load_ubx_bin_event(ubxmsgid=ubxmsgid,
                                  root=root,
                                  ubxfolder=ubxfolder)
    csv_file = load_ubx_harp_ts_event(ubxmsgid=ubxmsgid,
                                      root=root,
                                      ubxfolder=ubxfolder)
    if (bin_file['Class'].values == csv_file['Class'].values).all():
        bin_file['Seconds'] = csv_file.index
        bin_file = bin_file.set_index('Seconds')
        return bin_file
    else:
        raise ValueError('Misalignment found between CSV and UBX arrays.')


def errhandler(err):
    '''
    Handles errors output by iterator.
    '''
    print(f'\nERROR: {err}\n')


def read(stream,
         errorhandler=errhandler, protfilter=2,
         quitonerror=3, validate=True, msgmode=0):
    '''
    Reads and parses UBX message data from stream.
    '''
    ubr = ubx.UBXReader(
        stream,
        protfilter=protfilter,
        quitonerror=quitonerror,
        validate=validate,
        msgmode=msgmode,
        parsebitfield=True,
    )
    return [parsed_data for (_, parsed_data) in ubr.iterate(
        quitonerror=quitonerror, errorhandler=errorhandler
    )]

## TODO

#http://docs.ros.org/en/kinetic/api/ublox_msgs/html/msg/EsfMEAS.html
#https://cdn.sparkfun.com/assets/learn_tutorials/1/1/7/2/ZED-F9R_Interfacedescription__UBX-19056845_.pdf  @page 57
#integration document @p36 https://content.u-blox.com/sites/default/files/ZED-F9R_Integrationmanual_UBX-20039643.pdf?hash=undefined&_ga=2.212516247.229517523.1660666345-1786438948.1649933107
#dataType = 5 : z-axis gyroscope angular rate deg/s *2^-12 (signed 24bit)
#dataType = 11 : speed m/s * 1e-3 (signed)
#dataType = 12 : Gyro temperature (deg celsiues 1e-2) signed
#dataType = 13 : y-axis gyroscope angular rate deg/s *2^-12 (signed 24bit)
#dataType = 14 : x-axis gyroscope angular rate  deg/s *2^-12 (signed 24bit)
#dataType = 16 : Gyro x acc (m/s^2 *2^-10) signed
#dataType = 17 : Gyro y acc (m/s^2 *2^-10) signed
#dataType = 18 : Gyro z acc (m/s^2 *2^-10) signed

#def get_gyro_from_ubx(message):
#    return pd.Series([e, f, g])

## Parse accelerometer data

# ESF_MEAS = filter_event(ubx_data, "ESF-MEAS")

# _dataTypeDict = {
#     5 : 'angular_rate_z',
#     8 : 'left_wheel_tick',
#     9 : 'right_wheel_tick',
#     10 : 'speed_tick',
#     11 : 'speed',
#     12: 'temperature',
#     13 : 'angular_rate_y',
#     14 : 'angular_rate_x',
#     16 : 'gyro_acc_x',
#     17 : 'gyro_acc_y',
#     18 : 'gyro_acc_z'
# }

# [ESF_MEAS.assign(x = np.NAN) for x in _dataTypeDict.values()]


# for ii, row in ESF_MEAS.iterrows():
#     message = row['Message']
#     n = message.numMeas
#     for i in range(n):
#         datatype = getattr(message, f'dataType_0{i+1}')
#         datafield = getattr(message, f'dataField_0{i+1}')
#         ESF_MEAS.loc[ii,_dataTypeDict[datatype]] = datafield
# print(ESF_MEAS)
# acc = ESF_MEAS[~ESF_MEAS["gyro_acc_z"].isnull()]

# plt.figure()
# plt.plot(acc.index.values, acc.gyro_acc_z.values)
# plt.show()

# acc