import unittest

import numpy as np
from pandas import DataFrame

from athletic_pandas.exceptions import MissingDataException
from athletic_pandas.models import Athlete, Workout


class TestWorkout(unittest.TestCase):
    def setUp(self):
        self.wdf = Workout()

    def test_init(self):
        self.assertIsInstance(self.wdf, DataFrame)
        self.assertIsInstance(self.wdf, Workout)

    def test_constructor(self):
        self.wdf['power'] = np.nan
        new_wdf = self.wdf.ix[:,['power']]
        self.assertIsInstance(new_wdf, DataFrame)
        self.assertIsInstance(new_wdf, Workout)

    def test_mean_max_power(self):
        self.wdf['power'] = np.nan
        self.assertIsNone(self.wdf.mean_max_power())

    def test_mean_max_power_missing_power(self):
        with self.assertRaises(MissingDataException):
            self.assertIsNone(self.wdf.mean_max_power())

    def test_normalized_power(self):
        self.assertIsNone(self.wdf.normalized_power())

    def test_power_per_kg(self):
        self.wdf['power'] = np.nan
        self.wdf._metadata['athlete'].ftp = 300
        self.assertIsNone(self.wdf.power_per_kg())

    def test_power_per_kg_missing_ftp(self):
        self.wdf['power'] = np.nan
        with self.assertRaises(MissingDataException):
            self.wdf.power_per_kg()
