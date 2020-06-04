import pandas as pd
import pytest
import sweat
from sweat.io import tcx
from sweat.examples.utils import FileTypeEnum


def test_top_level_import():
    assert sweat.read_tcx == tcx.read_tcx


@pytest.mark.parametrize(
    "example", [(i) for i in sweat.examples(file_type=FileTypeEnum.tcx)]
)
def test_read_tcx(example):
    activity = tcx.read_tcx(example.path)

    assert isinstance(activity, pd.DataFrame)
    assert isinstance(activity.index, pd.DatetimeIndex)
    included_data = set(i.value for i in example.included_data)
    assert included_data <= set(activity.columns.to_list())

    assert "lap" in activity.columns
    assert activity["lap"].max() == example.laps - 1

    assert "session" in activity.columns
    assert activity["session"].max() == example.sessions - 1
