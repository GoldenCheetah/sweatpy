import pandas as pd
import pytest
import sweat
from sweat.io import fit
from fitparse.utils import FitParseError


def test_top_level_import():
    assert sweat.read_fit == fit.read_fit


def test_read_fit():
    example_fit = sweat.examples(path="4078723797.fit")
    fit_df = fit.read_fit(example_fit.path)

    assert isinstance(fit_df, pd.DataFrame)
    assert "heartrate" in fit_df.columns
    assert "power" in fit_df.columns
    assert "cadence" in fit_df.columns
    assert "distance" in fit_df.columns
    assert fit_df.index.dtype == int
    assert len(fit_df) == 8357


def test_read_fit_no_fit():
    example_tcx = sweat.examples(path="activity_4078723797.tcx")
    with pytest.raises(FitParseError):
        fit_df = fit.read_fit(example_tcx.path)
