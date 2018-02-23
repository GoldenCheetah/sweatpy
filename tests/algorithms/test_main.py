import pandas as pd
import pytest

from athletic_pandas.algorithms import main


class TestDataPoint:
    def test_init(self):
        p = main.DataPoint(1, 2)

        assert p == (1, 2)
        assert p.index == 1
        assert p.value == 2

    def test_init_missing_values(self):
        with pytest.raises(TypeError):
            main.DataPoint()

    def test_init_too_many_values(self):
        with pytest.raises(TypeError):
            main.DataPoint(1, 2, 3)


@pytest.fixture
def power():
    return pd.Series(range(100))


def test_mean_max_power(power):
    mmp = main.mean_max_power(power)
    assert mmp.iloc[0] == 99.0
    assert mmp.iloc[10] == 94.0
    assert mmp.iloc[-1] == 49.5

def test_mean_max_bests(power):
    bests = main.mean_max_bests(power, 3, 3)

    assert len(bests) == 3
    assert isinstance(bests[0], main.DataPoint)
    assert bests[0].index == 99
    assert bests[0].value == 98.0
    assert bests[2].index == 91
    assert bests[2].value == 90.0

def test_weighted_average_power(power):
    wap = main.weighted_average_power(power)

    assert wap == 59.45534981958064

def test_power_per_kg(power):
    ppkg = main.power_per_kg(power, 80.0)

    assert len(ppkg) == len(power)
    assert ppkg.iloc[0] == 0.0
    assert ppkg.iloc[50] == 0.625
    assert ppkg.iloc[-1] == 1.2375
