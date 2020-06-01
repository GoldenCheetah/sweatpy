import pandas as pd
import pytest
import sweat
from sweat.io import tcx
from sweat.examples.utils import FileTypeEnum


def test_top_level_import():
    assert sweat.read_tcx == tcx.read_tcx


@pytest.mark.parametrize(
    "example_tcx", [(i) for i in sweat.examples(file_type=FileTypeEnum.tcx)]
)
def test_read_tcx(example_tcx):
    tcx_df = tcx.read_tcx(example_tcx.path)

    assert isinstance(tcx_df, pd.DataFrame)
    assert isinstance(tcx_df.index, pd.DatetimeIndex)
    included_data = set(i.value for i in example_tcx.included_data)
    assert included_data <= set(tcx_df.columns.to_list())
