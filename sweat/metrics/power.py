import pandas as pd
from sweat.utils import cast_array_to_original_type


def wpk(power, weight):
    """Watts per kilo

    Parameters
    ----------
    power : list, ndarray, series
    weight : number

    Returns
    -------
    array-like
    """

    if not isinstance(power, pd.Series):
        y = pd.Series(power)
    else:
        y = power

    rv = y/weight
    rv = cast_array_to_original_type(rv, type(power))

    return rv


def relative_intensity(wap, threshold_power):
    """Relative intensity

    Parameters
    ----------
    wap : number
        WAP or xPower
    threshold_power : number
        FTP or CP

    Returns
    -------
    float
        IF or RI
    """

    rv = wap / threshold_power

    return rv


def stress_score(wap, threshold_power, duration):
    """Stress Score

    Parameters
    ----------
    wap : number
        WAP or xPower
    threshold_power : number
        FTP or CP
    duration : int
        Duration in seconds

    Returns
    -------
    ss
    """

    ss = (duration/3600) * (wap/threshold_power)**2 * 100

    return ss


