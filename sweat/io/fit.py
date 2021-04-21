import json
import pathlib
from functools import lru_cache

import numpy as np
import pandas as pd
from fitparse import FitFile
from fitparse.utils import FitHeaderError

from .exceptions import InvalidFitFile
from .utils import (
    create_empty_dataframe,
    remove_duplicate_indices,
    resample_data,
    semicircles_to_degrees,
)


def process_location_columns(df, columns=None):
    if columns is None:
        columns = [
            c
            for c in df.columns
            if isinstance(c, str) and (c.endswith("_lat") or c.endswith("_long"))
        ]
    else:
        columns = [c for c in columns if c in df.columns]

    for column in columns:
        df[column] = semicircles_to_degrees(df[column])

    return df


def process_summaries(summaries):
    summaries = pd.DataFrame(summaries)

    if summaries.empty:
        return summaries

    for dt_column in summaries.select_dtypes(include=["datetime64"]).columns:
        summaries[dt_column] = summaries[dt_column].dt.tz_localize("UTC")
    summaries = summaries.sort_values(by="start_time").reset_index()

    summaries = process_location_columns(summaries)

    return summaries


def read_fit(
    fpath,
    resample: bool = False,
    interpolate: bool = False,
    hrv: bool = False,
    pool_lengths: bool = False,
    summaries: bool = False,
    metadata: bool = False,
    raw_messages: bool = False,
    fitparse_kwargs=None,
) -> pd.DataFrame:
    """This method uses the Python fitparse library to load a FIT file into a Pandas DataFrame.
    It is tested with a Garmin FIT file but will probably work with other FIT files too.
    Columns names are translated to sweat terminology (e.g. "heart_rate" > "heartrate").

    Args:
        fpath: str, file-like or Path object
        resample: whether or not the data frame needs to be resampled to 1Hz
        interpolate: whether or not missing data in the data frame needs to be interpolated
        hrv: whether to return hrv data. Note: If set to True this method will return a dictionairy instead of a data frame.
        pool_lengths: whether to return pool length data. Note: If set to True this method will return a dictionairy with a "pool_lengths" key instead of a data frame.
        summaries: whether to return session summary data. Note: If set to True this method will return a dictionairy instead of a data frame.
        metadata: whether to return metadata. Note: If set to True this method will return a dictionairy instead of a data frame.
        fitparse_kwargs: keyword arguments to pass the the python-fitparse FitFile class. Defaults to {"check_crc": False}
        raw_messages: Whether to return the raw FIT messages as a list of dictionaries. If set to True this method will return a dictionairy with a "raw_messages" key instead of a data frame.

    Returns:
        A pandas data frame with all the data or a dictionairy when either hrv, summaries or metadata are True.
    """

    if isinstance(fpath, pathlib.PurePath):
        fpath = fpath.as_posix()

    default_fitparse_kwargs = {"check_crc": False}
    if fitparse_kwargs is None:
        fitparse_kwargs = default_fitparse_kwargs
    else:
        # Merge default and provided fitparse_kwargs. Provided take precedence.
        fitparse_kwargs = {**default_fitparse_kwargs, **fitparse_kwargs}

    try:
        fitfile = FitFile(fpath, **fitparse_kwargs)
    except FitHeaderError as e:
        raise InvalidFitFile(f"Invalid FIT file: {str(e)}")

    session_summaries = []
    lap_summaries = []
    activity_summary = {}
    devices = {}
    records = []
    sport = None
    rr_intervals = []
    pool_length_records = []
    raw_message_records = []
    record_sequence = 0
    for record in fitfile.get_messages():
        try:
            mesg_type = record.mesg_type.name
        except AttributeError:
            continue

        if raw_messages:
            raw_message_records.append(record.get_values())

        if mesg_type == "record":
            values = record.get_values()
            values["sport"] = sport
            values["record_sequence"] = record_sequence
            records.append(values)
            record_sequence += 1
        elif mesg_type == "device_info":
            device = record.get_values()
            serial_number = device.get("serial_number", None)
            if serial_number is not None:
                devices[serial_number] = device
            continue
        elif mesg_type == "file_id":
            continue
        elif mesg_type == "file_creator":
            continue
        elif mesg_type == "device_settings":
            continue
        elif mesg_type == "user_profile":
            continue
        elif mesg_type == "zones_target":
            continue
        elif mesg_type == "developer_data_id":
            continue
        elif mesg_type == "field_description":
            continue
        elif mesg_type == "activity":
            activity_summary = record.get_values()
        elif mesg_type == "lap":
            lap_summaries.append(record.get_values())
        elif mesg_type == "event":
            if record.get_value("event_type") == "start":
                # This happens whens an activity is (manually or automatically) paused or stopped and the resumed
                # @TODO Decide how to handle this with respect to laps and sessions
                continue
        elif mesg_type == "sport":
            sport = record.get_value("sport")
        elif mesg_type == "hrv":
            if hrv:
                values = record.get_values()["time"]
                for val in values:
                    if val is not None:
                        rr_intervals.append(val)
        elif mesg_type == "hr":
            # @TODO Decide wether to use these
            continue
        elif mesg_type == "session":
            session_summaries.append(record.get_values())
        elif mesg_type == "length":
            if pool_lengths:
                pool_length_records.append(record.get_values())
        else:
            continue

    fit_df = pd.DataFrame(records)

    session_summaries = process_summaries(session_summaries)
    lap_summaries = process_summaries(lap_summaries)

    if fit_df.empty:
        fit_df = create_empty_dataframe()
    else:
        fit_df = fit_df.rename(
            columns={
                "heart_rate": "heartrate",
                "position_lat": "latitude",
                "position_long": "longitude",
                "altitude": "elevation",
                "left_right_balance": "left-right balance",
            }
        )

        # Postprocessing fit_df
        fit_df["datetime"] = pd.to_datetime(fit_df["timestamp"], utc=True)
        fit_df = fit_df.drop(["timestamp"], axis="columns")
        fit_df = fit_df.set_index("datetime")
        fit_df = fit_df.sort_index()

        if "left-right balance" in fit_df.columns:
            try:
                fit_df["left-right balance"] = pd.to_numeric(
                    fit_df["left-right balance"]
                )
            except ValueError:
                # Weird issue with some fit files
                fit_df.loc[
                    fit_df["left-right balance"] == "right", "left-right balance"
                ] = np.nan
                fit_df["left-right balance"] = pd.to_numeric(
                    fit_df["left-right balance"]
                )

            # Source: https://www.thisisant.com/forum/viewthread/6445/#7097
            fit_df["right balance"] = fit_df["left-right balance"] - 128
            fit_df["left balance"] = 100 - fit_df["right balance"]

        fit_df = process_location_columns(fit_df, columns=["latitude", "longitude"])

        fit_df["session"] = 0
        fit_df["lap"] = 0
        session_end = pd.Timestamp.max.tz_localize("UTC")
        if not session_summaries.empty:
            for session, session_start in (
                session_summaries["start_time"].sort_index(ascending=False).iteritems()
            ):
                fit_df.loc[
                    (fit_df.index >= session_start) & (fit_df.index < session_end),
                    "session",
                ] = session

                if not lap_summaries.empty:
                    laps_in_session = lap_summaries.loc[
                        (lap_summaries["start_time"] >= session_start)
                        & (lap_summaries["start_time"] < session_end)
                    ].reset_index()
                    lap_end = session_end
                    for lap, lap_start in (
                        laps_in_session["start_time"]
                        .sort_index(ascending=False)
                        .iteritems()
                    ):
                        fit_df.loc[
                            (fit_df.index >= lap_start) & (fit_df.index < lap_end),
                            "lap",
                        ] = lap
                        lap_end = lap_start

                session_end = session_start

        fit_df = remove_duplicate_indices(fit_df)

        fit_df = resample_data(fit_df, resample, interpolate)

    if (
        not hrv
        and not pool_lengths
        and not summaries
        and not metadata
        and not raw_messages
    ):
        return fit_df

    return_value = {
        "data": fit_df,
    }

    if hrv:
        return_value["hrv"] = pd.Series(rr_intervals, name="RR interval")

    if pool_lengths:
        pool_length_df = pd.DataFrame(pool_length_records)
        if not pool_length_df.empty:
            pool_length_df["datetime"] = pd.to_datetime(
                pool_length_df["start_time"], utc=True
            )
            # pool_length_df = pool_length_df.drop(["timestamp"], axis="columns")
            pool_length_df = pool_length_df.set_index("datetime")
        return_value["pool_lengths"] = pool_length_df

    if summaries:
        return_value["sessions"] = session_summaries
        return_value["laps"] = lap_summaries
        return_value["activity"] = activity_summary

    if metadata:
        return_value["devices"] = devices

    if raw_messages:
        return_value["raw_messages"] = raw_message_records

    return return_value


def _fit_profile_json_path():
    current_dir = pathlib.Path(__file__).parent
    return pathlib.Path(current_dir, "fit_profile.json")


def _import_fit_profile(fname):
    """
    Helper function to create a JSON file from the Profile.xlsx that is included in the GGarmin FIT SDK (https://developer.garmin.com/fit/download/).
    """
    profile_types = pd.read_excel(fname, sheet_name="Types")

    profile_types["Type Name"] = profile_types["Type Name"].ffill()
    profile_types["Base Type"] = profile_types["Base Type"].ffill()
    profile_types = profile_types.dropna(axis="rows", subset=["Value Name"])

    profile = {}
    for type_name, group in profile_types.groupby("Type Name"):
        group = group.set_index("Value Name")
        group = group.drop(labels=["Type Name"], axis="columns")
        profile[type_name] = group.to_dict(orient="index")

    fpath = _fit_profile_json_path()
    with fpath.open("w") as fit_profile_file:
        json.dump(profile, fit_profile_file)


lru_cache(maxsize=32)


def load_fit_profile():
    """
    This methods return the FIT profile types based on the Profile.xslx that is included in the Garmin FIT SDK (https://developer.garmin.com/fit/download/).
    The returned profile can be used to translate e.g. Garmin product names to their corresponding integer product ids.
    """
    fpath = _fit_profile_json_path()
    with fpath.open("r") as fit_profile_file:
        profile = json.load(fit_profile_file)

    return profile
