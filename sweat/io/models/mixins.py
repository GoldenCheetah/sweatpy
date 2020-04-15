import numpy as np

from sweat.io.models.exceptions import WorkoutDataFrameValidationException

VALIDATION_COLUMNS = ["time", "power", "heartrate", "cadence", "speed"]

COLUMN_DTYPES = {
    "time": np.int,
    "power": np.int,
    "heartrate": np.int,
    "cadence": np.int,
    "speed": np.int,
}

COLUMN_MIN_VALUE = {"time": 0, "power": 0, "heartrate": 0, "cadence": 0, "speed": 0}

COLUMN_MAX_VALUE = {
    "time": np.inf,
    "power": 3000,
    "heartrate": 300,
    "cadence": 300,
    "speed": 0,
}


class ValidationMixin(object):
    def is_valid(self):
        errors = list()

        errors += self._validate_index()
        errors += self._validate_columns()

        if errors:
            raise WorkoutDataFrameValidationException(errors)
        return True

    def _validate_columns(self):
        errors = list()
        columns = set(VALIDATION_COLUMNS) & set(list(self))

        for c in columns:
            errors += self._validate_series(
                series=self[c],
                dtype=COLUMN_DTYPES[c],
                min_value=COLUMN_MIN_VALUE[c],
                max_value=COLUMN_MAX_VALUE[c],
            )

        return errors

    @classmethod
    def _validate_series(cls, series, dtype, min_value, max_value):
        errors = list()
        if series.dtype != dtype:
            errors.append("Column '{}' is not of dtype '{}'".format(series.name, dtype))
        if series.min() < min_value:
            errors.append("Column '{}' has values < {}".format(series.name, min_value))
        if series.max() > max_value:
            errors.append("Column '{}' has values > {}".format(series.name, max_value))
        return errors

    def _validate_index(self):
        errors = list()

        if not self.index.name == "time":
            errors.append(
                "Index should be set to 'time'. See 'pandas.DataFrame.set_index'"
            )
            return errors

        # @TODO change diff to calculation that's meaningful for time object
        # @TODO also change time dtype and min max
        index_diff = self.index.to_series().diff(1)
        if index_diff.where(index_diff != 1).where(index_diff != np.nan).count():
            errors.append("Sample rate is not (consistent) 1Hz")

        return errors
