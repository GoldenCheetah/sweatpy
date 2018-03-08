import pandas as pd
import pytest

from athletic_pandas.algorithms import w_prime_balance


def test_tau_w_prime_balance(power):
    tau = w_prime_balance.tau_w_prime_balance(power, cp=25)
    assert tau == 795.44010528262652

def test_tau_w_prime_balance_with_untill(power):
    tau = w_prime_balance.tau_w_prime_balance(power, cp=25, untill=15)
    assert tau == 772.05753543055448

@pytest.mark.parametrize("test_input,expected", [
    (dict(tau_dynamic=False, tau_value=None), [795.44010528262652]*2),
    (dict(tau_dynamic=True, tau_value=None), [741.2252275569871, 795.44010528262652]),
    (dict(tau_dynamic=False, tau_value=100), [100, 100, 100]),
])
def test_get_tau_method(power, test_input, expected):

    tau_method = w_prime_balance.get_tau_method(power, cp=25, **test_input)
    assert tau_method(0) == expected[0]
    assert tau_method(99) == expected[1]

@pytest.mark.parametrize("test_input,expected", [
    (dict(tau_dynamic=False, tau_value=None), 750.77417744392937),
    (dict(tau_dynamic=True, tau_value=None), 750.77417744392937),
    (dict(tau_dynamic=False, tau_value=100), 909.61894732869769),
])
def test_w_prime_balance_waterworth(power, test_input, expected):
    w_bal = w_prime_balance.w_prime_balance_waterworth(power, cp=25,
                                                  w_prime=2000, **test_input)
    assert w_bal.iloc[75] == expected

@pytest.mark.parametrize("test_input,expected", [
    (dict(tau_dynamic=False, tau_value=None), 750.77417744392892),
    (dict(tau_dynamic=True, tau_value=None), 750.77417744392892),
    (dict(tau_dynamic=False, tau_value=100), 909.61894732869769),
])
def test_w_prime_balance_skiba(power, test_input, expected):
    w_bal = w_prime_balance.w_prime_balance_skiba(power, cp=25,
                                             w_prime=2000, **test_input)
    assert w_bal.iloc[75] == expected

def test_w_prime_balance_froncioni(power):
    w_bal = w_prime_balance.w_prime_balance_froncioni_skiba_clarke(power, cp=25,
                                                 w_prime=2000)
    assert w_bal.iloc[75] == 725.0

@pytest.mark.parametrize("test_input,expected", [
    (dict(), 1678.2431086242659),
    (dict(algorithm='waterworth'), 1678.2431086242659),
    (dict(algorithm='waterworth', tau_value=500), 1680.1356439412966),
    (dict(algorithm='waterworth', tau_dynamic=True), 1678.2431086242659),
    (dict(algorithm='skiba'), 1678.2431086242659),
    (dict(algorithm='skiba', tau_value=500), 1680.1356439412966),
    (dict(algorithm='skiba', tau_dynamic=True), 1678.2431086242659),
    (dict(algorithm='froncioni-skiba-clarke'), 1675.0),
])
def test_w_prime_balance(power, test_input, expected):
    w_bal = w_prime_balance.w_prime_balance(power, cp=25, w_prime=2000,
                                       **test_input)
    assert w_bal.iloc[50] == expected
