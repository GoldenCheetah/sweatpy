from pandas import DataFrame

from .helpers import requirements


class Athlete:
    def __init__(self, name=None, weight=None, dob=None, ftp=None):
        self.name = name
        self.weight = weight
        self.dob = dob
        self.ftp = ftp


class Workout(DataFrame):
    def __init__(self, *args, **kwargs):
        super(Workout, self).__init__(*args, **kwargs)
        self._metadata = {'athlete': kwargs.pop('athlete', Athlete())}

    @property
    def _constructor(self):
        return Workout

    def __finalize__(self, other, method=None, **kwargs):
        # Borrowed from GeoPandas.GeoDataFrame.__finalize__
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self

    @requirements(columns=["power"])
    def mean_max_power(self):
        pass

    def normalized_power(self):
        pass

    @requirements(columns=["power"], athlete=['ftp'])
    def power_per_kg(self):
        pass
