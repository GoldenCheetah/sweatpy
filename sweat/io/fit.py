from fitparse import FitFile
import numpy as np

from .models import dataframes


def load(fname):
    """
    This method uses the Python fitparse library to load a FIT file into a WorkoutDataFrame.
    It is tested with a Garmin FIT file but will probably work with other FIT files too.
    Columns names are translated to sweat terminology (e.g. "heart_rate" > "heartrate").

    Parameters
    ----------
    fname : str

    Returns
    -------
    wdf : WorkoutDataFrame
    """

    fitfile = FitFile(fname)

    records = []
    for record in fitfile.get_messages("record"):
        records.append(record.get_values())

    wdf = dataframes.WorkoutDataFrame(records)

    wdf = wdf.rename(columns={"heart_rate": "heartrate"})

    wdf.index = (wdf.timestamp - wdf.timestamp[0]) / np.timedelta64(1, "s")
    wdf.index = wdf.index.astype(int)

    return wdf
