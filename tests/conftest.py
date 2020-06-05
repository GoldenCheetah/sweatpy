import pandas as pd
import pytest
import os
import json
from sweat.io import strava


@pytest.fixture
def power():
    return pd.Series(range(100))


@pytest.fixture
def test_stream():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    f_name = os.path.normpath(
        os.path.join(current_dir, "fixtures/strava/streams_1202065_1354978421.json")
    )
    with open(f_name) as f:

        _stream = json.load(f)

        return strava.stream2dict(_stream)


@pytest.fixture
def test_stream_with_nans():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    f_name = os.path.normpath(
        os.path.join(current_dir, "fixtures/strava/streams_1202065_1299011495.json")
    )

    with open(f_name) as f:

        _stream = json.load(f)

        return strava.stream2dict(_stream)
