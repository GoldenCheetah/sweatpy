import pytest
from sweat.io.strava import authorization_header
from sweat.io.strava import stream2dict
from sweat.io.strava import zones2list


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

    assert authorization_header(access_token)==expected


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

    assert stream2dict(stream_list) == expected


def test_zones2list_power(test_zones):

    rv = zones2list(test_zones, type="power")
    expected = [-1, 144, 196, 235, 274, 313, 391, 10000]
    assert rv == expected


def test_zones2list_heart_rate(test_zones):

    rv = zones2list(test_zones, type="heart_rate")
    expected = [-1, 142, 155, 162, 174, 10000]
    assert rv == expected
