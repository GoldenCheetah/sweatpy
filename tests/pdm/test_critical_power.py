import numpy as np
import pandas as pd
import pytest

from sweat.pdm import critical_power


@pytest.mark.parametrize('model,expected_params', [
    (
        '2_parameter_non_linear',
        dict(
            cp=200,
            w_prime=10000
        )
    ),
    (
        '3_parameter_non_linear',
        dict(
            cp=199.9999996798856,
            w_prime=10000.000107025966,
            p_max=926323089119.79919
        )
    ),
    (
        'extended_5_3',
        dict(
            power_anaerobic_alactic=811.0,
            power_anaerobic_decay=-2.0,
            cp=280.0,
            cp_delay=-0.90000000000000002,
            cp_decay=-0.58299999999999996,
            cp_decay_delay=-180.0,
            tau=1.208,
            tau_delay=-4.7999999999999998
        )
    ),
    (
        'extended_7_3',
        dict(
            power_anaerobic_alactic=811,
            power_anaerobic_decay=-2.0,
            cp=280.0,
            cp_delay=-0.90000000000000002,
            cp_decay=-0.58299999999999996,
            cp_decay_delay=-180.0,
            tau=1.208,
            tau_delay=-4.7999999999999998
        )
    ),
])
def test_critical_power(model, expected_params):
    time_axis = np.arange(1, 1800, 10)
    max_efforts = 10000 / time_axis + 200
    fitted_params = critical_power.model_fit(
        time_axis,
        max_efforts,
        model=model
    )
    
    assert fitted_params == expected_params
