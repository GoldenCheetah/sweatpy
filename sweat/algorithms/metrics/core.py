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

