import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

from .utils import (
    create_empty_dataframe,
    remove_duplicate_indices,
    resample_data,
    Device,
    Sensor,
)


NAMESPACES = {
    "default": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
    "ns5": "http://www.garmin.com/xmlschemas/ActivityGoals/v1",
    "ns3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2",
    "ns2": "http://www.garmin.com/xmlschemas/UserProfile/v2",
}


def xml_find_value_or_none(element, match, namespaces=None):
    if element is None:
        return None

    e = element.find(match, namespaces=namespaces)
    if e is None:
        return e
    else:
        return e.text


def process_tcx_tree(elements, metadata, name):
    records = []
    lap_no = 0
    session = 0
    for element in elements.findall(f"default:{name}", NAMESPACES):
        if name == "Course":
            laps = [element]
        else:
            laps = element.findall("default:Lap", NAMESPACES)

        for lap in laps:
            track = lap.find("default:Track", NAMESPACES)
            for trackpoint in track.findall("default:Trackpoint", NAMESPACES):
                datetime = xml_find_value_or_none(
                    trackpoint, "default:Time", NAMESPACES
                )
                elevation = xml_find_value_or_none(
                    trackpoint, "default:AltitudeMeters", NAMESPACES
                )
                distance = xml_find_value_or_none(
                    trackpoint, "default:DistanceMeters", NAMESPACES
                )
                cadence = xml_find_value_or_none(
                    trackpoint, "default:Cadence", NAMESPACES
                )

                position = trackpoint.find("default:Position", NAMESPACES)
                latitude = xml_find_value_or_none(
                    position, "default:LatitudeDegrees", NAMESPACES
                )
                longitude = xml_find_value_or_none(
                    position, "default:LongitudeDegrees", NAMESPACES
                )

                hr = trackpoint.find("default:HeartRateBpm", NAMESPACES)
                heartrate = xml_find_value_or_none(hr, "default:Value", NAMESPACES)

                extensions = trackpoint.find("default:Extensions", NAMESPACES)
                if extensions:
                    tpx = extensions.find("ns3:TPX", NAMESPACES)
                    speed = xml_find_value_or_none(tpx, "ns3:Speed", NAMESPACES)
                    power = xml_find_value_or_none(tpx, "ns3:Watts", NAMESPACES)
                else:
                    speed = None
                    power = None

                records.append(
                    dict(
                        datetime=datetime,
                        latitude=latitude,
                        longitude=longitude,
                        elevation=elevation,
                        heartrate=heartrate,
                        cadence=cadence,
                        distance=distance,
                        speed=speed,
                        power=power,
                        lap=lap_no,
                        session=session,
                    )
                )
            lap_no += 1

        device = None
        if metadata:
            creator = element.find("default:Creator", NAMESPACES)
            device_name = xml_find_value_or_none(creator, "default:Name", NAMESPACES)
            unit_id = xml_find_value_or_none(creator, "default:UnitId", NAMESPACES)
            product_id = xml_find_value_or_none(
                creator, "default:ProductID", NAMESPACES
            )

            device = Device(
                name=device_name,
                product_id=product_id,
                serial_number=unit_id,
                metadata={"creator_xml": creator},
            )

    tcx_df = pd.DataFrame(records)

    return tcx_df, device


def process_tcx_activities(activities, metadata):
    return process_tcx_tree(activities, metadata, name="Activity")


def process_tcx_courses(courses, metadata):
    return process_tcx_tree(courses, metadata, name="Course")


def postprocess(tcx_df, device, resample, interpolate, metadata):
    if tcx_df.empty:
        return create_empty_dataframe()

    tcx_df = tcx_df.dropna(axis="columns", how="all")
    tcx_df["datetime"] = pd.to_datetime(tcx_df["datetime"], utc=True)
    tcx_df = tcx_df.set_index("datetime")

    # Convert columns to numeric if possible
    tcx_df = tcx_df.apply(pd.to_numeric, errors="ignore")

    tcx_df = remove_duplicate_indices(tcx_df)

    tcx_df = resample_data(tcx_df, resample, interpolate)

    if not metadata:
        return tcx_df

    return {
        "data": tcx_df,
        "device": device,
    }


def read_tcx(
    fpath, resample: bool = False, interpolate: bool = False, metadata: bool = False
) -> pd.DataFrame:
    """This method loads a TCX file into a Pandas DataFrame.
    Columns names are translated to sweat terminology (e.g. "heart_rate" > "heartrate").

    Args:
        fpath: str, file-like or Path object
        resample: whether or not the data frame needs to be resampled to 1Hz
        interpolate: whether or not missing data in the data frame needs to be interpolated
        metadata: whether to return metadata. Note: If set to True this method will return a dictionairy instead of a data frame.

    Returns:
        A pandas data frame with all the data.
    """
    tree = ET.parse(Path(fpath))
    root = tree.getroot()

    activities = root.find("default:Activities", NAMESPACES)
    if activities is not None:
        tcx_df, device = process_tcx_activities(activities, metadata)

        return postprocess(tcx_df, device, resample, interpolate, metadata)
    
    courses = None
    for child in root:
        if child.tag.endswith("Courses"):
            courses = child
    # courses = root.findall("default:Courses", NAMESPACES)
    if courses is not None:
        tcx_df, device = process_tcx_courses(courses, metadata)

        return postprocess(tcx_df, device, resample, interpolate, metadata)
    
    raise TypeError("Unsupported gpx file format: This gpx file does not seem to contain either activities or courses.")
