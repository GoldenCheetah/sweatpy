from dataclasses import dataclass, field
from typing import List

import pandas as pd


def resample_data(data, resample: bool, interpolate: bool) -> pd.DataFrame:
    """Function to calculate the mean max power for all available activities.

    Args:
        data: The data frame that needs to be resampled and/or interpolated
        resample: whether or not the data frame needs to be resampled to 1Hz
        interpolate: whether or not missing data in the data frame needs to be interpolated

    Returns:
        Returns the resampled and interpolated dataframe

    """
    if resample:
        data = data.resample("1S").mean()

    if interpolate:
        data = data.interpolate(method="linear")

    return data


def remove_duplicate_indices(data: pd.DataFrame, keep="first") -> pd.DataFrame:
    """Function that removes duplicate indices

    Args:
        data: The data frame for which duplicate indices need to be deleted
        keep: Determines which duplicates (if any) to mark. See pandas.DataFrame.index.duplicated documentation for more information

    Returns:
        Returns the data frame with duplicate indices removed

    """
    return data[~data.index.duplicated(keep=keep)]


def semicircles_to_degrees(semicircles):
    return semicircles * (180 / (2 ** 31))


def create_empty_dataframe():
    df = pd.DataFrame()
    df.index = pd.to_datetime(df.index)
    return df


@dataclass
class Sensor:
    name: str
    product_id: str = None
    serial_number: str = None
    metadata: dict = field(default_factory=dict)


@dataclass
class Device:
    name: str
    product_id: str = None
    serial_number: str = None
    metadata: dict = field(default_factory=dict)
    sensors: List[Sensor] = field(default_factory=list)
