import numpy as np
import pandas as pd

from .helpers import requires
from .validators import WorkoutDataFrameValidator

MEAN_MAX_POWER_INTERVALS = [
    1, 2, 3, 5, 10, 15, 20, 30, 45, 60, 90,\
    120, 180, 300, 600, 1200, 3600, 7200]


class WorkoutDataFrame(pd.DataFrame):
    _metadata = ['athlete']

    @property
    def _constructor(self):
        return WorkoutDataFrame

    def is_valid(self):
        return WorkoutDataFrameValidator.is_valid(self)

    @requires(columns=['power'])
    def mean_max_power(self):
        mmp = pd.Series()
        length = len(self)

        for i in MEAN_MAX_POWER_INTERVALS:
            if i > length:
                break

            mmp = mmp.append(
                pd.Series([int(round(self.power.rolling(i).mean().max(), 0))], [i]))

        return mmp

    def weighted_average_power(self):
        wap = self.power.rolling(30).mean().pow(4).mean()**(1/4)
        return int(round(wap, 0))

    @requires(columns=['power'], athlete=['weight'])
    def power_per_kg(self):
        ppkg = self.power / self.athlete.weight
        return ppkg.round(2)


class Athlete:
    def __init__(self, name=None, sex=None, weight=None, dob=None, ftp=None):
        self.name = name
        self.sex = sex
        self.weight = weight
        self.dob = dob
        self.ftp = ftp
