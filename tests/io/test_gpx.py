import pandas as pd
import pytest
import sweat
from sweat.io import gpx
from sweat.examples.utils import FileTypeEnum


def test_top_level_import():
    assert sweat.read_gpx == gpx.read_gpx


@pytest.mark.parametrize(
    "example_gpx", [(i) for i in sweat.examples(file_type=FileTypeEnum.gpx)]
)
def test_read_gpx(example_gpx):
    gpx_df = gpx.read_gpx(example_gpx.path)

    assert isinstance(gpx_df, pd.DataFrame)
    assert isinstance(gpx_df.index, pd.DatetimeIndex)
    included_data = set(i.value for i in example_gpx.included_data)
    assert included_data <= set(gpx_df.columns.to_list())
