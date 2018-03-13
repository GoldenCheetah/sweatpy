import numpy as np
import pandas as pd
from sweat.algorithms.metrics.power import (wpk, relative_intensity)


def test_wpk():

    power = [1,2,3]
    weight = 2

    rv = wpk(power, weight)
    expected = [0.5,1.0,1.5]
    assert type(rv) == list
    assert rv == expected

    rv = wpk(np.array(power), weight)
    expected = np.array([0.5, 1.0, 1.5])
    assert type(rv) == np.ndarray
    assert (rv == expected).all()

    rv = wpk(pd.Series(power), weight)
    expected = pd.Series([0.5, 1.0, 1.5])
    assert type(rv) == pd.Series
    assert (rv == expected).all()


def test_relative_intensity():

    norm_power = 300.0
    threshold_power = 300.0

    assert relative_intensity(norm_power, threshold_power) == 1.0

