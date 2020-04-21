import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd


NAMESPACES = {
    "default": "http://www.topografix.com/GPX/1/1",
    "gpxtpx": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1",
    "gpxx": "http://www.garmin.com/xmlschemas/GpxExtensions/v3",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


def xml_find_value_or_none(element, match, namespaces=None):
    e = element.find(match, namespaces=namespaces)
    if e is None:
        return e
    else:
        return e.text


def read_gpx(fpath):
    tree = ET.parse(Path(fpath))
    root = tree.getroot()
    trk = root.find("default:trk", NAMESPACES)
    trkseg = trk.find("default:trkseg", NAMESPACES)

    records = []
    for trackpoint in trkseg.findall("default:trkpt", NAMESPACES):
        latitude = trackpoint.attrib.get("lat", None)
        longitude = trackpoint.attrib.get("lon", None)

        elevation = xml_find_value_or_none(trackpoint, "default:ele", NAMESPACES)

        timestamp = xml_find_value_or_none(trackpoint, "default:time", NAMESPACES)

        extensions = trackpoint.find("default:extensions", NAMESPACES)

        power = xml_find_value_or_none(extensions, "default:power", NAMESPACES)

        trackpoint_extension = extensions.find("gpxtpx:TrackPointExtension", NAMESPACES)

        temperature = xml_find_value_or_none(
            trackpoint_extension, "gpxtpx:atemp", NAMESPACES
        )
        heartrate = xml_find_value_or_none(
            trackpoint_extension, "gpxtpx:hr", NAMESPACES
        )
        cadence = xml_find_value_or_none(trackpoint_extension, "gpxtpx:cad", NAMESPACES)

        records.append(
            dict(
                latitude=latitude,
                longitude=longitude,
                elevation=elevation,
                timestamp=timestamp,
                power=power,
                temperature=temperature,
                heartrate=heartrate,
                cadence=cadence,
            )
        )

    gpx_df = pd.DataFrame(records)
    gpx_df = gpx_df.dropna("columns", "all")

    return gpx_df
