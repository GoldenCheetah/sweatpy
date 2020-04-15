import pandas as pd


def wpk(power, weight):
    """Watts per kilo

    Parameters
    ----------
    power : ndarray
    weight : number

    Returns
    -------
    array-like
    """

    return power / weight


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

    ss = (duration / 3600) * (wap / threshold_power) ** 2 * 100

    return ss
