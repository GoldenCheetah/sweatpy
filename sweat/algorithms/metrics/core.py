import numpy as np
import pandas as pd
from sweat.utils import cast_array_to_original_type


def mask_fill(arg, mask=None, value=0.0, **kwargs):
    """Replace masked values

    Parameters
    ----------
    arg : array-like
    mask : array-like of bools, optional
        Default value is None, which means no masking will be applied
    value : number, optional
        Value to use for replacement, default=0.0

    Returns
    -------
    y: type of input argument


    In case the arg is an ndarray all operations will be performed on the original array.
    To preserve original array pass a copy to the function
    """

    if mask is None:
        return arg

    y = np.array(arg)

    mask = np.array(mask, dtype=bool)
    y[~mask] = value

    rv = cast_array_to_original_type(y, type(arg))

    return rv



def rolling_mean(arg, window=10, mask=None, value=0.0, **kwargs):
    """Compute rolling mean

    Compute *uniform* or *ewma* rolling mean of the stream. In-process masking with replacement is
    controlled by optional keyword parameters

    Parameters
    ----------
    arg : array-like
    window : int
        Size of the moving window in sec, default=10
    mask : array-like of boolean, optional
        Default value is None, which means no masking will be applied
    value : number, optional
        Value to use for replacement, default=0.0
    type : {"uniform", "emwa"}, optional
        Type of averaging, default="uniform"

    Returns
    -------
    y: type of input argument

    The moving array will indicate which samples to set to zero before
    applying rolling mean.
    """
    if mask is not None:
        arg = mask_fill(arg, mask, value, **kwargs)

    y = pd.Series(arg)

    if kwargs.get('type', 'uniform') == 'ewma':
        y = y.ewm(span=window, min_periods=1).mean().values
    else:
        y = y.rolling(window, min_periods=1).mean().values

    y = cast_array_to_original_type(y, type(arg))

    return y


def median_filter(arg, window=31, threshold=1, value=None, **kwargs):
    """Outlier replacement using median filter

    Detect outliers using median filter and replace with rolling median or specified value

    Parameters
    ----------
    arg : array-like
    window : int, optional
        Size of window (including the sample; default=31 is equal to 15 on either side of value)
    threshold : number, optional
        default=3 and corresponds to 2xSigma
    value : float, optional
        Value to be used for replacement, default=None, which means replacement by rolling median value

    Returns
    -------
    y: type of input argument

    In case the arg is an ndarray all operations will be performed on the original array.
    To preserve original array pass a copy to the function
    """
    y = pd.Series(arg)

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

    y = y.as_matrix()

    y = cast_array_to_original_type(y, type(arg))

    return y


# FTP based 7-zones with left bind edge set to -0.001
POWER_ZONES_THRESHOLD = [-0.001, 0.55, 0.75, 0.9, 1.05, 1.2, 1.5, 10.0]
POWER_ZONES_THRESHOLD_DESC = ["Active Recovery", "Endurance", "Tempo",
                              "Threshold", "VO2Max", "Anaerobic", "Neuromuscular",]
POWER_ZONES_THRESHOLD_ZNAME = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7"]

# LTHR based 5-zones with left bind edge set to -0.001
HEART_RATE_ZONES = [-0.001, 0.68, 0.83, 0.94, 1.05, 10.0]
HEART_RATE_ZONES_DESC = ["Active recovery", "Endurance", "Tempo", "Threshold", "VO2Max",]
HEART_RATE_ZONES_ZNAME = ["Z1", "Z2", "Z3", "Z4", "Z5"]


def compute_zones(arg, **kwargs):
    """Convert stream into respective zones stream

    Watts streams can be converted either into ftp based 7-zones or into custom zones
    HR streams can be converted either in lthr based 5-zones or into custom zones
    One of three *ftp*, *lthr* or *zone* keyword parameters must be provided

    Parameters
    ----------
    arg : array-like
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

    arg_s = pd.Series(arg)

    if kwargs.get('zones', None):
        abs_zones = kwargs.get('zones')

    elif kwargs.get('ftp', None):
        abs_zones = np.asarray(POWER_ZONES_THRESHOLD) * kwargs.get('ftp')

    elif kwargs.get('lthr', None):
        abs_zones = np.asarray(HEART_RATE_ZONES) * kwargs.get('lthr')

    else:
        raise ValueError

    labels = kwargs.get('labels', list(range(1, len(abs_zones))))
    assert len(abs_zones) == (len(labels) + 1)

    y = pd.cut(arg_s, bins=abs_zones, labels=labels)
    y = cast_array_to_original_type(y, type(arg))

    return y


def best_interval(arg, window, mask=None, value=0.0, **kwargs):
    """Compute best interval of the stream

    Masking with replacement is controlled by keyword arguments

    Parameters
    ----------
    arg: array-like
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

    y = rolling_mean(arg, window=window, mask=mask, value=value, **kwargs)

    rv = np.max(y)

    return rv


def time_in_zones(arg, **kwargs):
    """Time in zones

    Calculate time [sec] spent in each zone

    Parameters
    ----------
    arg : array-like, power or heartrate
    kwargs : see zones

    Returns
    -------
    array-like, the same type as arg
    """
    type_arg = type(arg)
    z = pd.Series(compute_zones(arg, **kwargs))
    tiz = z.groupby(z).count()
    rv = cast_array_to_original_type(tiz, type_arg)

    return rv


def weighted_average_power(arg, mask=None, value=0.0, **kwargs):
    """Weighted average power

    Parameters
    ----------
    arg : array-like
        Power stream
    mask: array-like of bool, optional
        default=None, which means no masking
    value : number, optional
        Value to use for replacement, default=0.0
    type : {"WAP", "xPower"}
        Determines calculation method to use, default='WAP'

    Returns
    -------
    number
    """

    if kwargs.get('type', 'WAP') == 'xPower':
        _rolling_mean = rolling_mean(arg, window=25, mask=mask, value=value, type='emwa')
    else:
        _rolling_mean = rolling_mean(arg, window=30, mask=mask, value=value)

    if type(_rolling_mean) == list:
        _rolling_mean = np.asarray(_rolling_mean, dtype=np.float)

    rv = np.mean(np.power(_rolling_mean, 4)) ** (1/4)

    return rv


def mean_max(arg, mask=None, value=0.0, **kwargs):
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
    rv : type of input argument
        Power-Duration Curve
    """

    y = mask_fill(arg, mask=mask, value=value)
    y = pd.Series(y)

    # Compute the accumulated energy from the power data
    energy = y.cumsum()

    # Compute the maximum sustainable power using the difference in energy
    # This method is x4 faster than using rolling mean
    y = np.array([])
    for t in np.arange(1, len(energy)):
        y = np.append(y, energy.diff(t).max()/(t))
    y = cast_array_to_original_type(y, type(arg))

    return y