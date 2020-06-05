import numpy as np
import pytest
from sklearn.utils.estimator_checks import check_estimator

import sweat
from sweat.pdm import regressors


@pytest.mark.skip()
def test_top_level_import():
    assert sweat.CriticalPowerRegressor == regressors.CriticalPowerRegressor


class TestCriticalPowerRegressor:
    @pytest.mark.skip()
    def test_base(self):
        check_estimator(sweat.CriticalPowerRegressor())

    def test_2_param(self):
        cpreg = sweat.CriticalPowerRegressor()
        cpreg.fit([[1.0], [60.0], [1200.0]], [1500.0, 600.0, 350.0])
        assert isinstance(cpreg.predict([[60], [61]]), np.ndarray)
        assert hasattr(cpreg, "cp_")
        assert hasattr(cpreg, "w_prime_")

        cpreg = sweat.CriticalPowerRegressor(model="2 param")
        cpreg.fit([[1.0], [60.0], [1200.0]], [1500.0, 600.0, 350.0])
        assert isinstance(cpreg.predict([[60], [61]]), np.ndarray)
        assert hasattr(cpreg, "cp_")
        assert hasattr(cpreg, "w_prime_")

    def test_3_param(self):
        cpreg = sweat.CriticalPowerRegressor(model="3 param")
        cpreg.fit([[1.0], [60.0], [1200.0]], [1500.0, 600.0, 350.0])
        assert isinstance(cpreg.predict([[60], [61]]), np.ndarray)
        assert hasattr(cpreg, "cp_")
        assert hasattr(cpreg, "w_prime_")
        assert hasattr(cpreg, "p_max_")
