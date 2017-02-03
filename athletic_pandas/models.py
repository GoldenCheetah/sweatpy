from pandas import DataFrame

from .helpers import requirements


class Athlete:
    def __init__(self, name=None, sex=None, weight=None, dob=None, ftp=None):
        self.name = name
        self.sex = sex
        self.weight = weight
        self.dob = dob
        self.ftp = ftp


class WorkoutDataFrame(DataFrame):
    _metadata = ['athlete']

    @property
    def _constructor(self):
        return WorkoutDataFrame

    @requirements(columns=["power"])
    def mean_max_power(self):
        pass

    def normalized_power(self):
        pass

    @requirements(columns=["power"], athlete=['ftp'])
    def power_per_kg(self):
        pass
