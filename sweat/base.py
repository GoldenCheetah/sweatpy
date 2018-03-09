import pandas as pd

from .mixins import ValidationMixin


class BaseWorkoutDataFrame(pd.DataFrame, ValidationMixin):
    _metadata = ['athlete']

    @property
    def _constructor(self):
        return self.__class__ # A less hacky way would be appreciated...
