# Data loading

*Sweatpy* has built-in support for loading these activity file formats:

- [FIT files](#fit-files)
- [GPX files](#gpx-files)
- [TCX files](#tcx-files)

## FIT files
The `read_fit()` function accepts strings, [pathlib](https://docs.python.org/3/library/pathlib.html) objects and other file-like objects and returns a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with column names matching *Sweatpy* [nomenclature](nomenclature.md).

Usage:
```python
import sweat

data = sweat.read_fit('path/to/file.fit')
```

Example:
```python
import sweat

example_fit = sweat.examples(path='4078723797.fit')

data = sweat.read_fit(example_fit.path)
```

## GPX files
The `read_gpx()` function accepts strings, [pathlib](https://docs.python.org/3/library/pathlib.html) objects and other file-like objects and returns a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with column names matching *Sweatpy* [nomenclature](nomenclature.md).

Usage:
```python
import sweat

data = sweat.read_gpx('path/to/file.gpx')
```

Example:
```python
import sweat

example_gpx = sweat.examples(path='4078723797_strava.gpx')

data = sweat.read_gpx(example_gpx.path)
```

## TCX files
The `read_tcx()` function accepts strings, [pathlib](https://docs.python.org/3/library/pathlib.html) objects and other file-like objects and returns a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with column names matching *Sweatpy* [nomenclature](nomenclature.md).

Usage:
```python
import sweat

data = sweat.read_gpx('path/to/file.gpx')
```

Example:
```python
import sweat

example_tcx = sweat.examples(path='3173437224.tcx'

data = sweat.read_tcx(example_tcx.path)
```
