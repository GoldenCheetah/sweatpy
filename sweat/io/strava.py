from datetime import timedelta

import pandas as pd
from stravalib.client import Client

from .utils import resample_data


STREAM_TYPES = [
    "time",
    "latlng",
    "distance",
    "altitude",
    "velocity_smooth",
    "heartrate",
    "cadence",
    "watts",
    "temp",
    "moving",
    "grade_smooth",
]

COLUMN_TRANSLATIONS = {
    "altitude": "elevation",
    "velocity_smooth": "speed",
    "watts": "power",
    "temp": "temperature",
    "grade_smooth": "grade",
}


def read_strava(
    activity_id: int,
    access_token: str,
    refresh_token: str = None,
    client_id: int = None,
    client_secret: str = None,
    resample: bool = False,
    interpolate: bool = False,
) -> pd.DataFrame:
    """This method lets you retrieve activity data from Strava.
    Columns names are translated to sweat terminology (e.g. "heart_rate" > "heartrate").
    Two API calls are made to the Strava API: 1 to retrieve activity metadata, 1 to retrieve the raw data ("streams").

    Args:
        activity_id: The id of the activity
        access_token: The Strava access token
        refresh_token: The Strava refresh token. Optional.
        client_id: The Strava client id. Optional. Used for token refresh.
        client_secret: The Strava client secret. Optional. Used for token refresh.
        resample: whether or not the data frame needs to be resampled to 1Hz
        interpolate: whether or not missing data in the data frame needs to be interpolated

    Returns:
        A pandas data frame with all the data.
    """
    client = Client()
    client.access_token = access_token
    client.refresh_token = refresh_token

    activity = client.get_activity(activity_id)
    start_datetime = activity.start_date_local

    streams = client.get_activity_streams(
        activity_id=activity_id,
        types=STREAM_TYPES,
        series_type="time",
    )

    raw_data = dict()
    for key, value in streams.items():
        if key == "latlng":
            latitude, longitude = list(zip(*value.data))
            raw_data["latitude"] = latitude
            raw_data["longitude"] = longitude
        else:
            try:
                key = COLUMN_TRANSLATIONS[key]
            except KeyError:
                pass

            raw_data[key] = value.data

    data = pd.DataFrame(raw_data)

    def time_to_datetime(time):
        return start_datetime + timedelta(seconds=time)

    data["datetime"] = data["time"].apply(time_to_datetime)

    data = data.drop(["time"], axis="columns")

    data = data.set_index("datetime")

    data = resample_data(data, resample, interpolate)

    return data
