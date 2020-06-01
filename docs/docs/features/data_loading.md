# Data loading

*Sweatpy* has built-in support for loading these activity file formats:

- [FIT files](#fit-files)
- [GPX files](#gpx-files)
- [TCX files](#tcx-files)

Helper functions:

- [`read_file()`](#helper-functions), that automatically determines the file format.
- [`read_dir()`](#helper-functions), that iterates over all the files in a directory.


## FIT files
The `read_fit()` function accepts strings, [pathlib](https://docs.python.org/3/library/pathlib.html) objects and other file-like objects and returns a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with column names matching *Sweatpy* [nomenclature](nomenclature.md).

Usage:
```python
import sweat


data = sweat.read_fit("path/to/file.fit")
```

Example:
```python
import sweat


example_fit = sweat.examples(path="4078723797.fit")

data = sweat.read_fit(example_fit.path)
```

## GPX files
The `read_gpx()` function accepts strings, [pathlib](https://docs.python.org/3/library/pathlib.html) objects and other file-like objects and returns a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with column names matching *Sweatpy* [nomenclature](nomenclature.md).

Usage:
```python
import sweat


data = sweat.read_gpx("path/to/file.gpx")
```

Example:
```python
import sweat


example_gpx = sweat.examples(path="4078723797_strava.gpx")

data = sweat.read_gpx(example_gpx.path)
```

## TCX files
The `read_tcx()` function accepts strings, [pathlib](https://docs.python.org/3/library/pathlib.html) objects and other file-like objects and returns a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with column names matching *Sweatpy* [nomenclature](nomenclature.md).

Usage:
```python
import sweat


data = sweat.read_gpx("path/to/file.gpx")
```

Example:
```python
import sweat


example_tcx = sweat.examples(path="3173437224.tcx")

data = sweat.read_tcx(example_tcx.path)
```

## Helper functions
`read_file()` works exactly as the other `read_*()` functions but tries to automatically determine the file format.
It raises a `ValueError` when the file format cannot be determined or is not supported.
Please note that the `read_file()` does not support passing file-like objects.

Example:
```python
import sweat


example_tcx = sweat.examples(path="3173437224.tcx")

data = sweat.read_file(example_tcx.path)
```

`read_dir()` allows you to read all the files in a directory and iterate over them.
It uses `read_file()` under the hood and returns a generator.
Please note that `read_dir()` expects **all** the files in the directory to be of a supported file format.

Example:
```python
from pathlib import Path

import sweat


directory = Path("path/to/some/dir/")

for activity in sweat.read_dir(directory):
    # Do things with the activities
```

## Resampling
All `read_*()` functions accept a `resample` and `interpolate` argument (both `False` by default) that can trigger a resampling to 1Hz and subsequent linear interpolation of the data for files that are not sampled (consistently) at 1Hz, as some Garmin devices with "smart recording mode" do.

```python
import sweat


example_tcx = sweat.examples(path="3173437224.tcx")

data = sweat.read_tcx(example_tcx.path, resample=True, interpolate=True)
```
