from enum import Enum
from pathlib import Path
from typing import List

from yaml import load, Loader
from pydantic import BaseModel, parse_obj_as, validator


class SportEnum(str, Enum):
    cycling = "cycling"
    running = "running"
    swimming = "swimming"


class FileTypeEnum(str, Enum):
    fit = "FIT"
    tcx = "TCX"
    gpx = "GPX"


class DataTypeEnum(str, Enum):
    latitude = "latitude"
    longitude = "longitude"
    speed = "speed"
    power = "power"
    left_right_balance = "left-right balance"
    elevation = "elevation"
    cadence = "cadence"
    heartrate = "heartrate"
    temperature = "temperature"
    distance = "distance"


class Sensor(BaseModel):
    name: str
    data_types: List[DataTypeEnum]


class ExampleData(BaseModel):
    description: str = None
    path: Path
    sport: SportEnum
    file_type: FileTypeEnum
    recording_device: str
    recording_device: str
    sensors: List[Sensor] = None
    included_data: List[DataTypeEnum]

    @validator("path")
    def make_path_absolute(cls, v):
        return Path(examples_data_dir(), v)


def examples_dir():
    return Path(".", __file__).parent


def examples_data_dir():
    return Path(examples_dir(), "data")


def examples(*, path=None, file_type=None, sport=None):
    if path is not None and (file_type is not None or sport is not None):
        raise ValueError(
            "Providing both the path argument and one or more of file_type and sport is not supported."
        )

    with Path(examples_dir(), "index.yml").open("r") as f:
        index = load(f, Loader=Loader)
    loaded_data = parse_obj_as(List[ExampleData], index)

    if path is not None:
        example_data_dir = examples_data_dir()
        path = Path(example_data_dir, path)
        for example in examples():
            if example.path == path:
                return example
        raise ValueError(f'Example data "{path}" not found.')

    if file_type is not None:
        loaded_data = filter(lambda d: d.file_type == file_type, examples())

    if sport is not None:
        loaded_data = filter(lambda d: d.sport == sport, examples())

    return loaded_data
