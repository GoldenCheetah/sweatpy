import math
from collections import namedtuple

from lmfit import minimize, Parameters
import numpy as np
import pandas as pd

from .extended_critical_power import *
from .heartrate_models import *
from .w_prime_balance import *


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
