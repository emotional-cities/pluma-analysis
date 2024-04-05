from pathlib import Path
from typing import Any, Union
from dotmap import DotMap
import frost_sta_client as fsc
from requests import HTTPError
from pluma.export.ogcapi.records import RecordProperties
from pluma.schema import Dataset
from pluma.stream import Stream
from itertools import groupby
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

def convert_dataset_to_sta(dataset: Dataset, properties: SensorThingsProperties) -> SensorThingsDataset:
    root_path = Path(dataset.rootfolder.path)
    thing = fsc.Thing(
        name = f"{root_path.name.lower()}",
        description = dataset.datasetlabel
    )

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
    return SensorThingsDataset(thing, properties, datastreams)

def create_sta_properties(properties: SensorThingsProperties, service: fsc.SensorThingsService):
    for sensor in properties.sensors.values():
        try_create(sensor, service)
    for observed_property in properties.observed_properties.values():
        try_create(sensor, observed_property)

def create_sta_entities(sta_dataset: SensorThingsDataset, service: fsc.SensorThingsService):
    service.create(sta_dataset.thing)
    for datastream in sta_dataset.datastreams:
        service.create(datastream)

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