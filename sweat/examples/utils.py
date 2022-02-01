from enum import Enum
from pathlib import Path
from typing import List, Optional

from yaml import load, Loader
from pydantic import BaseModel, parse_obj_as, validator

from sweat.constants import DataTypeEnum


class SportEnum(str, Enum):
    cycling = "cycling"
    running = "running"
    swimming = "swimming"
    rowing = "rowing"
    multisport = "multisport"


class FileTypeEnum(str, Enum):
    fit = "FIT"
    tcx = "TCX"
    gpx = "GPX"


class Sensor(BaseModel):
    name: str
    data_types: List[DataTypeEnum]


class ExampleData(BaseModel):
    description: str = None
    path: Path
    sport: Optional[SportEnum]
    file_type: FileTypeEnum
    recording_device: Optional[str]
    recording_device: Optional[str]
    sensors: Optional[List[Sensor]]
    included_data: Optional[List[DataTypeEnum]]
    laps: Optional[int]
    sessions: Optional[int]
    course: bool = False

    @validator("path")
    def make_path_absolute(cls, v):
        return Path(examples_data_dir(), v)


def examples_dir():
    return Path(".", __file__).parent


def examples_data_dir():
    return Path(examples_dir(), "data")


def examples(*, path=None, file_type=None, sport=None, course=None):
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
        for example in loaded_data:
            if example.path == path:
                return example
        raise ValueError(f'Example data "{path}" not found.')

    if file_type is not None:
        loaded_data = filter(lambda d: d.file_type == file_type, loaded_data)

    if sport is not None:
        loaded_data = filter(lambda d: d.sport == sport, loaded_data)

    if course is not None:
        loaded_data = filter(lambda d: d.course == course, loaded_data)

    return loaded_data
