import numpy as np
import pandas as pd
import pytest

import sweat


class TestSweatAccessor:
    def test_accessor(self):
        example = sweat.examples(path="4078723797.fit")
        data = sweat.read_fit(example.path)
        mean_max_data = data.sweat.mean_max("power")

        assert isinstance(mean_max_data, pd.DataFrame)
        assert isinstance(mean_max_data.index, pd.TimedeltaIndex)
        assert "mean_max_power" in mean_max_data.columns
        assert len(mean_max_data) == len(data) - 1

    def test_accessor_no_datetimeindex(self):
        data = pd.DataFrame(dict(power=range(10)), index=range(10))

        with pytest.raises(AttributeError):
            data.sweat.mean_max("power")

    def test_accessor_not_1hz(self):
        example = sweat.examples(path="2020-06-01-16-52-40.fit")
        data = sweat.read_fit(example.path)

        with pytest.raises(AttributeError):
            data.sweat.mean_max("power")

    def test_accessor_relative_index(self):
        example = sweat.examples(path="4078723797.fit")
        data = sweat.read_fit(example.path)

        data = data.sweat.to_timedelta_index()

        assert isinstance(data, pd.DataFrame)
        assert isinstance(data.index, pd.TimedeltaIndex)
        assert "power" in data.columns


class TestSweatSeriesAccessor:
    def test_accessor(self):
        example = sweat.examples(path="4078723797.fit")
        data = sweat.read_fit(example.path)
        mean_max = data["power"].sweat.mean_max()

        assert isinstance(mean_max, pd.Series)
        assert isinstance(mean_max.index, pd.TimedeltaIndex)
        assert mean_max.name == "mean_max_power"
        assert len(mean_max) == len(data) - 1

    def test_accessor_no_datetimeindex(self):
        data = pd.DataFrame(dict(power=range(10)), index=range(10))

        with pytest.raises(AttributeError):
            data["power"].sweat.mean_max()

    def test_accessor_not_1hz(self):
        example = sweat.examples(path="2020-06-01-16-52-40.fit")
        data = sweat.read_fit(example.path)

        with pytest.raises(AttributeError):
            data["power"].sweat.mean_max()

    def test_accessor_relative_index(self):
        example = sweat.examples(path="4078723797.fit")
        data = sweat.read_fit(example.path)

        data = data["power"].sweat.to_timedelta_index()

        assert isinstance(data, pd.Series)
        assert isinstance(data.index, pd.TimedeltaIndex)
        assert data.name == "power"

    def test_accessor_compute_zones(self):
        example = sweat.examples(path="4078723797.fit")
        data = sweat.read_fit(example.path)

        zones = data["heartrate"].sweat.calculate_zones(
            [0, 100, 150, np.inf], ["zone 1", "zone 2", "zone 3"]
        )
        assert len(zones) == len(data)
        assert set(zones.unique()) == set(["zone 1", "zone 2", "zone 3"])

    def test_accessor_time_in_zone(self):
        example = sweat.examples(path="4078723797.fit")
        data = sweat.read_fit(example.path)

        time_in_zone = data["heartrate"].sweat.time_in_zone(
            [0, 100, 150, np.inf], ["zone 1", "zone 2", "zone 3"]
        )
        assert set(time_in_zone.index.unique()) == set(["zone 1", "zone 2", "zone 3"])
