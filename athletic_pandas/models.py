import math
from collections import namedtuple

import numpy as np
import pandas as pd

from .base import BaseWorkoutDataFrame
from .helpers import requires

MEAN_MAX_POWER_INTERVALS = [
    1, 2, 3, 5, 10, 15, 20, 30, 45, 60, 90,\
    120, 180, 300, 600, 1200, 3600, 7200]


DataPoint = namedtuple('DataPoint', ['index', 'value'])


class WorkoutDataFrame(BaseWorkoutDataFrame):
    _metadata = ['athlete']

    @requires(columns=['power'])
    def mean_max_power(self):
        mmp = pd.Series()
        length = len(self)

        for i in MEAN_MAX_POWER_INTERVALS:
            if i > length:
                break

            mmp = mmp.append(
                pd.Series(
                    [self.power.rolling(i).mean().max()],
                    [i]
                )
            )

        return mmp

    @requires(columns=['power'])
    def weighted_average_power(self):
        wap = self.power.rolling(30).mean().pow(4).mean().__pow__(1/4)
        return wap

    @requires(columns=['power'], athlete=['weight'])
    def power_per_kg(self):
        ppkg = self.power / self.athlete.weight
        return ppkg

    def _tau_w_prime_balance(self, untill=None):
        if untill is None:
            untill = len(self.power)

        avg_power_below_cp = self.power[:untill][self.power[:untill] < self.athlete.cp].mean()
        if math.isnan(avg_power_below_cp):
            avg_power_below_cp = 0

        return 546*math.e**(-0.01*avg_power_below_cp) + 316

    def _get_tau_method(self, tau_dynamic, tau_value):
        if tau_dynamic:
            tau_dynamic = [self._tau_w_prime_balance(i) for i in range(len(self.power))]
            tau = lambda t: tau_dynamic[t]

        elif tau_value is None:
            static_tau = self._tau_w_prime_balance()
            tau = lambda t: static_tau

        else:
            tau = lambda t: tau_value
        
        return tau

    @requires(columns=['power'], athlete=['cp', 'w_prime'])
    def _w_prime_balance_waterworth(self, tau_dynamic=False, tau_value=None, *args, **kwargs):
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
        tau = self._get_tau_method(tau_dynamic, tau_value)
        
        for t, power in enumerate(self.power):
            power_above_cp = power - self.athlete.cp
            w_prime_expended = max(0, power_above_cp)*sampling_rate
            running_sum = running_sum + \
                w_prime_expended*(math.e**(t*sampling_rate/tau(t)))

            w_prime_balance.append(
                self.athlete.w_prime - running_sum*math.e**(-t*sampling_rate/tau(t))
            )

        return pd.Series(w_prime_balance)

    @requires(columns=['power'], athlete=['cp', 'w_prime'])
    def _w_prime_balance_skiba(self, tau_dynamic=False, tau_value=None, *args, **kwargs):
        '''
        Source:
        Skiba, Philip Friere, et al. "Modeling the expenditure and reconstitution of work capacity above critical power." Medicine and science in sports and exercise 44.8 (2012): 1526-1532.
        '''
        w_prime_balance = []
        tau = self._get_tau_method(tau_dynamic, tau_value)

        for t in range(len(self.power)):
            w_prime_exp_sum = 0

            for u, power in enumerate(self.power[:t]):
                w_prime_exp = max(0, power - self.athlete.cp)
                w_prime_exp_sum += w_prime_exp * np.power(np.e, (u - t)/tau(t))

            w_prime_balance.append(self.athlete.w_prime - w_prime_exp_sum)

        return pd.Series(w_prime_balance)

    @requires(columns=['power'], athlete=['cp', 'w_prime'])
    def _w_prime_balance_froncioni(self):
        """
        Source:
        https://github.com/GoldenCheetah/GoldenCheetah/blob/160eb74cab712bfaa9eab64dd19310e5d42ed193/src/Metrics/WPrime.cpp#L257
        """
        cp = self.athlete.cp
        w_prime = self.athlete.w_prime
        last = self.athlete.w_prime
        w_prime_balance = []

        for power in self.power:
            if power < cp:
                new = last + (cp - power) * (w_prime - last)/last
            else:
                new = last + (cp - power)

            w_prime_balance.append(new)
            last = new

        return pd.Series(w_prime_balance)

    def w_prime_balance(self, algorithm=None, *args, **kwargs):
        if algorithm is None:
            algorithm = 'waterworth'
        method = getattr(self, '_w_prime_balance_' + algorithm)

        return method(*args, **kwargs)

    def compute_mean_max_bests(self, duration, amount):
        moving_average = self.power.rolling(duration).mean()
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

        return mean_max_bests


class Athlete:
    def __init__(self, name=None, sex=None, weight=None, dob=None, ftp=None,
            cp=None, w_prime=None):
        self.name = name
        self.sex = sex
        self.weight = weight
        self.dob = dob
        self.ftp = ftp
        self.cp = cp
        self.w_prime = w_prime
