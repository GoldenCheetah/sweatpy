import pandas as pd

from sweat.io.models.mixins import ValidationMixin


class BaseWorkoutDataFrame(pd.DataFrame, ValidationMixin):
    _metadata = ["athlete"]

    @property
    def _constructor(self):
        return self.__class__  # A less hacky way would be appreciated...
