import pathlib

from fitparse import FitFile
import numpy as np
import pandas as pd

from .utils import remove_duplicate_indices, resample_data, semicircles_to_degrees


def read_fit(fpath, resample: bool = False, interpolate: bool = False) -> pd.DataFrame:
    """This method uses the Python fitparse library to load a FIT file into a Pandas DataFrame.
    It is tested with a Garmin FIT file but will probably work with other FIT files too.
    Columns names are translated to sweat terminology (e.g. "heart_rate" > "heartrate").

    Args:
        fpath: str, file-like or Path object
        resample: whether or not the data frame needs to be resampled to 1Hz
        interpolate: whether or not missing data in the data frame needs to be interpolated

    Returns:
        A pandas data frame with all the data.
    """

    if isinstance(fpath, pathlib.PurePath):
        fpath = fpath.as_posix()

    fitfile = FitFile(fpath)

    records = []
    lap = 0
    session = -1
    for record in fitfile.get_messages():
        if record.mesg_type is None:
            continue

        if record.mesg_type.name == "record":
            values = record.get_values()
            values["lap"] = lap
            values["session"] = session
            records.append(values)
        elif record.mesg_type.name == "lap":
            lap += 1
        elif record.mesg_type.name == "event":
            if record.get_value("event_type") == "start":
                # This happens whens an activity is (manually or automatically) paused or stopped and the resumed
                session += 1
        elif record.mesg_type.name == "sport":
            # @TODO handle this to be able to return metadata
            pass

    fit_df = pd.DataFrame(records)

    fit_df = fit_df.rename(
        columns={
            "heart_rate": "heartrate",
            "position_lat": "latitude",
            "position_long": "longitude",
            "altitude": "elevation",
            "left_right_balance": "left-right balance",
        }
    )

    fit_df["datetime"] = pd.to_datetime(fit_df["timestamp"], utc=True)
    fit_df = fit_df.drop(["timestamp"], axis="columns")
    fit_df = fit_df.set_index("datetime")

    fit_df["latitude"] = semicircles_to_degrees(fit_df["latitude"])
    fit_df["longitude"] = semicircles_to_degrees(fit_df["longitude"])

    fit_df = remove_duplicate_indices(fit_df)

    fit_df = resample_data(fit_df, resample, interpolate)

    return fit_df
