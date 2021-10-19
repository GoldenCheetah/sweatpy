from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    UNSPECIFIED = "UNSPECIFIED"


class UnitSystem(Enum):
    METRIC = "METRIC"
    STATUTE = "STATUTE"
    NAUTICAL = "NAUTICAL"


class ThresholdSetting(BaseModel):
    sport: str
    sub_sport: str
    power: Optional[int]
    speed: Optional[float]
    heartrate: Optional[int]


class Athlete(BaseModel):
    name: Optional[str]
    gender: Optional[Gender]
    age: Optional[int]
    weight: Optional[float]
    max_heartrate: Optional[int]
    unit_system: Optional[UnitSystem]
    threshold: Optional[ThresholdSetting]
    activity_class: Optional[int]

    @classmethod
    def from_fit_file(cls, user_profile, zones_target, sport):
        data = {}
        if user_profile is not None:
            fit_gender = user_profile.get("gender", None)
            if fit_gender == "male":
                data["gender"] = Gender.MALE
            elif fit_gender == "female":
                data["gender"] = Gender.FEMALE
            else:
                data["gender"] = Gender.UNSPECIFIED

            data["weight"] = user_profile.get("weight", None)
            data["height"] = user_profile.get("height", None)

            for setting in ["elev", "weight", "speed", "dist", "temperature", "height"]:
                if f"{setting}_setting" in user_profile:
                    if user_profile[f"{setting}_setting"] == "statute":
                        data["unit_system"] = UnitSystem.STATUTE
                    elif user_profile[f"{setting}_setting"] == "nautical":
                        data["unit_system"] = UnitSystem.NAUTICAL
                    else:
                        data["unit_system"] = UnitSystem.METRIC
                    break

            data["max_heartrate"] = user_profile.get("default_max_heart_rate", None)
            data["activity_class"] = user_profile.get("activity_class", None)

        if sport is not None and zones_target is not None:
            threshold_data = {}
            threshold_data["sport"] = sport["sport"]
            threshold_data["sub_sport"] = sport["sub_sport"]
            threshold_data["power"] = zones_target.get("functional_threshold_power", None)
            threshold_data["heartrate"] = zones_target.get("threshold_heart_rate", None)
            data["threshold"] = threshold_data

        return cls.parse_obj(data)
