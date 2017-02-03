import unittest

from pandas import DataFrame

from athletic_pandas.models import WorkoutDataFrame
from athletic_pandas.exceptions import MissingDataException


class TestWorkoutDataFrame(unittest.TestCase):
    def setUp(self):
        self.wdf = WorkoutDataFrame()

    def test_init(self):
        self.assertIsInstance(self.wdf, DataFrame)
        self.assertIsInstance(self.wdf, WorkoutDataFrame)

    def test_mean_max_power(self):
        with self.assertRaises(MissingDataException):
            self.assertIsNone(self.wdf.mean_max_power())

    def test_normalized_power(self):
        self.assertIsNone(self.wdf.normalized_power())

