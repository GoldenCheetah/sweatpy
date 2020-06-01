from pathlib import Path
from typing import Generator, Union

import pandas as pd

from .fit import read_fit
from .gpx import read_gpx
from .tcx import read_tcx


def read_file(fpath: Union[str, Path], *args, **kwargs) -> pd.DataFrame:
    """This method tries to recognize the file type of the fpath argument by reading the file extension (suffix).
    Please note that this method does not support file-like objects, in contrast to the other read_* functions of sweatpy.

    Args:
        fpath: str or Path object representing the path to a file.

    Returns:
        Returns an activity as a pandas data frames.
    """
    suffix = Path(fpath).suffix.lower()

    if suffix == ".tcx":
        read_func = read_tcx
    elif suffix == ".gpx":
        read_func = read_gpx
    elif suffix == ".fit":
        read_func = read_fit
    else:
        raise ValueError(
            f"Argument fpath ({fpath}) has an unsupported file extensions (suffix): {suffix}"
        )

    return read_func(fpath, *args, **kwargs)


def read_dir(path: Union[str, Path]) -> Generator[pd.DataFrame, None, None]:
    """Generator function that returns activities in a directory as pandas data frames.

    Args:
        path: str or Path object representing the path to a directory with activity files.

    Yields:
        Yields activities as pandas data frames.

    """
    path = Path(path)

    assert path.is_dir()

    for f in path.iterdir():
        if f.is_dir():
            continue

        yield read_file(f)
