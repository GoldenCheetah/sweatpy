import importlib
import sys

import numpy as np
import pandas as pd
import pytest

from sweat import utils
from sweat.metrics import power


@pytest.fixture()
def reload_power_module():
    yield
    key_values = [(key, value) for key, value in sys.modules.items()]
    for key, value in key_values:
        if key.startswith('sweat.hrm') or key.startswith('sweat.pdm') or key.startswith('sweat.metrics'):
            importlib.reload(value)


def test_enable_type_casting_module(reload_power_module):
    pwr = [1, 2, 3]
    wap = [1, 2, 3]
    weight = 80
    threshold_power = 80

    assert isinstance(power.wpk(np.asarray(pwr), weight), np.ndarray)
    assert isinstance(power.relative_intensity(np.asarray(wap), threshold_power), np.ndarray)

    with pytest.raises(TypeError):
        power.wpk(pwr, weight)

    with pytest.raises(TypeError):
        power.relative_intensity(wap, threshold_power)
    
    doc_string = power.wpk.__doc__
    utils.enable_type_casting(power)

    assert isinstance(power.wpk(pwr, weight), list)
    assert isinstance(power.wpk(pd.Series(pwr), weight), pd.Series)
    assert isinstance(power.wpk(np.asarray(pwr), weight), np.ndarray)

    assert isinstance(power.relative_intensity(wap, threshold_power), list)
    assert isinstance(power.relative_intensity(pd.Series(wap), threshold_power), pd.Series)
    assert isinstance(power.relative_intensity(np.asarray(wap), threshold_power), np.ndarray)

    assert power.wpk.__doc__ == doc_string

def test_enable_type_casting_func(reload_power_module):
    pwr = [1, 2, 3]
    wap = [1, 2, 3]
    weight = 80
    threshold_power = 80

    assert isinstance(power.wpk(np.asarray(pwr), weight), np.ndarray)
    assert isinstance(power.relative_intensity(np.asarray(wap), threshold_power), np.ndarray)

    with pytest.raises(TypeError):
        power.wpk(pwr, weight)

    with pytest.raises(TypeError):
        power.relative_intensity(wap, threshold_power)
    
    doc_string = power.wpk.__doc__
    wpk = utils.enable_type_casting(power.wpk)

    assert isinstance(wpk(pwr, weight), list)
    assert isinstance(wpk(pd.Series(pwr), weight), pd.Series)
    assert isinstance(wpk(np.asarray(pwr), weight), np.ndarray)

    with pytest.raises(TypeError):
        power.relative_intensity(wap, threshold_power)

    assert power.wpk.__doc__ == doc_string


def test_enable_type_casting_all(reload_power_module):
    pwr = [1, 2, 3]
    wap = [1, 2, 3]
    weight = 80
    threshold_power = 80

    assert isinstance(power.wpk(np.asarray(pwr), weight), np.ndarray)
    assert isinstance(power.relative_intensity(np.asarray(wap), threshold_power), np.ndarray)

    with pytest.raises(TypeError):
        power.wpk(pwr, weight)

    with pytest.raises(TypeError):
        power.relative_intensity(wap, threshold_power)
    
    doc_string = power.wpk.__doc__
    utils.enable_type_casting()

    assert isinstance(power.wpk(pwr, weight), list)
    assert isinstance(power.wpk(pd.Series(pwr), weight), pd.Series)
    assert isinstance(power.wpk(np.asarray(pwr), weight), np.ndarray)

    assert isinstance(power.relative_intensity(wap, threshold_power), list)
    assert isinstance(power.relative_intensity(pd.Series(wap), threshold_power), pd.Series)
    assert isinstance(power.relative_intensity(np.asarray(wap), threshold_power), np.ndarray)

    assert power.wpk.__doc__ == doc_string


def test_enable_type_casting_error():
    with pytest.raises(ValueError):
        utils.enable_type_casting('covfefe')
