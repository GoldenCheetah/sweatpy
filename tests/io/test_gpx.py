import pandas as pd
import pytest
import sweat
from sweat.io import gpx
from sweat.examples.utils import FileTypeEnum


def test_top_level_import():
    assert sweat.read_gpx == gpx.read_gpx


@pytest.mark.parametrize(
    "example", [(i) for i in sweat.examples(file_type=FileTypeEnum.gpx)]
)
def test_read_gpx(example):
    activity = gpx.read_gpx(example.path)

    assert isinstance(activity, pd.DataFrame)
    assert isinstance(activity.index, pd.DatetimeIndex)
    included_data = set(i.value for i in example.included_data)
    assert included_data <= set(activity.columns.to_list())
