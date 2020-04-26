import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd


NAMESPACES = {
    "default": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
    "ns5": "http://www.garmin.com/xmlschemas/ActivityGoals/v1",
    "ns3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2",
    "ns2": "http://www.garmin.com/xmlschemas/UserProfile/v2",
}


def xml_find_value_or_none(element, match, namespaces=None):
    e = element.find(match, namespaces=namespaces)
    if e is None:
        return e
    else:
        return e.text


def read_tcx(fpath):
    tree = ET.parse(Path(fpath))
    root = tree.getroot()
    activities = root.find("default:Activities", NAMESPACES)

    records = []
    for activity in activities.findall("default:Activity", NAMESPACES):
        for lap in activity.findall("default:Lap", NAMESPACES):
            track = lap.find("default:Track", NAMESPACES)
            for trackpoint in track.findall("default:Trackpoint", NAMESPACES):
                timestamp = xml_find_value_or_none(
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
                        timestamp=timestamp,
                        latitude=latitude,
                        longitude=longitude,
                        elevation=elevation,
                        heartrate=heartrate,
                        cadence=cadence,
                        distance=distance,
                        speed=speed,
                        power=power,
                    )
                )

    tcx_df = pd.DataFrame(records)
    tcx_df = tcx_df.dropna("columns", "all")

    return tcx_df
