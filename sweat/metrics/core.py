import numpy as np
import pandas as pd
from collections import namedtuple


def mask_fill(y, mask=None, value=0.0):
    """Replace masked values

    Parameters
    ----------
    y : ndarray
    mask : array-like of bools, optional
        Default value is None, which means no masking will be applied
    value : number, optional
        Value to use for replacement, default=0.0

    Returns
    -------
    y: ndarray

    All operations will be performed on the original array.
    To preserve original array pass a copy to the function
    """

    if mask is None:
        return y

    mask = np.array(mask, dtype=bool)
    y[~mask] = value

    return y


def rolling_mean(y, window=10, mask=None, algorithm="uniform", value=0.0):
    """Compute rolling mean

    Compute *uniform* or *ewma* rolling mean of the stream. In-process masking with replacement is
    controlled by optional keyword parameters

    Parameters
    ----------
    y : ndarray
    window : int
        Size of the moving window in sec, default=10
    mask : array-like of boolean, optional
        Default value is None, which means no masking will be applied
    algorithm : {"uniform", "emwa"}, optional
        Type of averaging, default="uniform"
    value : number, optional
        Value to use for replacement, default=0.0

    Returns
    -------
    y: ndarray

    The moving array will indicate which samples to set to zero before
    applying rolling mean.
    """
    if mask is not None:
        y = mask_fill(y, mask, value)

    y = pd.Series(y)

    if algorithm == "ewma":
        y = y.ewm(span=window, min_periods=1).mean().values
    elif algorithm == "uniform":
        y = y.rolling(window, min_periods=1).mean().values

    return y


def median_filter(y, window=31, threshold=1, value=None):
    """Outlier replacement using median filter

    Detect outliers using median filter and replace with rolling median or specified value

    Parameters
    ----------
    y : ndarray
    window : int, optional
        Size of window (including the sample; default=31 is equal to 15 on either side of value)
    threshold : number, optional
        default=3 and corresponds to 2xSigma
    value : float, optional
        Value to be used for replacement, default=None, which means replacement by rolling median value

    Returns
    -------
    y: ndarray

    All operations will be performed on the original array.
    To preserve original array pass a copy to the function
    """
    y = pd.Series(y)

    rolling_median = y.rolling(window, min_periods=1).median()

    difference = np.abs(y - rolling_median)

    median_abs_deviation = difference.rolling(window, min_periods=1).median()

    outlier_idx = difference > 1.4826 * threshold * median_abs_deviation
    """ The factor 1.4826 makes the MAD scale estimate
        an unbiased estimate of the standard deviation for Gaussian data.
    """

    if value:
        y[outlier_idx] = value
    else:
        y[outlier_idx] = rolling_median[outlier_idx]

    return y.values


# FTP based 7-zones with left bind edge set to -0.001
POWER_ZONES_THRESHOLD = [-0.001, 0.55, 0.75, 0.9, 1.05, 1.2, 1.5, 10.0]
POWER_ZONES_THRESHOLD_DESC = [
    "Active Recovery",
    "Endurance",
    "Tempo",
    "Threshold",
    "VO2Max",
    "Anaerobic",
    "Neuromuscular",
]
POWER_ZONES_THRESHOLD_ZNAME = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7"]

# LTHR based 5-zones with left bind edge set to -0.001
HEART_RATE_ZONES = [-0.001, 0.68, 0.83, 0.94, 1.05, 10.0]
HEART_RATE_ZONES_DESC = [
    "Active recovery",
    "Endurance",
    "Tempo",
    "Threshold",
    "VO2Max",
]
HEART_RATE_ZONES_ZNAME = ["Z1", "Z2", "Z3", "Z4", "Z5"]


def compute_zones(y, zones=None, ftp=None, lthr=None, labels=None):
    """Convert stream into respective zones stream

    Watts streams can be converted either into ftp based 7-zones or into custom zones
    HR streams can be converted either in lthr based 5-zones or into custom zones
    One of three *ftp*, *lthr* or *zone* keyword parameters must be provided

    Parameters
    ----------
    y : ndarray
    ftp : number, optional
        Value for FTP, will be used for 7-zones calculation
    lthr: number, optional
        Value for LTHR, will be used for 5-zones calculation
    zones: list, optional
        List of custom defined zones with left edge set to -1 and right edge to 10000

    Returns
    -------
    array-like of int, the same type as arg
    """

    if zones is not None:
        abs_zones = zones
    elif ftp is not None:
        abs_zones = np.asarray(POWER_ZONES_THRESHOLD) * ftp
    elif lthr is not None:
        abs_zones = np.asarray(HEART_RATE_ZONES) * lthr
    else:
        raise ValueError(
            "One of the keyword arguments [zones, ftp, lthr] must be provided"
        )

    if labels is None:
        labels = list(range(1, len(abs_zones)))
    assert len(abs_zones) == (len(labels) + 1)

    y = pd.cut(y, bins=abs_zones, labels=labels)

    return y


def best_interval(y, window, mask=None, value=0.0):
    """Compute best interval of the stream

    Masking with replacement is controlled by keyword arguments

    Parameters
    ----------
    y: ndarray
    window : int
        Duration of the interval in seconds
    mask : array-like of bool, optional
        default=None, which means no masking
    value : number, optional
        Value to use for replacement, default=0.0

    Returns
    -------
    float
    """

    y = rolling_mean(y, window=window, mask=mask, value=value)

    rv = np.max(y)

    return rv


def time_in_zones(y, **kwargs):
    """Time in zones

    Calculate time [sec] spent in each zone

    Parameters
    ----------
    y : ndarray, power or heartrate
    kwargs : see zones

    Returns
    -------
    ndarray
    """
    z = pd.Series(compute_zones(y, **kwargs))
    tiz = z.groupby(z).count()

    return tiz.values


def weighted_average_power(y, mask=None, algorithm="WAP", value=0.0):
    """Weighted average power

    Parameters
    ----------
    y : ndarray
        Power stream
    mask: array-like of bool, optional
        default=None, which means no masking
    algorithm : {"WAP", "xPower"}
        Determines calculation method to use, default='WAP'
    value : number, optional
        Value to use for replacement, default=0.0

    Returns
    -------
    number
    """

    if algorithm == "WAP":
        _rolling_mean = rolling_mean(y, window=30, mask=mask, value=value)
    elif algorithm == "xPower":
        _rolling_mean = rolling_mean(
            y, window=25, mask=mask, value=value, algorithm="emwa"
        )

    rv = np.mean(np.power(_rolling_mean, 4)) ** (1 / 4)

    return rv


def mean_max(y, mask=None, value=0.0, monotonic=False):
    """Mean-max curve

    Compute mean-max (power duration curve) from the stream. Mask-filter options can be
    added using the keyword arguments.

    Parameters
    ----------
    arg : array-like
        Power stream
    mask: array-like, optional
        Replacement mask (the default is None, which implies no masking)
    value: number, optional
        Value to use as a replacement (the default is 0.0)

    Returns
    -------
    ndarray
    """

    y = mask_fill(y, mask=mask, value=value)
    y = pd.Series(y)

    # Compute the accumulated energy from the power data
    energy = y.cumsum()

    # Compute the maximum sustainable power using the difference in energy
    # This method is x4 faster than using rolling mean
    y = np.array([])
    for t in np.arange(1, len(energy)):
        y = np.append(y, energy.diff(t).max() / (t))

    if monotonic:
        monotonic_y = []
        previous = y[-1]
        for p in np.flip(y):
            if p <= previous:
                monotonic_y.append(previous)
            else:
                monotonic_y.append(p)
                previous = p

        y = np.flip(monotonic_y)

    return y


DataPoint = namedtuple("DataPoint", ["index", "value"])


def multiple_best_intervals(arg, duration, number):
    """Compute multiple best intervals

    TODO: This function should return a list of {'start_index': v, 'stop_index': v, 'index': v, 'value': v}
    Parameters
    ----------
    arg : pd.Stream
    duration : number
    number : int

    Returns
    -------
    ndarray
    """
    moving_average = arg.rolling(duration).mean()
    length = len(moving_average)
    mean_max_bests = []

    for i in range(number):
        if moving_average.isnull().all():
            mean_max_bests.append(DataPoint(np.nan, np.nan))
            continue

        max_value = moving_average.max()
        max_index = moving_average.idxmax()
        mean_max_bests.append(DataPoint(max_index, max_value))

        # Set moving averages that overlap with last found max to np.nan
        overlap_min_index = max(0, max_index - duration)
        overlap_max_index = min(length, max_index + duration)
        moving_average.loc[overlap_min_index:overlap_max_index] = np.nan

    return mean_max_bests
