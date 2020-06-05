import math

import numpy as np
import pandas as pd


def tau_w_prime_balance(power, cp, untill=None):
    if untill is None:
        untill = len(power)

    avg_power_below_cp = power[:untill][power[:untill] < cp].mean()
    if math.isnan(avg_power_below_cp):
        avg_power_below_cp = 0
    delta_cp = cp - avg_power_below_cp

    return 546 * math.e ** (-0.01 * delta_cp) + 316


def get_tau_method(power, cp, tau_dynamic, tau_value):
    if tau_dynamic:
        tau_dynamic = [tau_w_prime_balance(power, cp, i) for i in range(len(power))]
        tau = lambda t: tau_dynamic[t]

    elif tau_value is None:
        static_tau = tau_w_prime_balance(power, cp)
        tau = lambda t: static_tau

    else:
        tau = lambda t: tau_value

    return tau


def w_prime_balance_waterworth(
    power, cp, w_prime, tau_dynamic=False, tau_value=None, *args, **kwargs
):
    """
    Optimisation of Skiba's algorithm by Dave Waterworth.
    Source:
    http://markliversedge.blogspot.nl/2014/10/wbal-optimisation-by-mathematician.html
    Source:
    Skiba, Philip Friere, et al. "Modeling the expenditure and reconstitution of work capacity above critical power." Medicine and science in sports and exercise 44.8 (2012): 1526-1532.
    """
    sampling_rate = 1
    running_sum = 0
    w_prime_balance = []
    tau = get_tau_method(power, cp, tau_dynamic, tau_value)

    for t, p in enumerate(power):
        power_above_cp = p - cp
        w_prime_expended = max(0, power_above_cp) * sampling_rate
        running_sum = running_sum + w_prime_expended * (
            math.e ** (t * sampling_rate / tau(t))
        )

        w_prime_balance.append(
            w_prime - running_sum * math.e ** (-t * sampling_rate / tau(t))
        )

    return pd.Series(w_prime_balance)


def w_prime_balance_skiba(
    power, cp, w_prime, tau_dynamic=False, tau_value=None, *args, **kwargs
):
    """
    Source:
    Skiba, Philip Friere, et al. "Modeling the expenditure and reconstitution of work capacity above critical power." Medicine and science in sports and exercise 44.8 (2012): 1526-1532.
    """
    w_prime_balance = []
    tau = get_tau_method(power, cp, tau_dynamic, tau_value)

    for t in range(len(power)):
        w_prime_exp_sum = 0

        for u, p in enumerate(power[: t + 1]):
            w_prime_exp = max(0, p - cp)
            w_prime_exp_sum += w_prime_exp * np.power(np.e, (u - t) / tau(t))

        w_prime_balance.append(w_prime - w_prime_exp_sum)

    return pd.Series(w_prime_balance)


def w_prime_balance_froncioni_skiba_clarke(power, cp, w_prime):
    """
    Source:
    Skiba, P. F., Fulford, J., Clarke, D. C., Vanhatalo, A., & Jones, A. M. (2015). Intramuscular determinants of the ability to recover work capacity above critical power. European journal of applied physiology, 115(4), 703-713.
    """
    last = w_prime
    w_prime_balance = []

    for p in power:
        if p < cp:
            new = last + (cp - p) * (w_prime - last) / w_prime
        else:
            new = last + (cp - p)

        w_prime_balance.append(new)
        last = new

    return pd.Series(w_prime_balance)


def w_prime_balance(power, cp, w_prime, algorithm="waterworth", *args, **kwargs):
    if algorithm == "waterworth":
        method = w_prime_balance_waterworth
    elif algorithm == "skiba":
        method = w_prime_balance_skiba
    elif algorithm == "froncioni-skiba-clarke":
        method = w_prime_balance_froncioni_skiba_clarke

    return method(power, cp, w_prime, *args, **kwargs)
