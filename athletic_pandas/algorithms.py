import math
from collections import namedtuple

import numpy as np
import pandas as pd


def mean_max_power(power):
    mmp = []

    for i in range(len(power)):
        mmp.append(power.rolling(i+1).mean().max())

    return pd.Series(mmp)


DataPoint = namedtuple('DataPoint', ['index', 'value'])


def mean_max_bests(power, duration, amount):
    moving_average = power.rolling(duration).mean()
    length = len(moving_average)
    mean_max_bests = []

    for i in range(amount):
        if moving_average.isnull().all():
            mean_max_bests.append(DataPoint(np.nan, np.nan))
            continue

        max_value = moving_average.max()
        max_index = moving_average.idxmax()
        mean_max_bests.append(DataPoint(max_index, max_value))

        # Set moving averages that overlap with last found max to np.nan
        overlap_min_index = max(0, max_index-duration)
        overlap_max_index = min(length, max_index+duration)
        moving_average.loc[overlap_min_index:overlap_max_index] = np.nan

    return pd.Series(mean_max_bests)

def weighted_average_power(power):
    wap = power.rolling(30).mean().pow(4).mean().__pow__(1/4)
    return wap

def power_per_kg(power, weight):
    ppkg = power / weight
    return ppkg

def _tau_w_prime_balance(power, cp, untill=None):
    if untill is None:
        untill = len(power)

    avg_power_below_cp = power[:untill][power[:untill] < cp].mean()
    if math.isnan(avg_power_below_cp):
        avg_power_below_cp = 0

    return 546*math.e**(-0.01*avg_power_below_cp) + 316

def _get_tau_method(power, cp, tau_dynamic, tau_value):
    if tau_dynamic:
        tau_dynamic = [_tau_w_prime_balance(power, cp, i) for i in range(len(power))]
        tau = lambda t: tau_dynamic[t]

    elif tau_value is None:
        static_tau = _tau_w_prime_balance(power, cp)
        tau = lambda t: static_tau

    else:
        tau = lambda t: tau_value

    return tau

def w_prime_balance_waterworth(power, cp, w_prime, tau_dynamic=False,
        tau_value=None, *args, **kwargs):
    '''
    Optimisation of Skiba's algorithm by Dave Waterworth.
    Source:
    http://markliversedge.blogspot.nl/2014/10/wbal-optimisation-by-mathematician.html
    Source:
    Skiba, Philip Friere, et al. "Modeling the expenditure and reconstitution of work capacity above critical power." Medicine and science in sports and exercise 44.8 (2012): 1526-1532.
    '''
    sampling_rate = 1
    running_sum = 0
    w_prime_balance = []
    tau = _get_tau_method(power, cp, tau_dynamic, tau_value)

    for t, p in enumerate(power):
        power_above_cp = p - cp
        w_prime_expended = max(0, power_above_cp)*sampling_rate
        running_sum = running_sum + \
            w_prime_expended*(math.e**(t*sampling_rate/tau(t)))

        w_prime_balance.append(
            w_prime - running_sum*math.e**(-t*sampling_rate/tau(t))
        )

    return pd.Series(w_prime_balance)

def w_prime_balance_skiba(power, cp, w_prime, tau_dynamic=False,
        tau_value=None, *args, **kwargs):
    '''
    Source:
    Skiba, Philip Friere, et al. "Modeling the expenditure and reconstitution of work capacity above critical power." Medicine and science in sports and exercise 44.8 (2012): 1526-1532.
    '''
    w_prime_balance = []
    tau = _get_tau_method(power, cp, tau_dynamic, tau_value)

    for t in range(len(power)):
        w_prime_exp_sum = 0

        for u, p in enumerate(power[:t]):
            w_prime_exp = max(0, p - cp)
            w_prime_exp_sum += w_prime_exp * np.power(np.e, (u - t)/tau(t))

        w_prime_balance.append(w_prime - w_prime_exp_sum)

    return pd.Series(w_prime_balance)

def w_prime_balance_froncioni(power, cp, w_prime):
    """
    Source:
    https://github.com/GoldenCheetah/GoldenCheetah/blob/160eb74cab712bfaa9eab64dd19310e5d42ed193/src/Metrics/WPrime.cpp#L257
    """
    last = w_prime
    w_prime_balance = []

    for p in power:
        if p < cp:
            new = last + (cp - p) * (w_prime - last)/last
        else:
            new = last + (cp - p)

        w_prime_balance.append(new)
        last = new

    return pd.Series(w_prime_balance)

def w_prime_balance(power, cp, w_prime, algorithm=None, *args, **kwargs):
    if algorithm is None:
        algorithm = 'waterworth'
    method = eval('w_prime_balance_' + algorithm)

    return method(power, cp, w_prime, *args, **kwargs)
