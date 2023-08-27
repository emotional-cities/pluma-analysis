import jinja2
import isodate
import pandas as pd
from pathlib import Path
from geopandas import GeoDataFrame
from datetime import datetime

from pluma.schema import Dataset
from dataclasses import dataclass, field, fields

_env = jinja2.Environment(
    loader=jinja2.PackageLoader("pluma"),
    autoescape=jinja2.select_autoescape)
_template = _env.get_template("metadata_template.j2")

def _format_timestamp(time_utc: datetime) -> str:
    return f"{time_utc.isoformat()}Z"

@dataclass
class Contact:
    name: str
    institution: str
    email: str

@dataclass
class Theme:
    scheme_url: str
    concepts: list[str] = field(default_factory=lambda: [])

@dataclass
class RecordProperties:
    title: str
    description: str
    license: str
    tool: str
    keywords: list[str] = field(default_factory=lambda: [])
    contacts: list[Contact] = field(default_factory=lambda: [])
    themes: list[Theme] = field(default_factory=lambda: [])

class DatasetRecord:
    def __init__(self, dataset: Dataset, gdf: GeoDataFrame, properties: RecordProperties) -> None:
        root_path = Path(dataset.rootfolder.path)
        self.id = f"{root_path.name}.geojson"
        self.start_date = gdf.index[0]
        self.end_date = gdf.index[-1]
        self.created_timestamp = pd.Timestamp(datetime.utcnow())
        self.updated_timestamp = self.created_timestamp
        self.resolution = isodate.duration_isoformat(pd.Timedelta(gdf.index.freq))
        self.bounds = gdf.total_bounds
        self.crs = gdf.crs
        self.properties = properties

    def to_json(self) -> str:
        return _template.render(
            id=self.id,
            start_date=_format_timestamp(self.start_date),
            end_date=_format_timestamp(self.end_date),
            created_timestamp=_format_timestamp(self.created_timestamp),
            updated_timestamp=_format_timestamp(self.updated_timestamp),
            resolution=self.resolution,
            coordinates=[[
                [self.bounds[0], self.bounds[1]],
                [self.bounds[0], self.bounds[3]],
                [self.bounds[2], self.bounds[3]],
                [self.bounds[2], self.bounds[1]],
                [self.bounds[0], self.bounds[1]]
            ]],
            crs=self.crs.to_string(),
            **(dict((field.name, getattr(self.properties, field.name))
                    for field in fields(self.properties))))
