import numpy as np
import pandas as pd
import pytest

from athletic_pandas.algorithms import critical_power, main


@pytest.mark.parametrize('predict_func,version,model_params', [
    (
        critical_power._ecp_predict_5_3,
        'extended_5_3',
        dict(
            power_anaerobic_alactic=-50069.215835935684,
            power_anaerobic_decay=-56.252291794719689,
            cp=461.10854374316568,
            cp_delay=-0.95214799279593743,
            cp_decay=-0.97239480096068875,
            cp_decay_delay=-401.24531894589637,
            tau=0.65413728252995684,
            tau_delay=-23.775957048235664
        )
    ),
    (
        critical_power._ecp_predict_7_3,
        'extended_7_3',
        dict(
            power_anaerobic_alactic=811,
            power_anaerobic_decay=-2.0,
            cp=280.0,
            cp_delay=-1.0073579624642723,
            cp_decay=-0.58299999999999996,
            cp_decay_delay=-180.0,
            tau=1.208,
            tau_delay=-4.7999999999999998
        )
    ),
])
def test_critical_power(predict_func, version, model_params):
    power = pd.Series(range(500))
    mean_max_power = main.mean_max_power(power)
    model = critical_power.critical_power_model(mean_max_power, version=version)
    
    assert model.params == model_params
