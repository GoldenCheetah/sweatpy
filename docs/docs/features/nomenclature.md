# Nomenclature

One of the main ideas behind Sweatpy is to offer a generic interface to data from different data sources.
A big part of this is making sure that the data frames that are returned by the `sweat.read_*()` methods (`read_fit()`, `read_tcx()`, etc.) are similar.
I.e. it should not matter if you are importing an activity from a .fit file or a .tcx file: Working with the data should be the same.

For the data frames returned by the `read_*()` methods, the column and data types are as follows:

| Column name       | unit | comments |
| ----------------- |:-----|:-----|
| index or datetime | [pandas.DatetimeIndex](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html) | Be aware that not all activity files are sampled at 1Hz |
| heartrate         | beats per minute | |
| speed             | meters/second | |
| power             | Watt | |
| latitude          | degrees | |
| longitude         | degrees | |
| left-right balance | % | |
| cadence           | rounds per minute | |
| distance          | meter | |
| elevation         | meter | |
| temperature       | degrees Celsius | |
