import pandas as pd
import pytest

from athletic_pandas.algorithms import heartrate_models


def test_heartrate_model():
    heartrate = pd.Series(range(50))
    power = pd.Series(range(0, 100, 2))

    model, predictions = heartrate_models.heartrate_model(heartrate, power)

    assert model.params['hr_rest'].value == 0.00039182374117378518
    assert model.params['hr_max'].value == 195.75616175654685
    assert model.params['dhr'].value == 0.49914432620946803
    assert model.params['tau_rise'].value == 0.98614419733274383
    assert model.params['tau_fall'].value == 22.975975612579408
    assert model.params['hr_drift'].value == 6.7232899323328612 * 10**-5
    assert len(predictions) == 50
