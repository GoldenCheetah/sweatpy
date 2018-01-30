import numpy as np
from lmfit import Parameters, minimize


def _ecp_predict_5_3(model_params, x):
    model = (
        (
            (
                model_params['power_anaerobic_alactic']
            ) * (
                1.20 - 0.20 * np.exp(-1 * x)
            ) * (
                np.exp(model_params['power_anaerobic_decay'] * x)
            )
        ) + (
            (
                model_params['cp']
            ) * (
                1 - np.exp(model_params['cp_delay'] * x)
            ) * (
                1 + model_params['cp_decay'] * np.exp(model_params['cp_decay_delay'] / x)
            ) * (
                1 - np.exp(model_params['tau_delay'] * x)
            ) * (
                1 + model_params['tau'] / x
            )
        )
    )

    model = np.nan_to_num(model)
    model[model > 2000] = 0
    model[model < 1] = 0

    return model


def _ecp_predict_7_3(model_params, x):
    model = (
        (
            (
                model_params['power_anaerobic_alactic']
            ) * (
                (
                    np.exp(model_params['power_anaerobic_decay'])
                ) * (
                    np.power(x, model_params['power_anaerobic_alactic'])
                )
            )
        ) + (
            (
                model_params['cp'] * (1 - np.exp(model_params['tau_delay'] * x))
            ) * (
                1 - np.exp(model_params['cp_delay'] * x)
            ) * (
                1 + model_params['cp_decay'] * np.exp(model_params['cp_decay_delay'] / x)
            ) * (
                1 + model_params['tau'] / x
            )
        )
    )

    model = np.nan_to_num(model)
    model[model > 2000] = 0
    model[model < 1] = 0

    return model


def _ecp_residual(model_params, x, data, version):
    if version == '5_3':
        model = _ecp_predict_5_3(model_params, x)
    elif version == '7_3':
        model = _ecp_predict_7_3(model_params, x)
    return data - model


def extended_critical_power(mean_max_power, **kwargs):
    """
    Credits to Damien Grauser. Source:
    https://github.com/GoldenCheetah/GoldenCheetah/blob/master/src/Metrics/ExtendedCriticalPower.cpp
    """
    mean_max_power = mean_max_power[:5400]

    time_axis = np.asarray(range(1, len(mean_max_power) + 1))

    # Initial model parameters
    model_params = Parameters()
    model_params.add_many(
        ('power_anaerobic_alactic', kwargs.get('power_anaerobic_alactic', 811)),
        ('power_anaerobic_decay', kwargs.get('power_anaerobic_decay', -2)),
        ('cp', kwargs.get('cp', 280)),
        ('cp_delay', kwargs.get('cp_delay', -0.9)),
        ('cp_decay', kwargs.get('cp_decay', -0.583)),
        ('cp_decay_delay', kwargs.get('cp_delay_decay', -180)),
        ('tau', kwargs.get('tau', 1.208)),
        ('tau_delay', kwargs.get('tau_delay', -4.8)),
    )

    version = kwargs.get('version', '5_3')

    model = minimize(_ecp_residual, model_params, args=(time_axis, mean_max_power, version))

    predictions = _ecp_predict_5_3(model.params, time_axis)

    return predictions
