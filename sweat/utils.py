import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def cast_array_to_original_type(arg, arg_type):
    """Cast array to another array-like type

    Parameters
    ----------
    arg: array-like {list, ndarray, pd.Series}
    arg_type: type

    Returns
    -------
    casted : arg_type array-like
    """

    if arg_type == list:
        return list(arg)

    elif arg_type == np.ndarray:
        return np.array(arg)

    elif arg_type == pd.Series:
        return pd.Series(arg)

    else:
        raise ValueError("arg_type must be list, ndarray or pd.Series")
