from pandas import DataFrame

from .helpers import field_validations


class WorkoutDataFrame(DataFrame):
    def __init__(self, *args, **kwargs):
        super(WorkoutDataFrame, self).__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return WorkoutDataFrame

    @field_validations(["power"])
    def mean_max_power(self):
        pass

    def normalized_power(self):
        pass
