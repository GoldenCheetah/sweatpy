from sweat.algorithms.hrm import heartrate_models
from sweat.algorithms.pdm import w_prime_balance
from sweat.algorithms.metrics import core, power
from .base import BaseWorkoutDataFrame
from sweat.models.helpers import requires


class WorkoutDataFrame(BaseWorkoutDataFrame):
    """Pandas DataFrame for Workouts

    Columns
    -------
    power : array-like
    heartrate : array-like
    time : array-like
    cadence : array-like
    speed : array-like

    Metadata
    --------
    athlete : Athlete
    """
    _metadata = ['athlete']

    @requires(columns=['power'])
    def compute_mean_max_power(self):
        return core.mean_max(self.power)

    @requires(columns=['power'])
    def compute_weighted_average_power(self):
        return core.weighted_average_power(self.power, type='WAP')

    @requires(columns=['power'], athlete=['weight'])
    def compute_power_per_kg(self):
        return power.wpk(self.power, self.athlete.weight)

    @requires(columns=['power'], athlete=['cp', 'w_prime'])
    def compute_w_prime_balance(self, algorithm=None, *args, **kwargs):
        return w_prime_balance.w_prime_balance(self.power, self.athlete.cp,
                                               self.athlete.w_prime, algorithm, *args, **kwargs)

    @requires(columns=['power'])
    def compute_mean_max_bests(self, duration, number):
        return core.multiple_best_intervals(self.power, duration, number)

    @requires(columns=['power', 'heartrate'])
    def compute_heartrate_model(self):
        return heartrate_models.heartrate_model(self.heartrate, self.power)


class Athlete:
    """Athlete object for WorkoutDataFrame"""

    def __init__(self, name=None, sex=None, weight=None, dob=None, ftp=None,
            cp=None, w_prime=None):
        """

        Parameters
        ----------
        name : str, optional
        sex : srt, optional
        weight : number, optional
        dob : str, "YYYY-MM-DD", optional
        ftp : number, optional
        cp : number, optional
        w_prime : number, optional
        """
        self.name = name
        self.sex = sex
        self.weight = weight
        self.dob = dob
        self.ftp = ftp
        self.cp = cp
        self.w_prime = w_prime
