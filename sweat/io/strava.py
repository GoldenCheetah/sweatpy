"""Very thin wrapper around the Strava API v3

    STRAVA_ACCESS_TOKEN must be explicitly provided as an input

    ALL returned values are python objects e.g. dict or list
"""
import requests
import logging

logger = logging.getLogger(__name__)


def retrieve_athlete(access_token):
    """Retrieve current(authenticated) athlete

    API V3: https://strava.github.io/api/v3/athlete/#get-details

    Parameters
    ----------
    access_token : str
        Settings/My API Applications/Your Access Token

    Returns
    -------
    dict
    """

    endpoint_url = "https://www.strava.com/api/v3/athlete"

    r = requests.get(endpoint_url, headers=authorization_header(access_token))

    r.raise_for_status()
    athlete = r.json()

    return athlete


def retrieve_zones(access_token, **kwargs):
    """Retrieve Power and Heartrate zones

    API V3: https://strava.github.io/api/v3/athlete/#zones

    Parameters
    ----------
    access_token : str
        Settings/My API Applications/Your Access Token

    Returns
    -------
    dict
    """

    endpoint_url = "https://www.strava.com/api/v3/athlete/zones"

    r = requests.get(endpoint_url, headers=authorization_header(access_token))

    r.raise_for_status()
    zones = r.json()

    return zones


def retrieve_activity(activity_id, access_token):
    """Retrieve a detailed representation of activity

    API V3: https://strava.github.io/api/v3/activities/#get-details

    Parameters
    ----------
    activity_id: int
    access_token : str
        Settings/My API Applications/Your Access Token

    Returns
    -------
    dict
    """

    endpoint_url = "https://www.strava.com/api/v3/activities/{}".format(activity_id)

    r = requests.get(endpoint_url, headers=authorization_header(access_token))

    r.raise_for_status()
    activity = r.json()

    return activity


def retrieve_streams(activity_id, access_token, **kwargs):
    """Retrieve activity streams

    API V3: https://strava.github.io/api/v3/streams/#activity

    Parameters
    ----------
    activity_id : int
    access_token : str
        Settings/My API Applications/Your Access Token
    type: {None, 'original'}
        Returns serialized original API response if set to 'original'

    Returns
    -------
    streams : list
        Streams are the list of dicts
    """

    types = kwargs.get(
        "types",
        "time,latlng,distance,altitude,velocity_smooth,heartrate,cadence,watts,temp,moving,grade_smooth",
    )

    endpoint_url = "https://www.strava.com/api/v3/activities/{}/streams/{}".format(
        activity_id, types
    )

    r = requests.get(endpoint_url, headers=authorization_header(access_token))

    r.raise_for_status()
    streams = r.json()

    if streams and not kwargs.get("type", None):

        streams = stream2dict(streams)

    return streams


def stream2dict(stream_list):
    """Convert stream list into stream dict

    Parameters
    ----------
    stream_list : list
        Stream in list form (list of dicts), as returned by Strava API v3

    Returns
    -------
    stream_dict : dict
        Stream in dict form, with key set to *stream name* and value set to the actual stream list.
        In this form, the stream is ready to be consumed by pandas
    """

    stream_dict = {}

    for s in stream_list:

        stream_dict.update({s["type"]: s["data"]})

    return stream_dict


def zones2list(zones, type="power"):
    """Convert zones Strava response into a list

    Parameters
    ----------
    zones : dict
        Strava API zones response
    type : {"power", "heart_rate"}

    Returns
    -------
    y : list
        Zones boundaries with left edge set to -1 and right to 10000
    """

    y = [x["min"] for x in zones[type]["zones"]]
    y[0] = -1
    y.append(10000)

    return y


def authorization_header(access_token):
    """Authorization header dict to be used with requests.get()

    Parameters
    ----------
    access_token : str
        Settings/My API Applications/Your Access Token

    Returns
    -------
    header : dict
    """

    rv = {"Authorization": "Bearer {}".format(access_token)}

    return rv
