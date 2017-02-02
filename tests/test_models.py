import unittest

from pandas import DataFrame

from athletic_pandas import models


class TestWorkoutDataFrame(unittest.TestCase):
    def setUp(self):
        self.wdf = models.WorkoutDataFrame()

    def test_init(self):
        self.assertIsInstance(self.wdf, DataFrame)
        self.assertIsInstance(self.wdf, models.WorkoutDataFrame)

    def test_mean_max_power(self):
        self.assertIsNone(self.wdf.mean_max_power())
