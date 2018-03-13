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