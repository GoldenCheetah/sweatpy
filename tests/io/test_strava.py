import pytest
import vcr

from sweat.io import strava


@pytest.fixture
def test_zones():

    rv = {
        'heart_rate': {'custom_zones': True,
                        'zones': [{'max': 142, 'min': 0},
                                  {'max': 155, 'min': 142},
                                  {'max': 162, 'min': 155},
                                  {'max': 174, 'min': 162},
                                  {'max': -1, 'min': 174}]},
             'power': {'zones': [{'max': 143, 'min': 0},
                                 {'max': 195, 'min': 144},
                                 {'max': 234, 'min': 196},
                                 {'max': 273, 'min': 235},
                                 {'max': 312, 'min': 274},
                                 {'max': 390, 'min': 313},
                                 {'max': -1, 'min': 391}]}}

    return rv


def test_authorization_header():

    access_token = 'abc123'
    expected = {'Authorization': 'Bearer abc123'}

    assert strava.authorization_header(access_token)==expected


@vcr.use_cassette('tests/fixtures/strava/test_retrieve_athlete.yaml')
def test_retrieve_athlete():
    access_token = '1234abcd'
    athlete = strava.retrieve_athlete(access_token)

    assert athlete['username'] == 'aart_goossens'
    assert athlete['id'] == 2495424


@vcr.use_cassette('tests/fixtures/strava/test_retrieve_zones.yaml')
def test_retrieve_zones():
    access_token = '1234abcd'
    zones = strava.retrieve_zones(access_token)

    assert 'heart_rate' in zones
    assert len(zones['heart_rate']['zones']) == 5
    assert zones['heart_rate']['zones'][0] == {'min': 0, 'max': 118}
    assert 'power' in zones
    assert len(zones['power']['zones']) == 7
    assert zones['power']['zones'][0] == {'min': 0, 'max': 193}


@vcr.use_cassette('tests/fixtures/strava/test_retrieve_activity.yaml')
def test_retrieve_activity():
    activity_id = 1478313529
    access_token = '1234abcd'
    activity = strava.retrieve_activity(activity_id, access_token)

    assert activity['id'] == activity_id
    assert activity['athlete']['id'] == 2495424
    assert activity['type'] == 'Ride'
    assert activity['average_watts'] == 204.7


@vcr.use_cassette('tests/fixtures/strava/test_retrieve_streams.yaml')
def test_retrieve_streams():
    activity_id = 1478313529
    access_token = '1234abcd'
    streams = strava.retrieve_streams(activity_id, access_token)

    assert list(streams.keys()) == [
        'latlng', 'time', 'distance', 'altitude', 'heartrate', 'cadence',
        'watts', 'temp', 'grade_smooth', 'moving', 'velocity_smooth'
    ]
    assert streams['watts'][1000:1005] == [196, 197, 188, 182, 182]


def test_stream2dict():

    stream_list = [
        {
            "data": [1,2,3],
            "type": "numbers"
        },
        {
            "data": ['a', 'b', 'c'],
            "type": "letters"
        }
    ]

    expected = {
        "numbers": [1, 2, 3],
        "letters": ["a", "b", "c"]
    }

    assert strava.stream2dict(stream_list) == expected


def test_zones2list_power(test_zones):

    rv = strava.zones2list(test_zones, type="power")
    expected = [-1, 144, 196, 235, 274, 313, 391, 10000]
    assert rv == expected


def test_zones2list_heart_rate(test_zones):

    rv = strava.zones2list(test_zones, type="heart_rate")
    expected = [-1, 142, 155, 162, 174, 10000]
    assert rv == expected
