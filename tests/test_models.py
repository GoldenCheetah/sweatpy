import unittest

import numpy as np
from pandas import DataFrame

from athletic_pandas.exceptions import MissingDataException
from athletic_pandas.models import Athlete, WorkoutDataFrame


class TestAthlete(unittest.TestCase):
    def setUp(self):
        self.athlete = Athlete(name='Chris', ftp=300)

    def test_empty_init(self):
        athlete = Athlete()
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
            'heartrate': range(10),
            'power': range(10)}
        athlete = Athlete(name='Chris', ftp=300)
        self.wdf = WorkoutDataFrame(data)
        self.wdf.athlete = athlete

    def test_empty_init(self):
        wdf = WorkoutDataFrame()
        self.assertIsInstance(wdf, DataFrame)
        self.assertIsInstance(wdf, WorkoutDataFrame)

    def test_init(self):
        self.assertTrue('power' in list(self.wdf))
        self.assertTrue('heartrate' in list(self.wdf))
        self.assertEqual(len(self.wdf), 10)
        self.assertTrue(hasattr(self.wdf, 'athlete'))
    
    def test_slicing(self):
        new_wdf = self.wdf[1:5]
        self.assertTrue(isinstance(new_wdf, WorkoutDataFrame))
    
    def test_metadata_propagation(self):
        self.assertEqual(self.wdf[1:5].athlete.name, 'Chris')
        self.assertEqual(self.wdf.iloc[[0, 1], :].athlete.name, 'Chris')
        self.assertEqual(self.wdf[['power']].athlete.name, 'Chris')

    def test_mean_max_power(self):
        self.wdf['power'] = np.nan
        self.assertIsNone(self.wdf.mean_max_power())

    def test_mean_max_power_missing_power(self):
        del self.wdf['power']
        with self.assertRaises(MissingDataException):
            self.assertIsNone(self.wdf.mean_max_power())

    def test_normalized_power(self):
        self.assertIsNone(self.wdf.normalized_power())

    def test_power_per_kg(self):
        self.wdf.athlete.ftp = 300
        self.assertIsNone(self.wdf.power_per_kg())

    def test_power_per_kg_missing_ftp(self):
        self.wdf.athlete.ftp = None
        with self.assertRaises(MissingDataException):
            self.wdf.power_per_kg()
