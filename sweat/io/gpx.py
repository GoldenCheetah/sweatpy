import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

from .utils import remove_duplicate_indices, resample_data


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


def read_gpx(fpath, resample: bool = False, interpolate: bool = False) -> pd.DataFrame:
    """This method loads a GPX file into a Pandas DataFrame.
    Columns names are translated to sweat terminology (e.g. "heart_rate" > "heartrate").

    Args:
        fpath: str, file-like or Path object
        resample: whether or not the data frame needs to be resampled to 1Hz
        interpolate: whether or not missing data in the data frame needs to be interpolated

    Returns:
        A pandas data frame with all the data.
    """
    tree = ET.parse(Path(fpath))
    root = tree.getroot()
    trk = root.find("default:trk", NAMESPACES)
    trkseg = trk.find("default:trkseg", NAMESPACES)

    records = []
    for trackpoint in trkseg.findall("default:trkpt", NAMESPACES):
        latitude = trackpoint.attrib.get("lat", None)
        longitude = trackpoint.attrib.get("lon", None)

        elevation = xml_find_value_or_none(trackpoint, "default:ele", NAMESPACES)

        datetime = xml_find_value_or_none(trackpoint, "default:time", NAMESPACES)

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
                latitude=pd.to_numeric(latitude),
                longitude=pd.to_numeric(longitude),
                elevation=pd.to_numeric(elevation),
                datetime=datetime,
                power=pd.to_numeric(power),
                temperature=pd.to_numeric(temperature),
                heartrate=pd.to_numeric(heartrate),
                cadence=pd.to_numeric(cadence),
            )
        )

    gpx_df = pd.DataFrame(records)
    gpx_df = gpx_df.dropna("columns", "all")
    gpx_df["datetime"] = pd.to_datetime(gpx_df["datetime"], utc=True)
    gpx_df = gpx_df.set_index("datetime")

    gpx_df = remove_duplicate_indices(gpx_df)

    gpx_df = resample_data(gpx_df, resample, interpolate)

    return gpx_df
