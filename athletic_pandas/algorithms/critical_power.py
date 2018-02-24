import numpy as np
from scipy.optimize import curve_fit


def extended_5_3_predict(x, power_anaerobic_alactic, power_anaerobic_decay,
                     cp, tau_delay, cp_delay, cp_decay, cp_decay_delay, tau):
    """
    Credits to Damien Grauser. Source:
    https://github.com/GoldenCheetah/GoldenCheetah/blob/master/src/Metrics/ExtendedCriticalPower.cpp
    """
    model = (
        (
            (
                power_anaerobic_alactic
            ) * (
                1.20 - 0.20 * np.exp(-1 * x)
            ) * (
                np.exp(power_anaerobic_decay * x)
            )
        ) + (
            (
                cp
            ) * (
                1 - np.exp(cp_delay * x)
            ) * (
                1 + cp_decay * np.exp(cp_decay_delay / x)
            ) * (
                1 - np.exp(tau_delay * x)
            ) * (
                1 + tau / x
            )
        )
    )

    model = np.nan_to_num(model)
    model[model > 2000] = 0
    model[model < 1] = 0

    return model


def extended_7_3_predict(x, power_anaerobic_alactic, power_anaerobic_decay,
                     cp, tau_delay, cp_delay, cp_decay, cp_decay_delay, tau):
    """
    Credits to Damien Grauser. Source:
    https://github.com/GoldenCheetah/GoldenCheetah/blob/master/src/Metrics/ExtendedCriticalPower.cpp
    """
    model = (
        (
            (
                power_anaerobic_alactic
            ) * (
                (
                    np.exp(power_anaerobic_decay)
                ) * (
                    np.power(x, power_anaerobic_alactic)
                )
            )
        ) + (
            (
                cp * (1 - np.exp(tau_delay * x))
            ) * (
                1 - np.exp(cp_delay * x)
            ) * (
                1 + cp_decay * np.exp(cp_decay_delay / x)
            ) * (
                1 + tau / x
            )
        )
    )

    model = np.nan_to_num(model)
    model[model > 2000] = 0
    model[model < 1] = 0

    return model


def model_fit(max_efforts, time_axis, version='extended_5_3'):
    if version == 'extended_5_3':
        predict_func = extended_5_3_predict
        initial_model_params = np.array([811, -2, 280, -0.9, -0.583, -180, 1.208, -4.8])
        model_param_names = [
            'power_anaerobic_alactic',
            'power_anaerobic_decay',
            'cp',
            'cp_delay',
            'cp_decay',
            'cp_decay_delay',
            'tau',
            'tau_delay'
        ]
    elif version == 'extended_7_3':
        predict_func = extended_7_3_predict
        initial_model_params = np.array([811, -2, 280, -0.9, -0.583, -180, 1.208, -4.8])
        model_param_names = [
            'power_anaerobic_alactic',
            'power_anaerobic_decay',
            'cp',
            'cp_delay',
            'cp_decay',
            'cp_decay_delay',
            'tau',
            'tau_delay'
        ]

    model_params, _ = curve_fit(predict_func, time_axis, max_efforts, initial_model_params)

    return dict(zip(model_param_names, model_params))
