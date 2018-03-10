"""Calculation of performance metrics that change the shape of stream"""

import numpy as np
import pandas as pd
from sweat.algorithms.streams import rolling_mean, mask_fill, compute_zones
from sweat.utils import cast_array_to_original_type

import logging
logger = logging.getLogger(__name__)


def power_duration_curve(arg, mask=None, value=0.0, **kwargs):
    """Power-Duration Curve

    Compute power duration curve from the power stream. Mask-filter options can be
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


def normalized_power(arg, mask=None, value=0.0, **kwargs):
    """Normalized power

    Parameters
    ----------
    arg : array-like
        Power stream
    mask: array-like of bool, optional
        default=None, which means no masking
    value : number, optional
        Value to use for replacement, default=0.0
    type : {"xPower", "NP}
        Determines calculation method to use, default='xPower'

    Returns
    -------
    number
    """

    if kwargs.get('type', 'NP') == 'xPower':
        _rolling_mean = rolling_mean(arg, window=25, mask=mask, value=value, type='emwa')
    else:
        _rolling_mean = rolling_mean(arg, window=30, mask=mask, value=value)

    if type(_rolling_mean) == list:
        _rolling_mean = np.asarray(_rolling_mean, dtype=np.float)

    rv = np.mean(np.power(_rolling_mean, 4)) ** (1/4)

    return rv


def relative_intensity(norm_power, threshold_power):
    """Relative intensity

    Parameters
    ----------
    norm_power : number
        NP or xPower
    threshold_power : number
        FTP or CP

    Returns
    -------
    float
        IF or RI
    """

    rv = norm_power/threshold_power

    return rv


def stress_score(norm_power, threshold_power, duration):
    """Stress Score

    Parameters
    ----------
    norm_power : number
        NP or xPower
    threshold_power : number
        FTP or CP
    duration : int
        Duration in seconds

    Returns
    -------
    ss:
        TSS or BikeScore
    """

    ss = (duration/3600) * (norm_power/threshold_power)**2 * 100

    return ss
