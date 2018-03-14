import pytest
import numpy as np
import pandas as pd
from unittest import mock
from sweat.algorithms.metrics.core import (mask_fill, rolling_mean,
                                           median_filter, compute_zones,
                                           best_interval, time_in_zones,
                                           weighted_average_power, mean_max,
                                           multiple_best_intervals, DataPoint)


class TestMaskFill():

    def test_mask_fill_no_mask(self):

        arg = [1, 1, 1]
        expected = [1, 1, 1]

        rv = mask_fill(arg)
        assert type(rv) == list
        assert rv == expected


    def test_mask_fill(self):

        arg = [1, 1, 1]
        mask = [True, False, True]
        expected = [1, 3.0, 1]

        rv = mask_fill(arg, mask=mask, value=3.0)
        assert type(rv) == list
        assert rv == expected

        arg = np.array([1, 1, 1])
        mask = [True, False, True]
        expected = np.array([1, 3.0, 1])

        rv = mask_fill(arg, mask=mask, value=3.0)
        assert type(rv) == np.ndarray
        assert (rv == expected).all()


class TestRollingMean():

    def test_rolling_mean_ndarray(self):
        stream = np.asarray([1, 2, 3, 4, 5])
        expected = np.asarray([1, 1.5, 2.5, 3.5, 4.5])

        rv = rolling_mean(stream, 2)

        assert type(rv) == np.ndarray
        assert (rv == expected).all()


    def test_rolling_mean_list(self):
        stream = [1, 2, 3, 4, 5]
        expected = [1, 1.5, 2.5, 3.5, 4.5]
        rv = rolling_mean(stream, 2)

        assert type(rv) == list
        assert rv == expected


    def test_rolling_mean_list_with_mask(self):
        stream = [1, 2, 3, 4, 5]
        mask = [True, True, False, True, True]
        expected = [1, 1.5, 1.0, 2.0, 4.5]
        rv = rolling_mean(stream, window=2, mask=mask)

        assert type(rv) == list
        assert rv == expected


    def test_rolling_mean_with_mask_ndarray(self):
        stream = np.asarray([1, 2, 3, 4, 5])
        mask = np.asarray([True, True, False, True, True], dtype=bool)
        expected = np.asarray([1, 1.5, 1.0, 2.0, 4.5])
        rv = rolling_mean(stream, window=2, mask=mask)

        assert type(rv) == np.ndarray
        assert (rv == expected).all()


    def test_rolling_mean_list_emwa(self):
        stream = list(np.ones(30))
        expected = list(np.ones(30))
        rv = rolling_mean(stream, 2, type='ewma')

        assert type(rv) == list
        assert rv == expected


    def test_rolling_mean_real_data(self, test_stream):
        rv = rolling_mean(test_stream['watts'],
                                  mask=test_stream['moving'],
                                  window=1)

        assert type(rv) == list
        assert rv == test_stream['watts']


class TestMedianFilter():

    def test_median_filter(self):
        stream = np.ones(60)
        stream[-1] = 2

        rv = median_filter(stream)
        assert type(rv) == np.ndarray
        assert (rv == np.ones(60)).all()


    def test_median_filter_list(self):
        stream = np.ones(60)
        stream[-1] = 2
        stream = stream.tolist()

        expected = np.ones(60)
        expected = expected.tolist()

        rv = median_filter(stream)

        assert type(rv) == list
        assert rv == expected


    def test_median_filter_with_replacement(self):
        stream = np.ones(60)
        stream[-1] = 2

        expected = np.ones(60)
        expected[-1] = 10

        rv = median_filter(stream, value=10)

        assert type(rv) == np.ndarray
        assert (rv == expected).all()


class TestComputeZones():

    def test_zones_power_ftp_list(self):
        stream = [0.55, 0.75, 0.9, 1.05, 1.2, 1.5, 10.0]
        expected = [1, 2, 3, 4, 5, 6, 7]

        rv = compute_zones(stream, ftp=1.0)

        assert type(rv) == list
        assert rv == expected


    def test_zones_heart_rate_lthr_list(self):
        stream = [0.6, 0.8, 0.9, 1.0, 1.1]
        expected = [1, 2, 3, 4, 5]

        rv = compute_zones(stream, lthr=1.0)

        assert type(rv) == list
        assert rv == expected


    def test_zones_power_explicit_zones_list(self):
        stream = [1, 150, 210, 250, 300, 350, 450]
        expected = [1, 2, 3, 4, 5, 6, 7]

        rv = compute_zones(stream, zones=[-1, 144, 196, 235, 274, 313, 391, 10000])

        assert type(rv) == list
        assert rv == expected


    def test_zones_heart_rate_explicit_zones_list(self):
        stream = [60, 120, 150, 160, 170, 180]
        expected = [1, 1, 2, 3, 4, 5]

        rv = compute_zones(stream, zones=[-1, 142, 155, 162, 174, 10000])

        assert type(rv) == list
        assert rv == expected


    def test_zones_power_ftp_list_of_int(self):
        stream = [1, 2, ]
        ftp = 1.0
        expected = [4, 7, ]

        rv = compute_zones(stream, ftp=ftp)

        assert type(rv) == list
        assert rv == expected


    def test_zones_power_ftp_unordered_list(self):
        stream = [2, 1, 3]
        ftp = 1.0
        expected = [7, 4, 7, ]

        rv = compute_zones(stream, ftp=ftp)

        assert type(rv) == list
        assert rv == expected


    def test_zones_power_ftp_ndarray(self):
        stream = np.asarray([0.55, 0.75, 0.9, 1.05, 1.2, 1.5, 10.0])
        expected = np.asarray(list(range(1, 8)))

        rv = compute_zones(stream, ftp=1.0)

        assert type(rv) == np.ndarray
        assert (rv == expected).all()


class TestBestInterval():

    @mock.patch('sweat.algorithms.metrics.core.rolling_mean')
    def test_best_interval(self, test_rolling_mean):
        stream = [1, 1, 1, 1, 1]
        test_rolling_mean.return_value = stream

        assert best_interval(stream, 5) == 1


class TestTimeInZones():

    @mock.patch('sweat.algorithms.metrics.core.compute_zones')
    def test_time_in_zones(self, zones):
        power = [0.55, 0.75, 0.9, 1.05, 1.2, 1.5, 10.0]
        zones.return_value = [1, 2, 3, 4, 5, 6, 7]

        rv = time_in_zones(power, ftp=1.0)
        expected = [1, 1, 1, 1, 1, 1, 1]

        assert type(rv) == list
        assert rv == expected


class TestWeightedAveragePower():

    def test_wap(self):
        stream = np.ones(30)
        moving = np.ones(30, dtype=bool)

        assert weighted_average_power(stream, moving) == 1


    def test_normalized_power_xpower(self):
        stream = np.ones(30)
        moving = np.ones(30, dtype=bool)

        assert weighted_average_power(stream, moving, type='xPower') == 1


class TestMeanMax():

    def test_power_duration_curve(self):
        power = np.arange(101)
        rv = mean_max(power)

        assert type(power) == np.ndarray
        assert rv[0] == 100.0
        assert rv[49] == 75.5
        assert rv[-1] == 50.5


    def test_power_duration_curve_list(self):
        stream = [0, 0, 0]
        expected = [0, 0]

        rv = mean_max(stream)

        assert type(rv) == list
        assert rv == expected


    def test_power_duration_curve_ndarray(self):
        stream = np.zeros(3)
        expected = np.zeros(2)

        rv = mean_max(stream)

        assert type(rv) == np.ndarray
        assert (rv == expected).all()


    def test_power_duration_curve_series(self):
        stream = pd.Series(np.zeros(3))
        expected = pd.Series(np.zeros(2))

        rv = mean_max(stream)

        assert type(rv) == pd.Series
        assert (rv == expected).all()


class TestMultipleBestIntervals():

    def test_mean_max_bests(self, power):
        bests = multiple_best_intervals(power, 3, 3)

        assert len(bests) == 3
        assert isinstance(bests[0], DataPoint)
        assert bests[0].index == 99
        assert bests[0].value == 98.0
        assert bests[2].index == 91
        assert bests[2].value == 90.0


class TestDataPoint:
    def test_init(self):
        p = DataPoint(1, 2)

        assert p == (1, 2)
        assert p.index == 1
        assert p.value == 2

    def test_init_missing_values(self):
        with pytest.raises(TypeError):
            DataPoint()

    def test_init_too_many_values(self):
        with pytest.raises(TypeError):
            DataPoint(1, 2, 3)



