from pathlib import Path
from typing import Any, Union
from dotmap import DotMap
from geojson import Point
import frost_sta_client as fsc
from requests import HTTPError
from pluma.export.ogcapi.records import RecordProperties
from pluma.schema import Dataset
from pluma.stream import Stream
from dataclasses import dataclass, field

class SensorThingsProperties:

    def __init__(
            self,
            sensors: Union[list[fsc.Sensor], dict[str, fsc.Sensor]],
            observed_properties: dict[str, fsc.ObservedProperty],
            units: dict[str, fsc.UnitOfMeasurement]
    ) -> None:
        if isinstance(sensors, dict):
            self.sensors = sensors
        else:
            self.sensors = {sensor.name:sensor for sensor in sensors}
        self.observed_properties = observed_properties
        self.units = units

@dataclass
class SensorThingsDataset:
    thing: fsc.Thing
    properties: SensorThingsProperties
    datastreams: list[fsc.Datastream] = field(default_factory=lambda: [])
    historical_locations: list[fsc.HistoricalLocation] = field(default_factory=lambda: [])

def convert_dataset_to_sta(dataset: Dataset, properties: SensorThingsProperties) -> SensorThingsDataset:
    root_path = Path(dataset.rootfolder.path)
    thing = fsc.Thing(
        name = f"{root_path.name.lower()}",
        description = dataset.datasetlabel,
        properties = { "withLocation": True }
    )

    historical_locations = []
    for row in dataset.georeference.spacetime.itertuples():
        time = row.Index
        point = Point((row.Longitude, row.Latitude))
        location = fsc.Location(
            name = "location",
            description = "GPS coordinates of the wearable backpack",
            encoding_type = "application/geo+json",
            location = point
        )
        historical_locations.append(fsc.HistoricalLocation(
            locations = [location],
            time = time.strftime(f"%Y-%m-%dT%H:%M:%S.%fZ"),
            thing = thing
        ))

    datastreams = []
    for stream in recursive_iterate_streams(dataset.streams):
        name = f"{stream.device}_{stream.streamlabel}"
        sensor = properties.sensors.get(name, properties.sensors[stream.device])
        observed_property = properties.observed_properties.get(name, properties.observed_properties[stream.streamlabel])
        unit = properties.units.get(name, properties.units[stream.streamlabel])
        datastreams.append(fsc.Datastream(
            name = name,
            description = stream.streamlabel,
            observation_type = "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            observed_property = observed_property,
            unit_of_measurement = unit,
            sensor = sensor,
            thing = thing
        ))
    return SensorThingsDataset(thing, properties, datastreams, historical_locations)

def create_sta_properties(properties: SensorThingsProperties, service: fsc.SensorThingsService):
    for sensor in properties.sensors.values():
        try_create(sensor, service)
    for observed_property in properties.observed_properties.values():
        try_create(observed_property, service)

def create_sta_entities(sta_dataset: SensorThingsDataset, service: fsc.SensorThingsService):
    service.create(sta_dataset.thing)
    for datastream in sta_dataset.datastreams:
        service.create(datastream)
    for historical_location in sta_dataset.historical_locations:
        service.create(historical_location)

def recursive_iterate_streams(streams):
    for stream in streams.values():
        if isinstance(stream, DotMap):
            yield from recursive_iterate_streams(stream)
        elif isinstance(stream, Stream):
            yield stream

def try_create(entity: Any, service: fsc.SensorThingsService):
    try:
        service.create(entity)
    except HTTPError:
        pass