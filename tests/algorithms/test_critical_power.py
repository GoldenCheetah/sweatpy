import numpy as np
import pandas as pd
import pytest

from athletic_pandas.algorithms import critical_power, main


@pytest.mark.parametrize('predict_func,version,expected_model', [
    (
        critical_power._ecp_predict_5_3,
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
        critical_power._ecp_predict_7_3,
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
def test_critical_power(predict_func, version, expected_model):
    power = pd.Series(range(500))
    mean_max_power = main.mean_max_power(power)
    model = critical_power.critical_power_model(
        mean_max_power,
        np.linspace(1, 501, num=500),
        version=version
    )
    
    assert model == expected_model
