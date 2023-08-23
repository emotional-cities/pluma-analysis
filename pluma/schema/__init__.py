from __future__ import annotations

import pickle
import datetime

from dotmap import DotMap
from typing import Union, Optional, Callable

from pluma.schema.outdoor import build_schema

from pluma.sync.ubx2harp import get_clockcalibration_ubx_to_harp_clock
from pluma.sync import ClockRefId

from pluma.stream import StreamType, Stream

from pluma.export import maps
from pluma.export.ogcapi.features import convert_dataset_to_geoframe, export_dataset_to_geojson

from pluma.stream.ubx import UbxStream, _UBX_MSGIDS
from pluma.stream.georeference import Georeference

from pluma.io.path_helper import ComplexPath, ensure_complexpath


class Dataset:

    def __init__(self,
                 root: Union[str, ComplexPath],
                 datasetlabel: str = '',
                 georeference: Georeference = Georeference(),
                 schema: Optional[Callable] = build_schema,
                 ):
        """High level class to represent an entire dataset. Loads and
        contains all the streams and methods for general dataset management.

        Args:
            root (Union[str, Path]): Path to the folder containing the full dataset raw data.
            datasetlabel (str, optional): Descriptive label. Defaults to ''.
        """
        self.rootfolder = ensure_complexpath(root)
        self.datasetlabel = datasetlabel
        self.georeference = georeference
        self.schema = schema
        self.streams = None
        self.has_calibration = False

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
                ubxstream = self.streams.UBX
            except:
                raise ImportError('Could not load Ubx stream.')

        if not(ubxstream.streamtype == StreamType.UBX):
            raise TypeError("Reference must be a UBX Stream")
        else:
            navdata = ubxstream.parseposition(
                event=event,
                calibrate_clock=calibrate_clock)

        self.georeference.from_dataframe(navdata)
        if strip is True:
            self.georeference.strip()
        if calibrate_clock is True:
            self.georeference.clockreference.referenceid =\
                ubxstream.clockreference.referenceid

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
            raise TypeError(f"Invalid type was found. Must be of \
                            {Union[DotMap, Stream]}")

    @staticmethod
    def import_dataset(filename: Union[str, ComplexPath]) -> Dataset:
        path = ensure_complexpath(filename)
        with path.open('rb') as handle:
            return pickle.load(handle)

    def export_dataset(self, filename: Union[str, ComplexPath] = None):
        """Serializes and exports the dataset's streams field as a
        pickle object.

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
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def export_streams(self, filename: Union[str, ComplexPath] = None):
        """Serializes and exports the dataset's streams field as a
        pickle object.

        Args:
            filename (str, optional): Path to save the .pickle file.\
                If None, it will save to Dataset.root. Defaults to None.
        """

        if filename is None:
            path = ensure_complexpath(self.rootfolder)
            path.join('dataset_streams.pickle')
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
            path.join('dataset_streams.pickle')
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
        self.streams = self.schema(
            root=root,
            parent_dataset=self,
            autoload=autoload)

    def calibrate_ubx_to_harp(self,
                              dt_error: float = 0.002,
                              plot_diagnosis: bool = False,
                              r2_min_qc: float = 0.99):
        """Attempts to calibrate the ubx clock to harp clock using\
            the synchronization pulses as a reference.

        Args:
            dt_error (float, optional): Allowed error between the derivative\
                of timestamps detected in the two streams. Defaults to 0.002 seconds.
            plot_diagnosis (bool, optional): If True plots the output of\
                the syncing algorithm. Defaults to False.
            r2_min_qc (float, optional): Quality control parameter.
            If < r2_min_qc, an error will be raised, since it likely\
                results from an automatic correction procedure. Defaults to 0.99.
        """

        model = get_clockcalibration_ubx_to_harp_clock(
                ubx_stream=self.streams.UBX,
                harp_sync=self.streams.BioData.Set.data,
                dt_error=dt_error,
                r2_min_qc=r2_min_qc,
                plot_diagnosis=plot_diagnosis)

        self.streams.UBX.clockreference.set_conversion_model(
            model=model,
            reference_from=ClockRefId.HARP)
        self.has_calibration = True

    def showmap(self, **kwargs):
        """Overload to export.showmap that shows spatial information color-coded by time.
        """
        temp_df = self.georeference.spacetime.assign(Data=1)
        fig = maps.showmap(temp_df, **kwargs)
        return fig

    def add_georeference_and_calibrate(self):
        if self.has_calibration is False:
            self.calibrate_ubx_to_harp(plot_diagnosis=True, dt_error=1)
            self.add_ubx_georeference(event=_UBX_MSGIDS.NAV_HPPOSLLH,
                                    calibrate_clock=True)
            self.has_calibration = True
        else:
            raise AssertionError('Dataset is already been automatically calibrated.')
        
    def to_geoframe(self,
                    sampling_dt: datetime.timedelta = datetime.timedelta(seconds=1),
                    rereference_to_ubx_time: bool = False):
        return convert_dataset_to_geoframe(self, sampling_dt, rereference_to_ubx_time)

    def to_geojson(self,
                   filename,
                   sampling_dt: datetime.timedelta = datetime.timedelta(seconds=1),
                   rereference_to_ubx_time: bool = False):
        export_dataset_to_geojson(self, sampling_dt, rereference_to_ubx_time, filename=filename)
