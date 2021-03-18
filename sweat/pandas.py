from functools import wraps
from typing import List, Union

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

from .constants import DataTypeEnum
from .metrics import core


def validate_sample_rate(sample_rate):
    def wrapper(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            if not all(self._obj.index.to_series().diff()[1:] == sample_rate):
                raise AttributeError(
                    f"Data is not sampled at a regular interval of {sample_rate.tostring()}. Consider resampling first."
                )
            return func(self, *args, **kwargs)

        return wrapped

    return wrapper


@pd.api.extensions.register_dataframe_accessor("sweat")
class SweatAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        if not isinstance(obj.index, (pd.DatetimeIndex, pd.TimedeltaIndex)):
            raise AttributeError("DataFrame Index should be a DateTimeIndex.")

        if not all(obj.index.to_series().diff()[1:] == np.timedelta64(1, "s")):
            raise AttributeError(
                "Data is not sampled at a regular 1s interval. Consider resampling first."
            )

        for data_type in DataTypeEnum:
            # @TODO figure out which columns need to be numeric continue
            continue
            try:
                if not is_numeric_dtype(obj[data_type.value]):
                    raise AttributeError(f"Column {data_type.value} is not numeric")
            except KeyError:
                continue

    @validate_sample_rate(sample_rate=np.timedelta64(1, "s"))
    def mean_max(
        self, columns: Union[List, str], monotonic: bool = False
    ) -> pd.DataFrame:
        if isinstance(columns, str):
            columns = [columns]

        data = None
        for column in columns:
            result = core.mean_max(self._obj[column], monotonic=monotonic)

            if data is None:
                index = pd.to_timedelta(range(1, len(result) + 1), unit="s")
                data = pd.DataFrame(index=index)

            data["mean_max_" + column] = result

        return data

    def to_timedelta_index(self):
        """This method converts the index to a relative TimedeltaIndex, returning a copy of the data frame with the new index.

        Returns:
            A pandas data frame with a TimedeltaIndex.
        """
        return self._obj.set_index(self._obj.index - self._obj.index[0])


@pd.api.extensions.register_series_accessor("sweat")
class SweatSeriesAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        if not isinstance(obj.index, pd.DatetimeIndex):
            raise AttributeError("DataFrame Index should be a DateTimeIndex.")

        if not all(obj.index.to_series().diff()[1:] == np.timedelta64(1, "s")):
            raise AttributeError(
                "Data is not sampled at a regular 1s interval. Consider resampling first."
            )

        if not is_numeric_dtype(obj):
            raise AttributeError(f"Series dtype should be numeric")

    @validate_sample_rate(sample_rate=np.timedelta64(1, "s"))
    def mean_max(self, monotonic: bool = False) -> pd.Series:
        """This method calculates the mean max values of the series.

        Returns:
            A pandas series with a TimedeltaIndex.
        """
        result = core.mean_max(self._obj, monotonic=monotonic)
        index = pd.to_timedelta(range(1, len(result) + 1), unit="s")
        return pd.Series(result, index=index, name="mean_max_" + self._obj.name)

    def to_timedelta_index(self):
        """This method converts the index to a relative TimedeltaIndex, returning a copy of the series with the new index.

        Returns:
            A pandas series with a TimedeltaIndex.
        """
        index = self._obj.index - self._obj.index[0]
        return pd.Series(self._obj, index=index)

    def calculate_zones(
        self, bins: List[int], labels: List[Union[int, str]]
    ) -> pd.Series:
        """Returns a pandas.Series with the zone label for each value.
        This method uses the pandas.cut() method under the hood.
        Nan will be returned for values that are not in any of the bins.

        Args:
            bins: Left and right bounds for each zone.
            labels: Specifies the labels for the zones. Must be the same length as the resulting zones.

        Returns:
            A pandas series with the zone label for each value.
        """
        return pd.cut(self._obj, bins=bins, labels=labels)

    def time_in_zone(self, bins: List[int], labels: List[Union[int, str]]) -> pd.Series:
        """Returns a pandas.Series with the value counts for each zone.
        This method uses the pandas.Series.value_counts() method under the hood.

        Args:
            bins: Left and right bounds for each zone.
            labels: Specifies the labels for the zones. Must be the same length as the resulting zones.

        Returns:
            A pandas series with the value counts for each zones.
        """
        zones = self.calculate_zones(bins, labels)
        zones_value_counts = zones.value_counts()
        return pd.to_timedelta(zones_value_counts, unit="s")
