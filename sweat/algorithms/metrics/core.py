import numpy as np
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
