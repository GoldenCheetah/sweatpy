import numpy as np
import pandas as pd
from sweat.metrics.power import (wpk, relative_intensity,
                                            stress_score)


def test_wpk():

    power = [1,2,3]
    weight = 2

    rv = wpk(np.array(power), weight)
    expected = np.array([0.5, 1.0, 1.5])
    assert type(rv) == np.ndarray
    assert (rv == expected).all()


def test_relative_intensity():

    norm_power = 300.0
    threshold_power = 300.0

    assert relative_intensity(norm_power, threshold_power) == 1.0


def test_stress_score():

    norm_power = 300.0
    threshold_power = 300.0
    duration = 3600

    assert stress_score(norm_power, threshold_power, duration) == 100.0

