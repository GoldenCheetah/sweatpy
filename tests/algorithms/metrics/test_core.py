import numpy as np
from sweat.algorithms.metrics.core import mask_fill


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