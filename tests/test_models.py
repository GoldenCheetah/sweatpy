import unittest

import numpy as np
import pandas as pd
import pytest

from athletic_pandas import algorithms, exceptions, models


@pytest.fixture
def wdf():
    data = {
        'time': range(10),
        'heartrate': range(10),
        'power': range(10)}
    athlete = models.Athlete(name='Chris', weight=80, ftp=300)
    wdf = models.WorkoutDataFrame(data)
    wdf = wdf.set_index('time')
    wdf.athlete = athlete
    return wdf


@pytest.fixture
def wdf_small():
    athlete = models.Athlete(cp=200, w_prime=20000)
    wdf = models.WorkoutDataFrame(
        pd.read_csv('tests/example_files/workout_1_short.csv')
    )
    wdf = wdf.set_index('time')
    wdf.athlete = athlete
    return wdf


@pytest.fixture
def wdf_big():
    athlete = models.Athlete(cp=200, w_prime=20000, weight=80)
    wdf = models.WorkoutDataFrame(
        pd.read_csv('tests/example_files/workout_1.csv')
    )
    wdf = wdf.set_index('time')
    wdf.athlete = athlete
    return wdf


class TestDataPoint:
    def test_init(self):
        p = algorithms.DataPoint(1, 2)

        assert p == (1, 2)
        assert p.index == 1
        assert p.value == 2

    def test_init_missing_values(self):
        with pytest.raises(TypeError):
            algorithms.DataPoint()

    def test_init_too_many_values(self):
        with pytest.raises(TypeError):
            algorithms.DataPoint(1, 2, 3)


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
    def test_empty_init(self):
        wdf = models.WorkoutDataFrame()

        assert isinstance(wdf, pd.DataFrame)
        assert isinstance(wdf, models.WorkoutDataFrame)

    def test_init(self, wdf):
        assert 'power' in list(wdf)
        assert 'heartrate' in list(wdf)
        assert len(wdf) == 10
        assert hasattr(wdf, 'athlete')

    def test_slicing(self, wdf):
        new_wdf = wdf[1:5]

        assert isinstance(new_wdf, models.WorkoutDataFrame)

    def test_metadata_propagation(self, wdf):
        assert wdf[1:5].athlete.name == 'Chris'
        assert wdf.iloc[[0, 1], :].athlete.name == 'Chris'
        assert wdf[['power']].athlete.name == 'Chris'

    def test_is_valid(self, wdf):
        assert wdf.is_valid()

    def test_is_valid_missing_time_index(self, wdf):
        wdf.index.name = 'not_time'

        with pytest.raises(exceptions.WorkoutDataFrameValidationException):
            wdf.is_valid()

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

    def test_compute_mean_max_power(self, wdf_big):
        mmp = wdf_big.compute_mean_max_power()

        assert mmp.iloc[1] == 263.0
        assert mmp.iloc[300] == 209.37209302325581

    def test_compute_mean_max_power_missing_power(self, wdf):
        del wdf['power']

        with pytest.raises(exceptions.MissingDataException):
            assert wdf.compute_mean_max_power() is None

    def test_compute_weighted_average_power(self, wdf_big):
        assert wdf_big.compute_weighted_average_power() == 156.24624656343036

    def test_compute_weighted_average_power_missing_power(self, wdf_big):
        del wdf_big['power']

        with pytest.raises(exceptions.MissingDataException):
            wdf_big.compute_weighted_average_power()

    def test_compute_power_per_kg(self, wdf_big):
        # wdf_big.athlete.ftp = 300
        ppkg = wdf_big.compute_power_per_kg()

        assert ppkg[1] == 1.1625000000000001
        assert ppkg[100] == 1.0125

    def test_compute_power_per_kg_missing_weight(self, wdf):
        wdf.athlete.weight = None

        with pytest.raises(exceptions.MissingDataException):
            wdf.compute_power_per_kg()

    @pytest.mark.parametrize("test_input,expected", [
        (dict(), 19006.732787629098),
        (dict(algorithm='waterworth'), 19006.732787629098),
        (dict(algorithm='waterworth', tau_value=500), 19118.509110305589),
        (dict(algorithm='waterworth', tau_dynamic=True), 18989.003862950944),
        (dict(algorithm='skiba'), 19009.732787629102),
        (dict(algorithm='skiba', tau_value=500), 19121.509110305589),
        (dict(algorithm='skiba', tau_dynamic=True), 19026.724199486114),
        (dict(algorithm='froncioni'), 19189.746089851626),
    ])
    def test_compute_w_prime_balance(self, wdf_small, test_input, expected):
        w_balance = wdf_small.compute_w_prime_balance(**test_input)

        assert w_balance.iloc[800] == expected

    def test_compute_mean_max_bests(self, wdf_big):
        result = wdf_big.compute_mean_max_bests(60, 3)

        assert len(result) == 3
        assert isinstance(result[0], algorithms.DataPoint)
        assert result[0] == (2038, 215.13333333333333)
        assert result[1] == (2236, 210.48333333333332)
        assert result[2] == (2159, 208.93333333333334)

    def test_compute_mean_max_bests_only_one_result(self, wdf_big):
        result = wdf_big.compute_mean_max_bests(3000, 2)

        assert len(result) == 2
        assert not result[0] == (np.nan, np.nan)
        assert result[1] == (np.nan, np.nan)

    def test_compute_mean_max_bests_no_results(self, wdf_big):
        result = wdf_big.compute_mean_max_bests(10000, 1)

        assert len(result) == 1
        assert result[0] == (np.nan, np.nan)

    def test_compute_heartrate_model(self, wdf_big):
        model, predictions = wdf_big.compute_heartrate_model()

        assert len(predictions) == len(wdf_big)
        assert model.params['hr_rest'].value == 86.552894067943839
        assert model.params['hr_max'].value == 223.29248085198429
        assert model.params['dhr'].value == 0.26860492517685708
        assert model.params['tau_rise'].value == 51.806209961533796
        assert model.params['tau_fall'].value == 155.18880949951827
        assert model.params['hr_drift'].value == 7.9899370717145379 * 10**-5
