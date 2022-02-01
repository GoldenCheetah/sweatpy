import pandas as pd
import pytest
import sweat
from pandas.api.types import is_numeric_dtype
from sweat.io import gpx
from sweat.examples.utils import FileTypeEnum


def test_top_level_import():
    assert sweat.read_gpx == gpx.read_gpx


@pytest.mark.parametrize(
    "example", [(i) for i in sweat.examples(file_type=FileTypeEnum.gpx, course=False)]
)
def test_read_gpx(example):
    activity = gpx.read_gpx(example.path)

    assert isinstance(activity, pd.DataFrame)
    assert isinstance(activity.index, pd.DatetimeIndex)
    included_data = set(i.value for i in example.included_data)
    assert included_data <= set(activity.columns.to_list())
    for column in [
        "power",
        "cadence",
        "heartrate",
        "elevation",
        "latitude",
        "longitude",
    ]:
        if column in activity.columns:
            assert is_numeric_dtype(activity[column])


@pytest.mark.parametrize(
    "example", [(i) for i in sweat.examples(file_type=FileTypeEnum.gpx, course=True)]
)
def test_read_gpx_course(example):
    course = gpx.read_gpx(example.path)

    assert isinstance(course, pd.DataFrame)
    assert isinstance(course.index, pd.RangeIndex)
    included_data = set(i.value for i in example.included_data)
    assert included_data <= set(course.columns.to_list())
