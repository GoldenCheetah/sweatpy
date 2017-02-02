from pandas import DataFrame


class WorkoutDataFrame(DataFrame):
    def __init__(self, *args, **kwargs):
        super(WorkoutDataFrame, self).__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return WorkoutDataFrame

    def mean_max_power(self):
        pass
