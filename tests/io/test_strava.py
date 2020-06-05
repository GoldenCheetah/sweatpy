import pytest

import pandas as pd

import sweat
from sweat.io import strava
from .utils import sweatvcr


def test_top_level_import():
    assert sweat.read_strava == strava.read_strava


@sweatvcr.use_cassette()
def test_read_strava():
    activity = sweat.read_strava(
        activity_id="3547667536", access_token="somerandomaccesstoken"
    )

    assert isinstance(activity, pd.DataFrame)
    assert isinstance(activity.index, pd.DatetimeIndex)
    columns = set(
        [
            "elevation",
            "speed",
            "cadence",
            "grade",
            "heartrate",
            "power",
            "temperature",
            "distance",
            "moving",
            "latitude",
            "longitude",
        ]
    )
    assert columns == set(activity.columns.tolist())
