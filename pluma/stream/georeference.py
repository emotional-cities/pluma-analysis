import pandas as pd
import geopandas

import shapely
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

import pluma.plotting.export as plumaexport
class Georeference():

    _georeference_header = ["Seconds", "Longitude", "Latitude", "Elevation"]

    def __init__(self,
                 spacetime: pd.DataFrame = None,
                 time: pd.Series = pd.Series(dtype='datetime64[ns]'),
                 lon: pd.Series = pd.Series(dtype=float),
                 lat: pd.Series = pd.Series(dtype=float),
                 height: pd.Series = pd.Series(dtype=float)) -> None:
        self._spacetime = self._build_spacetime_from_dataframe(spacetime)
        if self._spacetime is None:  # if no spacetime is provided attempt to assemble it individually
            self._time = time
            self._lon = lon
            self._lat = lat
            self._height = height
            self._spacetime = self._build_spacetime_from_series()
        else:
            self._refresh_properties()

    @property
    def spacetime(self):
        return self._spacetime

    @spacetime.setter
    def spacetime(self, df: pd.DataFrame):
        self._spacetime = self._build_spacetime_from_dataframe(df)
        self._refresh_properties()

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, series: pd.Series):
        self._build_spacetime_from_series(time=series)
        self._time = series

    @property
    def longitude(self):
        return self._lon

    @longitude.setter
    def longitude(self, series: pd.Series):
        self._build_spacetime_from_series(lon=series)
        self._lon = series

    @property
    def latitude(self):
        return self._lat

    @latitude.setter
    def latitude(self, series: pd.Series):
        self._build_spacetime_from_series(lat=series)
        self._lat = series

    @property
    def elevation(self):
        return self._height

    @elevation.setter
    def elevation(self, series: pd.Series):
        self._build_spacetime_from_series(height=series)
        self._height = series

    def _build_spacetime_from_dataframe(self, df: pd.DataFrame):
        if df is None:
            return None
        else:
            if self._validate_build_spacetime_from_dataframe(df) is True:
                if not(df.index.name == 'Seconds'):
                    df.set_index("Seconds", inplace=True)
                gdf = geopandas.GeoDataFrame(
                    df, geometry=geopandas.points_from_xy(
                        x=df.Longitude,
                        y=df.Latitude,
                        z=df.Elevation,
                        crs="EPSG:4326"))
                return gdf

    def _validate_build_spacetime_from_dataframe(
         self,
         df: pd.DataFrame) -> bool:
        offset = 0
        if (df.index.name == 'Seconds'):
            offset = 1

        expected = [x for x in Georeference._georeference_header[offset:]]
        got = [x for x in df.columns]

        if not (all(elem in got for elem in expected)):
            raise KeyError(f"Not compatible. Expected {expected}\
                , and got {got}")
        else:
            return True

    def _build_spacetime_from_series(self,
                                     time: pd.Series = None,
                                     lon: pd.Series = None,
                                     lat: pd.Series = None,
                                     height: pd.Series = None):
        # If not input is provided, default to self
        if time is None:
            time = self._time
        if lon is None:
            lon = self._lon
        if lat is None:
            lat = self._lat
        if height is None:
            height = self._height

        if self._validate_build_spacetime_from_series(
             time=time,
             lon=lon,
             lat=lat,
             height=height) is True:

            df = pd.concat(
                            [time, lon, lat, height],
                            axis=1)
            df.columns = Georeference._georeference_header
            self._spacetime = self._build_spacetime_from_dataframe(df)

    def _validate_build_spacetime_from_series(self,
                                              time: pd.Series,
                                              lon: pd.Series,
                                              lat: pd.Series,
                                              height: pd.Series) -> bool:

        if not (time.size == lon.size == lat.size == height.size):
            raise AssertionError("Sizes of input series do not match!")
        return True

    def _refresh_properties(self):
        self._time = self._spacetime.index.to_series()
        self._lon = self._spacetime["Longitude"]
        self._lat = self._spacetime["Latitude"]
        self._height = self._spacetime["Elevation"]

    def from_series(self,
                    time: pd.Series,
                    lon: pd.Series,
                    lat: pd.Series,
                    height: pd.Series):
        if (time is None) or (lon is None) or (lat is None) or (height is None):
            raise ValueError("No inputs can be None.")

        self._build_spacetime_from_series(time=time,
                                          lon=lon,
                                          lat=lat,
                                          height=height)

    def from_dataframe(self, df: pd.DataFrame):
        if (df is None):
            raise ValueError("Input dataframe cannot be None.")
        self.spacetime = self._build_spacetime_from_dataframe(df)

    def strip(self):
        tokeep = Georeference._georeference_header[1:]
        tokeep.append('geometry')
        self.spacetime = self.spacetime.loc[:, self.spacetime.columns.intersection(
            tokeep)]

    def __str__(self) -> str:
        return str(self.spacetime)

    def __repr__(self) -> str:
        return repr(self.spacetime)

    def export_kml(self,
                   export_path:str = "walk.kml",
                   **kwargs):
        plumaexport.export_kml_line(
            df=self.spacetime,
            export_path=export_path,
            **kwargs)
