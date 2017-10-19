import math

import numpy as np
import pandas as pd

from .base import BaseWorkoutDataFrame
from .helpers import requires

MEAN_MAX_POWER_INTERVALS = [
    1, 2, 3, 5, 10, 15, 20, 30, 45, 60, 90,\
    120, 180, 300, 600, 1200, 3600, 7200]


class WorkoutDataFrame(BaseWorkoutDataFrame):
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
        wap = self.power.rolling(30).mean().pow(4).mean()**(1/4)
        return wap

    @requires(columns=['power'], athlete=['weight'])
    def power_per_kg(self):
        ppkg = self.power / self.athlete.weight
        return ppkg

    def _tau_w_prime_balance(self):
        avg_power_below_cp = self.power[self.power < self.athlete.cp].mean()
        return 546*math.e**(-0.01*avg_power_below_cp) + 316

    @requires(columns=['power'], athlete=['cp', 'w_prime'])
    def w_prime_balance(self):
        '''
        Source:
        Skiba, Philip Friere, et al. "Modeling the expenditure and reconstitution of work capacity above critical power." Medicine and science in sports and exercise 44.8 (2012): 1526-1532.
        '''
        sampling_rate = 1
        running_sum = 0
        w_balance = []
        tau = self._tau_w_prime_balance()
        
        for i, power in enumerate(self.power):
            power_above_cp = power - self.athlete.cp
            w_prime_expenditure = max(0, power_above_cp)*sampling_rate
            running_sum = running_sum + \
                w_prime_expenditure*(math.e**(i*sampling_rate/tau))

            w_balance.append(
                self.athlete.w_prime - running_sum*math.e**(-i*sampling_rate/tau)
            )

        return pd.Series(w_balance)


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
