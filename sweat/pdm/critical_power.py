from collections import OrderedDict

import numpy as np
from scipy.optimize import curve_fit


def two_parameter_non_linear_predict(t, cp, w_prime):
    return cp + w_prime / t


def three_parameter_non_linear_predict(t, cp, w_prime, p_max):
    return w_prime / (t + (w_prime / (p_max - cp))) + cp


def extended_5_3_predict(
    t,
    power_anaerobic_alactic,
    power_anaerobic_decay,
    cp,
    tau_delay,
    cp_delay,
    cp_decay,
    cp_decay_delay,
    tau,
):
    """
    Credits to Damien Grauser. Source:
    https://github.com/GoldenCheetah/GoldenCheetah/blob/master/src/Metrics/ExtendedCriticalPower.cpp
    """
    model = (
        (power_anaerobic_alactic)
        * (1.20 - 0.20 * np.exp(-1 * t))
        * (np.exp(power_anaerobic_decay * t))
    ) + (
        (cp)
        * (1 - np.exp(cp_delay * t))
        * (1 + cp_decay * np.exp(cp_decay_delay / t))
        * (1 - np.exp(tau_delay * t))
        * (1 + tau / t)
    )

    model = np.nan_to_num(model)
    model[model > 2000] = 0
    model[model < 1] = 0

    return model


def extended_7_3_predict(
    t,
    power_anaerobic_alactic,
    power_anaerobic_decay,
    cp,
    tau_delay,
    cp_delay,
    cp_decay,
    cp_decay_delay,
    tau,
):
    """
    Credits to Damien Grauser. Source:
    https://github.com/GoldenCheetah/GoldenCheetah/blob/master/src/Metrics/ExtendedCriticalPower.cpp
    """
    model = (
        (power_anaerobic_alactic)
        * ((np.exp(power_anaerobic_decay)) * (np.power(t, power_anaerobic_alactic)))
    ) + (
        (cp * (1 - np.exp(tau_delay * t)))
        * (1 - np.exp(cp_delay * t))
        * (1 + cp_decay * np.exp(cp_decay_delay / t))
        * (1 + tau / t)
    )

    model = np.nan_to_num(model)
    model[model > 2000] = 0
    model[model < 1] = 0

    return model


def model_fit(x, y, model="extended_5_3"):
    if model == "2_parameter_non_linear":
        predict_func = two_parameter_non_linear_predict
        initial_model_params = OrderedDict(cp=300, w_prime=20000)
    if model == "3_parameter_non_linear":
        predict_func = three_parameter_non_linear_predict
        initial_model_params = OrderedDict(cp=300, w_prime=20000, p_max=1000)
    elif model == "extended_5_3":
        predict_func = extended_5_3_predict
        initial_model_params = OrderedDict(
            power_anaerobic_alactic=811,
            power_anaerobic_decay=-2,
            cp=280,
            cp_delay=-0.9,
            cp_decay=-0.583,
            cp_decay_delay=-180,
            tau=1.208,
            tau_delay=-4.8,
        )
    elif model == "extended_7_3":
        predict_func = extended_7_3_predict
        initial_model_params = OrderedDict(
            power_anaerobic_alactic=811,
            power_anaerobic_decay=-2,
            cp=280,
            cp_delay=-0.9,
            cp_decay=-0.583,
            cp_decay_delay=-180,
            tau=1.208,
            tau_delay=-4.8,
        )

    initial_param_array = np.array(list(initial_model_params.values()))

    model_params, _ = curve_fit(
        f=predict_func, xdata=x, ydata=y, p0=initial_param_array,
    )

    fitted_model_params = dict(zip(initial_model_params.keys(), model_params))

    return fitted_model_params
