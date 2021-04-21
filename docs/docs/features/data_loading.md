# Data loading

*Sweatpy* has built-in support for loading these activity file formats:

- [FIT files](#fit-files)
- [GPX files](#gpx-files)
- [TCX files](#tcx-files)

...and loading data from these services:

- [Strava](#strava)

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

### HRV data
The `read_fit()` function accepts an `hrv=True` parameter.
When set to `True` (default is `False`) a dictionairy is returned, with the dataframe in the key "data" and a [pandas.Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html) with RR intervals in the "hrv" key.

```python
import sweat


example_fit = sweat.examples(path="4078723797.fit")

data = sweat.read_fit(example_fit.path, hrv=True)

data["hrv"]
-> pd.Series
```

### Pool length data
When reading FIT files from pool swims, you can use the `pool_lengths=True` parameter.
When set to `True` (default is `False`) a dictionairy is returned, with the dataframe in the key "data" and a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with pool length records in the "pool_lengths" key.

```python
import sweat


example_fit = sweat.examples(path="4078723797.fit")

data = sweat.read_fit(example_fit.path, pool_lengths=True)

data["pool_lengths"]
-> pd.DataFrame
```


### Summaries
The `read_fit()` function accepts a `summaries=True` parameter.
When set to `True` (default is `False`) a dictionairy is returned, with the dataframe in the "data" key, and in the keys "activity", "session" and "laps" relevant summaries:

- "activity": a dictionairy with a summary of the entire activity.
- "sessions": a [pandas.DataFrames](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with summaries of each session. Only for multi session FIT files this is different from the activity summary.
- "sessions": a [pandas.DataFrames](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with summaries of each lap.

```python
import sweat


example_fit = sweat.examples(path="4078723797.fit")

data = sweat.read_fit(example_fit.path, summaries=True)

data["sessions"]
-> pd.DataFrame
```

### Metadata
The `read_fit()` function accepts a `metadata=True` parameter.
When set to `True` (default is `False`) a dictionairy is returned, with the dataframe in the "data" key, and in the key "devices" a list of all the devices found in the FIT file.

```python
import sweat


example_fit = sweat.examples(path="4078723797.fit")

data = sweat.read_fit(example_fit.path, metadata=True)

data["devices"]
-> list
```

### Raw FIT messages
The `read_fit()` function accepts a `raw_messages=True` parameter.
When set to `True` (default is `False`) a dictionairy is returned, with the dataframe in the "data" key, and in the key "raw_messages" a list of dictionairies that contains all the raw FIT messages.

```python
import sweat


example_fit = sweat.examples(path="4078723797.fit")

data = sweat.read_fit(example_fit.path, raw_messages=True)

data["raw_messages"]
-> list
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

### Metadata
The `read_tcx()` function accepts a `metadata=True` parameter.
When set to `True` (default is `False`) a dictionairy is returned, with the dataframe in the "data" key, and in the key "device" a `Device` object that has the attributes `name`, `product_id`, `serial_number`, `sensors` and `metadata`:

```python
import sweat


data = sweat.read_tcx("path_to.tcx", metadata=True)

data["device"]
-> Device(name='Garmin Edge 1000', product_id='1836', serial_number='3907354759', metadata={'creator_xml': ...}, sensors=[])
```

## Strava
The `sweat.read_strava()` function can be used to pull data from Strava.
Sweat assumes you already have an API access token. Read more about that [here](http://developers.strava.com/docs/authentication/).
If you are looking for a Python library that helps you with Strava API authentication, take a look at [stravalib](https://github.com/hozn/stravalib/) or [stravaio](https://github.com/sladkovm/stravaio).
`read_strava()` returns a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with column names matching *Sweatpy* [nomenclature](nomenclature.md).


Usage:
```python
import sweat

data = sweat.read_strava(activity_id=1234567890, access_token="some access token")
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
