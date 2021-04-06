import pandas as pd
import pytest
import sweat
from sweat.io import exceptions, fit
from sweat.examples.utils import FileTypeEnum
from fitparse.utils import FitParseError


def test_top_level_import():
    assert sweat.read_fit == fit.read_fit


@pytest.mark.parametrize(
    "example", [(i) for i in sweat.examples(file_type=FileTypeEnum.fit)]
)
def test_read_fit(example):
    activity = fit.read_fit(example.path)

    assert isinstance(activity, pd.DataFrame)
    assert isinstance(activity.index, pd.DatetimeIndex)
    included_data = set(i.value for i in example.included_data)
    assert included_data <= set(activity.columns.to_list())

    assert "lap" in activity.columns
    assert activity["lap"].max() == example.laps - 1

    assert "session" in activity.columns
    assert activity["session"].max() == example.sessions - 1


def test_read_fit_no_fit():
    example_tcx = sweat.examples(path="activity_4078723797.tcx")
    with pytest.raises(exceptions.InvalidFitFile):
        activity = fit.read_fit(example_tcx.path)
