from enum import Enum


class DataTypeEnum(str, Enum):
    latitude = "latitude"
    longitude = "longitude"
    speed = "speed"
    power = "power"
    left_right_balance = "left-right balance"
    elevation = "elevation"
    cadence = "cadence"
    heartrate = "heartrate"
    temperature = "temperature"
    distance = "distance"
