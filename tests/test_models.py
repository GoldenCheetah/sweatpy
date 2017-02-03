import unittest

import numpy as np
import pandas as pd

from athletic_pandas import exceptions
from athletic_pandas import models


class TestAthlete(unittest.TestCase):
    def setUp(self):
        self.athlete = models.Athlete(name='Chris', ftp=300)

    def test_empty_init(self):
        athlete = models.Athlete()
        self.assertTrue(hasattr(athlete, 'name'))
        self.assertTrue(hasattr(athlete, 'sex'))
        self.assertTrue(hasattr(athlete, 'weight'))
        self.assertTrue(hasattr(athlete, 'dob'))
        self.assertTrue(hasattr(athlete, 'ftp'))

    def test_init(self):
        self.assertEqual(self.athlete.name, 'Chris')
        self.assertEqual(self.athlete.ftp, 300)


class TestWorkoutDataFrame(unittest.TestCase):
    def setUp(self):
        data = {
            'time': range(10),
            'heartrate': range(10),
            'power': range(10)}
        athlete = models.Athlete(name='Chris', ftp=300)
        self.wdf = models.WorkoutDataFrame(data)
        self.wdf = self.wdf.set_index('time')
        self.wdf.athlete = athlete

    def test_empty_init(self):
        wdf = models.WorkoutDataFrame()
        self.assertIsInstance(wdf, pd.DataFrame)
        self.assertIsInstance(wdf, models.WorkoutDataFrame)

    def test_init(self):
        self.assertTrue('power' in list(self.wdf))
        self.assertTrue('heartrate' in list(self.wdf))
        self.assertEqual(len(self.wdf), 10)
        self.assertTrue(hasattr(self.wdf, 'athlete'))
    
    def test_slicing(self):
        new_wdf = self.wdf[1:5]
        self.assertTrue(isinstance(new_wdf, models.WorkoutDataFrame))
    
    def test_metadata_propagation(self):
        self.assertEqual(self.wdf[1:5].athlete.name, 'Chris')
        self.assertEqual(self.wdf.iloc[[0, 1], :].athlete.name, 'Chris')
        self.assertEqual(self.wdf[['power']].athlete.name, 'Chris')

    def test_is_valid(self):
        self.assertTrue(self.wdf.is_valid())

    def test_is_valid_missing_time_index(self):
        self.wdf.index.name = 'not_time'
        with self.assertRaises(exceptions.WorkoutDataFrameValidationException):
            self.wdf.is_valid()

    def test_is_valid_invalid_sample_rate(self):
        data = {
            'time': range(0, 20, 2),
            'heartrate': range(10),
            'power': range(10)}
        wdf = models.WorkoutDataFrame(data)
        wdf = wdf.set_index('time')
        with self.assertRaisesRegex(
            expected_exception=exceptions.WorkoutDataFrameValidationException,
            expected_regex='[.\n]*Sample rate is not \(consistent\) 1Hz[.\n]*'):
            wdf.is_valid()

    def test_is_valid_invalid_dtype(self):
        data = {
            'time': range(10),
            'heartrate': np.arange(0, 15, 1.5),
            'power': range(10)}
        wdf = models.WorkoutDataFrame(data)
        wdf = wdf.set_index('time')
        with self.assertRaisesRegex(
            expected_exception=exceptions.WorkoutDataFrameValidationException,
            expected_regex='[.\n]*Column \'heartrate\' is not of dtype[.\n]*'):
            wdf.is_valid()

    def test_is_valid_invalid_min_value(self):
        data = {
            'time': range(10),
            'heartrate': range(-10, 0),
            'power': range(10)}
        wdf = models.WorkoutDataFrame(data)
        wdf = wdf.set_index('time')
        with self.assertRaisesRegex(
            expected_exception=exceptions.WorkoutDataFrameValidationException,
            expected_regex='[.\n]*Column \'heartrate\' has values < 0[.\n]*'):
            wdf.is_valid()

    def test_is_valid_invalid_max_value(self):
        data = {
            'time': range(10),
            'heartrate': range(10),
            'power': range(10000, 10010)}
        wdf = models.WorkoutDataFrame(data)
        wdf = wdf.set_index('time')
        with self.assertRaisesRegex(
            expected_exception=exceptions.WorkoutDataFrameValidationException,
            expected_regex='[.\n]*Column \'power\' has values > 3000[.\n]*'):
            wdf.is_valid()

    def test_mean_max_power(self):
        self.wdf['power'] = np.nan
        self.assertIsNone(self.wdf.mean_max_power())

    def test_mean_max_power_missing_power(self):
        del self.wdf['power']
        with self.assertRaises(exceptions.MissingDataException):
            self.assertIsNone(self.wdf.mean_max_power())

    def test_normalized_power(self):
        self.assertIsNone(self.wdf.normalized_power())

    def test_power_per_kg(self):
        self.wdf.athlete.ftp = 300
        self.assertIsNone(self.wdf.power_per_kg())

    def test_power_per_kg_missing_ftp(self):
        self.wdf.athlete.ftp = None
        with self.assertRaises(exceptions.MissingDataException):
            self.wdf.power_per_kg()
