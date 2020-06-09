import numpy as np
import pytest
from sklearn.utils.estimator_checks import check_estimator

import sweat
from sweat.pdm import regressors


@pytest.mark.skip()
def test_top_level_import():
    assert sweat.PowerDurationRegressor == regressors.PowerDurationRegressor


class TestPowerDurationRegressor:
    @pytest.mark.skip()
    def test_base(self):
        check_estimator(sweat.PowerDurationRegressor())

    def test_2_param(self):
        cpreg = sweat.PowerDurationRegressor()
        cpreg.fit([[1.0], [60.0], [1200.0]], [1500.0, 600.0, 350.0])
        assert isinstance(cpreg.predict([[60], [61]]), np.ndarray)
        assert hasattr(cpreg, "cp_")
        assert hasattr(cpreg, "w_prime_")

        cpreg = sweat.PowerDurationRegressor(model="2 param")
        cpreg.fit([[1.0], [60.0], [1200.0]], [1500.0, 600.0, 350.0])
        assert isinstance(cpreg.predict([[60], [61]]), np.ndarray)
        assert hasattr(cpreg, "cp_")
        assert hasattr(cpreg, "w_prime_")

    def test_3_param(self):
        cpreg = sweat.PowerDurationRegressor(model="3 param")
        cpreg.fit([[1.0], [60.0], [1200.0]], [1500.0, 600.0, 350.0])
        assert isinstance(cpreg.predict([[60], [61]]), np.ndarray)
        assert hasattr(cpreg, "cp_")
        assert hasattr(cpreg, "w_prime_")
        assert hasattr(cpreg, "p_max_")

    def test_exp(self):
        cpreg = sweat.PowerDurationRegressor(model="exponential")
        cpreg.fit([[1.0], [60.0], [1200.0]], [1500.0, 600.0, 350.0])
        assert isinstance(cpreg.predict([[60], [61]]), np.ndarray)
        assert hasattr(cpreg, "cp_")
        assert hasattr(cpreg, "p_max_")
        assert hasattr(cpreg, "tau")

    def test_omni(self):
        cpreg = sweat.PowerDurationRegressor(model="omni")
        cpreg.fit([[1.0], [60.0], [1200.0], [3600.0]], [1500.0, 600.0, 350.0, 300.0])
        assert isinstance(cpreg.predict([[60], [61]]), np.ndarray)
        assert hasattr(cpreg, "cp_")
        assert hasattr(cpreg, "p_max_")
        assert hasattr(cpreg, "w_prime_")
        assert hasattr(cpreg, "a_")
