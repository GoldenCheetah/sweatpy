import pathlib

from fitparse import FitFile
import numpy as np
import pandas as pd


def read_fit(fpath):
    """
    This method uses the Python fitparse library to load a FIT file into a Pandas DataFrame.
    It is tested with a Garmin FIT file but will probably work with other FIT files too.
    Columns names are translated to sweat terminology (e.g. "heart_rate" > "heartrate").

    Parameters
    ----------
    fpath : str, file-like or Path object

    Returns
    -------
    fit_df : Pandas DataFrame
    """

    if isinstance(fpath, pathlib.PurePath):
        fpath = fpath.as_posix()

    fitfile = FitFile(fpath)

    records = []
    for record in fitfile.get_messages("record"):
        records.append(record.get_values())

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

    fit_df.index = (fit_df["timestamp"] - fit_df["timestamp"][0]) / np.timedelta64(
        1, "s"
    )
    fit_df.index = fit_df.index.astype(int)

    return fit_df
