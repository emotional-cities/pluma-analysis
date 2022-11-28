import pickle

from dotmap import DotMap
from typing import Union

from pluma.schema.outdoor import build_schema
from pluma.sync.ubx2harp import get_clockcalibration_ubx_to_harp_clock
from pluma.stream import StreamType, Stream

from pluma.plotting import maps

from pluma.stream.ubx import UbxStream

from pluma.stream.georeference import Georeference

from pluma.io.path_helper import ComplexPath, ensure_complexpath


class Dataset:

    def __init__(self,
                 root: Union[str, ComplexPath],
                 datasetlabel: str = '',
                 georeference: Georeference = Georeference()):
        """High level class to represent an entire dataset. Loads and
        contains all the streams and methods for general dataset management.

        Args:
            root (Union[str, Path]): Path to the folder containing the full dataset raw data.
            datasetlabel (str, optional): Descriptive label. Defaults to ''.
        """
        self.rootfolder = ensure_complexpath(root)
        self.datasetlabel = datasetlabel
        self.georeference = georeference
        self.streams = None

    def add_ubx_georeference(self,
                             ubxstream: UbxStream = None,
                             event: str = "NAV-HPPOSLLH",
                             calibrate_clock: bool = True,
                             strip=True):
        """_summary_

        Args:
            ubxstream (UbxStream, optional): UBX stream that will be used to automatically\
                generate a valid NavData. Defaults to None.
            event (str, optional): If ubxstream is None, this string will be used to\
                extract the valid position event. Defaults to "NAV-HPPOSLLH".
            calibrate_clock (bool, optional): If True, automatic drift correction will\
                be attempted to correct the UBX clock to the harp clock. Defaults to True.

        Raises:
            ImportError: Raises an error if the import of the UBX stream fails.
            TypeError: Raises an error if the wrong datatype is passed to the ubxstream input.
        """
        if ubxstream is None:
            try:
                navdata = self.streams.UBX.parseposition(
                    event=event,
                    calibrate_clock=calibrate_clock)
            except:
                raise ImportError('Could not load Ubx stream.')
        else:
            if not(ubxstream.streamtype == StreamType.UBX):
                raise TypeError("Reference must be a Ubx Stream")
            else:
                navdata = ubxstream.parseposition(
                    event=event,
                    calibrate_clock=calibrate_clock)
        self.georeference.from_dataframe(navdata)
        if strip is True:
            self.georeference.strip()

    def reload_streams(self,
                       schema: Union[DotMap, Stream, None] = None,
                       force_load: bool = False) -> None:
        """Recursively loads, from disk , all available streams in the streams' schema

        Args:
            schema (Union[DotMap, Stream, None]): Target schema to reload. \
                If None it will default to the Dataset.streams schema. Defaults to None.
            force_load (bool, optional): If True, it will attempt to load any stream found,\
                ignoring the stream.autoload value. Defaults to False.
        Raises:
            TypeError: An error is raised if a not allowed type is passed.
        """

        if schema is None:
            schema = self.streams

        if isinstance(schema, Stream):
            if force_load is True:
                schema.load()
            else:
                if schema.autoload is True:
                    schema.load()
        elif isinstance(schema, DotMap):
            for _stream in schema.values():
                self.reload_streams(_stream, force_load=force_load)
        else:
            raise TypeError(f"Invalid type was found. Must be of {Union[DotMap, Stream]}")

    def export_streams(self, filename: Union[str, ComplexPath] = None):
        """Serializes and exports the dataset as a pickle object.

        Args:
            filename (str, optional): Path to save the .pickle file.\
                If None, it will save to Dataset.root. Defaults to None.
        """

        if filename is None:
            path = ensure_complexpath(self.rootfolder)
            path.join('dataset.pickle')
        else:
            path = ensure_complexpath(filename)
        with path.open('wb') as handle:
            pickle.dump(self.streams, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def import_streams(self, filename: Union[str, ComplexPath] = None):
        """Deserializes and imports the dataset as a pickle object.

        Args:
            filename (str, optional): Path to load the .pickle file from.\
                If None, it will use Dataset.root. Defaults to None.
        """
        if filename is None:
            path = ensure_complexpath(self.rootfolder)
            path.join('dataset.pickle')
        else:
            path = ensure_complexpath(filename)
        with path.open('rb') as handle:
            self.streams = pickle.load(handle)

    def populate_streams(self,
                         root: Union[str, ComplexPath, None] = None,
                         autoload: bool = False):
        """Populates the streams property with all the schema information.

        Args:
            root (str, optional): Path to the folder containing the full\
                dataset rawdata. If None, it will default to Dataset.root.
            autoload (bool, optional): If True it will automatically\
                attempt to load data from disk. Defaults to False.
        """
        if root is None:
            root = self.rootfolder
        if isinstance(root, str):
            root = ComplexPath(root)
        root = ensure_complexpath(root)
        self.streams = build_schema(
            root=root,
            autoload=autoload)

    def calibrate_ubx_to_harp(self,
                              dt_error: float = 0.002,
                              plot_diagnosis: bool = False,
                              r2_min_qc: float = 0.99):
        """Attempts to calibrate the ubx clock to harp clock using\
            the synchronization pulses as a reference.

        Args:
            dt_error (float, optional): Allowed error between the derivate\
                of timestamps detected in the two streams. Defaults to 0.002 seconds.
            plot_diagnosis (bool, optional): If True plots the output of\
                the syncing algorithm. Defaults to False.
            r2_min_qc (float, optional): Quality control parameter.
            If < r2_min_qc, an error will be raised, since it likely\
                results from an automatic correction procedure. Defaults to 0.99.
        """
        self.streams.UBX.clock_calib_model =\
            get_clockcalibration_ubx_to_harp_clock(
                ubx_stream=self.streams.UBX,
                harp_sync=self.streams.BioData.Set.data,
                dt_error=dt_error,
                r2_min_qc=r2_min_qc,
                plot_diagnosis=plot_diagnosis)

    def showmap(self, **kwargs):
        """Overload to plotting.showmap that shows spatial information color-coded by time.
        """
        temp_df = self.georeference.spacetime.assign(Data=1)
        maps.showmap(temp_df, **kwargs)