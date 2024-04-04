from dotmap import DotMap
import frost_sta_client as fsc
from pluma.export.ogcapi.records import RecordProperties
from pluma.schema import Dataset
from pluma.stream import Stream
from itertools import groupby

def export_dataset_to_sta(dataset: Dataset, properties: RecordProperties) -> fsc.Thing:
    thing = fsc.Thing(
        name = properties.title,
        description = properties.description
    )
    
    datastreams = []
    for device_name, device_streams in groupby(
        recursive_iterate_streams(dataset.streams),
        lambda s: s.device):
        sensor = fsc.Sensor(name = device_name)
        for stream in device_streams:
            datastreams.append(fsc.Datastream(
                name = stream.streamlabel,
                description = stream.description,
                sensor = sensor,
                thing = thing
            ))
    thing.datastreams = datastreams
    return thing

def recursive_iterate_streams(streams):
    for stream in streams.values():
        if isinstance(stream, DotMap):
            yield from recursive_iterate_streams(stream)
        elif isinstance(stream, Stream):
            yield stream