import pandas as pd
import pytest
import os
import json
from sweat.io import strava
from sweat.io.models import dataframes


@pytest.fixture
def power():
    return pd.Series(range(100))


@pytest.fixture
def test_stream():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    f_name = os.path.normpath(os.path.join(current_dir,
                                           'fixtures/strava/streams_1202065_1354978421.json'))
    with open(f_name) as f:

        _stream = json.load(f)

        return strava.stream2dict(_stream)


@pytest.fixture
def test_stream_with_nans():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    f_name = os.path.normpath(os.path.join(current_dir,
                                           'fixtures/strava/streams_1202065_1299011495.json'))

    with open(f_name) as f:

        _stream = json.load(f)

        return strava.stream2dict(_stream)


@pytest.fixture
def wdf():
    data = {
        'time': range(10),
        'heartrate': range(10),
        'power': range(10)}
    athlete = dataframes.Athlete(name='Chris', weight=80, ftp=300)
    wdf = dataframes.WorkoutDataFrame(data)
    wdf = wdf.set_index('time')
    wdf.athlete = athlete
    return wdf


@pytest.fixture
def wdf_small():

    athlete = dataframes.Athlete(cp=200, w_prime=20000)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    wdf = dataframes.WorkoutDataFrame(
        pd.read_csv(os.path.join(current_dir, 'fixtures/workout_1_short.csv'))
    )
    wdf = wdf.set_index('time')
    wdf.athlete = athlete
    return wdf


@pytest.fixture
def wdf_big():
    athlete = dataframes.Athlete(cp=200, w_prime=20000, weight=80)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    wdf = dataframes.WorkoutDataFrame(
        pd.read_csv(os.path.join(current_dir, 'fixtures/workout_1.csv'))
    )
    wdf = wdf.set_index('time')
    wdf.athlete = athlete
    return wdf
