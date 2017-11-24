import unittest

import numpy as np
import pandas as pd
import pytest

from athletic_pandas import exceptions, models


class TestDataPoint:
    def test_init(self):
        p = models.DataPoint(1, 2)

        assert p == (1, 2)
        assert p.index == 1
        assert p.value == 2

    def test_init_missing_values(self):
        with pytest.raises(TypeError):
            models.DataPoint()

    def test_init_too_many_values(self):
        with pytest.raises(TypeError):
            models.DataPoint(1, 2, 3)


class TestAthlete:
    def setup(self):
        self.athlete = models.Athlete(name='Chris', ftp=300)

    def test_empty_init(self):
        athlete = models.Athlete()
        assert hasattr(athlete, 'name')
        assert hasattr(athlete, 'sex')
        assert hasattr(athlete, 'weight')
        assert hasattr(athlete, 'dob')
        assert hasattr(athlete, 'ftp')
        assert hasattr(athlete, 'cp')
        assert hasattr(athlete, 'w_prime')

    def test_init(self):
        assert self.athlete.name == 'Chris'
        assert self.athlete.ftp == 300


class TestWorkoutDataFrame:
    def setup(self):
        data = {
            'time': range(10),
            'heartrate': range(10),
            'power': range(10)}
        athlete = models.Athlete(name='Chris', weight=80, ftp=300)
        self.wdf = models.WorkoutDataFrame(data)
        self.wdf = self.wdf.set_index('time')
        self.wdf.athlete = athlete

    def _import_csv_as_wdf(self, filename='workout_1.csv'):
        athlete = self.wdf.athlete
        self.wdf = models.WorkoutDataFrame(
            pd.read_csv('tests/example_files/{}'.format(filename)))
        self.wdf = self.wdf.set_index('time')
        self.wdf.athlete = athlete

    def test_empty_init(self):
        wdf = models.WorkoutDataFrame()

        assert isinstance(wdf, pd.DataFrame)
        assert isinstance(wdf, models.WorkoutDataFrame)

    def test_init(self):
        assert 'power' in list(self.wdf)
        assert 'heartrate' in list(self.wdf)
        assert len(self.wdf) == 10
        assert hasattr(self.wdf, 'athlete')

    def test_slicing(self):
        new_wdf = self.wdf[1:5]

        assert isinstance(new_wdf, models.WorkoutDataFrame)

    def test_metadata_propagation(self):
        assert self.wdf[1:5].athlete.name == 'Chris'
        assert self.wdf.iloc[[0, 1], :].athlete.name == 'Chris'
        assert self.wdf[['power']].athlete.name == 'Chris'

    def test_is_valid(self):
        assert self.wdf.is_valid()

    def test_is_valid_missing_time_index(self):
        self.wdf.index.name = 'not_time'

        with pytest.raises(exceptions.WorkoutDataFrameValidationException):
            self.wdf.is_valid()

    def test_is_valid_invalid_sample_rate(self):
        data = {
            'time': range(0, 20, 2),
            'heartrate': range(10),
            'power': range(10)}
        wdf = models.WorkoutDataFrame(data)
        wdf = wdf.set_index('time')

        with pytest.raises(exceptions.WorkoutDataFrameValidationException) as e:
            wdf.is_valid()
            assert e.message == '[.\n]*Sample rate is not \(consistent\) 1Hz[.\n]*'

    def test_is_valid_invalid_dtype(self):
        data = {
            'time': range(10),
            'heartrate': np.arange(0, 15, 1.5),
            'power': range(10)}
        wdf = models.WorkoutDataFrame(data)
        wdf = wdf.set_index('time')

        with pytest.raises(exceptions.WorkoutDataFrameValidationException) as e:
            wdf.is_valid()
            assert e.message == '[.\n]*Column \'heartrate\' is not of dtype[.\n]*'

    def test_is_valid_invalid_min_value(self):
        data = {
            'time': range(10),
            'heartrate': range(-10, 0),
            'power': range(10)}
        wdf = models.WorkoutDataFrame(data)
        wdf = wdf.set_index('time')

        with pytest.raises(exceptions.WorkoutDataFrameValidationException) as e:
            wdf.is_valid()
            assert e.message == '[.\n]*Column \'heartrate\' has values < 0[.\n]*'

    def test_is_valid_invalid_max_value(self):
        data = {
            'time': range(10),
            'heartrate': range(10),
            'power': range(10000, 10010)}
        wdf = models.WorkoutDataFrame(data)
        wdf = wdf.set_index('time')

        with pytest.raises(exceptions.WorkoutDataFrameValidationException) as e:
            wdf.is_valid()
            assert e.message == '[.\n]*Column \'power\' has values > 3000[.\n]*'

    def test_mean_max_power(self):
        self._import_csv_as_wdf()
        mmp = self.wdf.mean_max_power()

        assert mmp[1] == 280
        assert mmp[300] == 209.43666666666667

    def test_mean_max_power_missing_power(self):
        del self.wdf['power']

        with pytest.raises(exceptions.MissingDataException):
            assert self.wdf.mean_max_power() is None

    def test_weighted_average_power(self):
        self._import_csv_as_wdf()

        assert self.wdf.weighted_average_power() == 156.24624656343036

    def test_weighted_average_power_missing_weight(self):
        self._import_csv_as_wdf()
        self.wdf.athlete.weight = None

        assert self.wdf.weighted_average_power() == 156.24624656343036

        with pytest.raises(exceptions.MissingDataException):
            self.wdf.power_per_kg()

    def test_power_per_kg(self):
        self._import_csv_as_wdf()
        self.wdf.athlete.ftp = 300
        ppkg = self.wdf.power_per_kg()

        assert ppkg[1] == 1.1625000000000001
        assert ppkg[100] == 1.0125

    def test_power_per_kg_missing_weight(self):
        self.wdf.athlete.weight = None

        with pytest.raises(exceptions.MissingDataException):
            self.wdf.power_per_kg()

    def test_tau_w_prime_balance(self):
        self._import_csv_as_wdf()
        self.wdf.athlete.cp = 200
        self.wdf.athlete.w_prime = 20000
        tau = self.wdf._tau_w_prime_balance()
        assert tau == 482.32071983184653

    def test_w_prime_balance_waterworth(self):
        self._import_csv_as_wdf()
        self.wdf.athlete.cp = 200
        self.wdf.athlete.w_prime = 20000
        w_balance = self.wdf.w_prime_balance()

        assert len(self.wdf), len(w_balance)
        assert w_balance[0] == 20000
        assert w_balance[2500] == 18389.473009018817
        assert w_balance[3577] == 19597.259313320854

    def test_w_prime_balance_waterworth_2(self):
        self._import_csv_as_wdf()
        self.wdf.athlete.cp = 200
        self.wdf.athlete.w_prime = 20000
        w_balance = self.wdf.w_prime_balance(algorithm='waterworth')

        assert len(self.wdf) == len(w_balance)
        assert w_balance[0] == 20000
        assert w_balance[2500] == 18389.473009018817
        assert w_balance[3577] == 19597.259313320854

    def test_w_prime_balance_skiba(self):
        self._import_csv_as_wdf(filename='workout_1_short.csv')
        self.wdf.athlete.cp = 200
        self.wdf.athlete.w_prime = 20000
        w_balance = self.wdf.w_prime_balance(algorithm='skiba')

        assert len(self.wdf) == len(w_balance)
        assert w_balance[0] == 20000
        assert w_balance[500] == 19031.580246246991
        assert w_balance[900] == 19088.871117462611

    def test_w_prime_balance_froncioni(self):
        self._import_csv_as_wdf()
        self.wdf.athlete.cp = 200
        self.wdf.athlete.w_prime = 20000
        w_balance = self.wdf.w_prime_balance(algorithm='froncioni')

        assert len(self.wdf) == len(w_balance)
        assert w_balance[0] == 20000
        assert w_balance[2500] == 19369.652383790162
        assert w_balance[3577] == 19856.860886492974

    def test_compute_mean_max_bests(self):
        self._import_csv_as_wdf()
        result = self.wdf.compute_mean_max_bests(60, 3)

        assert len(result) == 3
        assert isinstance(result[0], models.DataPoint)
        assert result[0] == (2038, 215.13333333333333)
        assert result[1] == (2236, 210.48333333333332)
        assert result[2] == (2159, 208.93333333333334)

    def test_compute_mean_max_bests_only_one_result(self):
        self._import_csv_as_wdf()
        result = self.wdf.compute_mean_max_bests(3000, 2)

        assert len(result) == 2
        assert not result[0] == (np.nan, np.nan)
        assert result[1] == (np.nan, np.nan)

    def test_compute_mean_max_bests_no_results(self):
        self._import_csv_as_wdf()
        result = self.wdf.compute_mean_max_bests(10000, 1)

        assert len(result) == 1
        assert result[0] == (np.nan, np.nan)
