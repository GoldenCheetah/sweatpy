import pandas as pd
import pytest


@pytest.fixture
def power():
    return pd.Series(range(100))
