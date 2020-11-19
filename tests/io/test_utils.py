import pytest

import pandas as pd

import sweat
from sweat.io import utils


def check_if_sampled_at_1hz(data: pd.Series) -> bool:
    diffs = data.index.to_series().diff()
    diffs = diffs.dropna()  # Delete first nan value
    return (diffs == pd.Timedelta(seconds=1)).all()


@pytest.mark.parametrize(
    "path,sampled_1hz", [("4078723797.fit", True), ("2020-06-01-16-52-40.fit", False),],
)
def test_resample_data(path, sampled_1hz):
    example = sweat.examples(path=path)
    original_data = sweat.read_file(example.path)

    sample_freq_1hz = check_if_sampled_at_1hz(original_data)

    assert sample_freq_1hz == sampled_1hz

    data = utils.resample_data(original_data, resample=False, interpolate=False)

    assert sample_freq_1hz == check_if_sampled_at_1hz(data)

    has_nan_values = original_data["latitude"].isnull().values.any()
    data = utils.resample_data(original_data, resample=True, interpolate=False)

    assert check_if_sampled_at_1hz(data)
    if not sampled_1hz and not has_nan_values:
        assert data.isnull().values.any()

    data = utils.resample_data(original_data, resample=True, interpolate=True)
    assert check_if_sampled_at_1hz(data)
    if not sampled_1hz and not has_nan_values:
        assert not data["latitude"].isnull().values.any()
