import isodate
import pandas as pd
from pathlib import Path
from geopandas import GeoDataFrame
from datetime import datetime

from pluma.schema import Dataset

class MetadataRecord:
    def __init__(self, dataset: Dataset, gdf: GeoDataFrame) -> None:
        root_path = Path(dataset.rootfolder.path)
        self.id = f"{root_path.name}.geojson"
        self.start_date = gdf.index[0]
        self.end_date = gdf.index[-1]
        self.created_timestamp = pd.Timestamp(datetime.utcnow())
        self.updated_timestamp = self.created_timestamp
        self.resolution = isodate.duration_isoformat(pd.Timedelta(gdf.index.freq))
        self.bounds = gdf.total_bounds
        self.crs = gdf.crs

    def to_json(self) -> str:
        return ""