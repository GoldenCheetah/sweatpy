import pandas as pd
import pytest

from athletic_pandas.algorithms import critical_power, main


@pytest.mark.parametrize('version,expected', [
    ('5_3', [520.7906012962726, 371.41971316054241, 500]),
    ('7_3', [406.62249287047558, 201.27837128971581, 500]),
])
def test_extended_critical_power(version, expected):
    power = pd.Series(range(500))
    mean_max_power = main.mean_max_power(power)
    ecp = critical_power.extended_critical_power(mean_max_power, version=version)
    assert ecp[1] == expected[0]
    assert ecp[250] == expected[1]
    assert len(ecp) == expected[2]
