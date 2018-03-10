import numpy as np
import pandas as pd
from sweat.utils import cast_array_to_original_type


def test_cast_array_to_original_type():

    arg = [0, 0, 0]

    rv = cast_array_to_original_type(np.array(arg), type(arg))
    assert type(rv) == type(arg)

    rv = cast_array_to_original_type(pd.Series(arg), type(arg))
    assert type(rv) == type(arg)

    arg = np.array([0, 0, 0])

    rv = cast_array_to_original_type(list(arg), type(arg))
    assert type(rv) == type(arg)

    rv = cast_array_to_original_type(pd.Series(arg), type(arg))
    assert type(rv) == type(arg)

    arg = pd.Series([0, 0, 0])

    rv = cast_array_to_original_type(list(arg), type(arg))
    assert type(rv) == type(arg)

    rv = cast_array_to_original_type(np.array(arg), type(arg))
    assert type(rv) == type(arg)