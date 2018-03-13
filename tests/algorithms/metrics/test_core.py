import numpy as np
from sweat.algorithms.metrics.core import (mask_fill, rolling_mean,
                                           median_filter)


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

