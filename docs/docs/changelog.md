# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The same types of changes should be grouped.
Types of changes:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [0.21.0] - 2021-04-22
### Added
- Adds testing for Python 3.10
- `read_tcx()` now supports a metadata=True kwarg that will return device data.

## [0.20.3] - 2021-04-20
### Fixed
- `sweat.read_fit()` now supports integer column names.

## [0.20.2] - 2021-04-16
### Fixed
- `read_fit()` now handles summary data correctly when there is no data

## [0.20.1] - 2021-04-16
### Fixed
- Fixed issue when `pool_lengths=True` but there are no pool length records in the FIT file.

## [0.20.0] - 2021-04-15
### Added
- `read_fit() now returns pool length records when the `pool_lenghts=True` argument is passed.
- `read_fit()` now return raw FIT messages when a `raw_message=True` argument is passed.
- `read_fit()` can now return metadata and device information.

## [0.19.0] - 2021-04-06
### Added
- Adds matplotlib dependency.
- Extends `sweat.read_fit()` with support for multi session FIT files, hrv data, metadata (summaries and devices), error handling and much more...
- Properly handles left-right balance from FIT files.
- Adds Garmin FIT Profile based on the Garmin FIT SDK 21.47.

### Fixed
- Removes unnecessary numpy import in pdm docs.

## [0.18.1] - 2021-03-12
### Fixed
- Fixes the index of mean max calculations as they were of by 1 second. First index is now 00:00:01 instead of 00:00:00.

## [0.18.0] - 2021-03-12
### Added
- Adds `monotonic` argument to `sweat.mean_max()` to enforce a monotonically decreasing mean max curve. Usage: `power.sweat.mean_max(monotonic=True)`. Defaults to False.

## [0.17.1] - 2021-03-09
### Fixed
- Numerical columns are now converted to numeric dtypes for gpx files.

## [0.17.0] - 2020-12-31
### Fixed
- Fixes error when loading FIT file without location data.

### Changed
- Removes "forward fill" when resampling dataframes. Users can manually get the old behavior back by running `df = df.ffill()`.

## [0.16.1] - 2020-11-19
### Fixed
- Fixes publishing docs by updating mknotebooks version >0.6.0

## [0.16.0] - 2020-11-19
## Added
- Adds support for Python 3.9

### Fixed
- Latitude and longitude from FIT files are now converted from semicircles to degrees.

## [0.15.0] - 2020-06-14
### Added
- Adds exponential power duration model.
- Adds omni power duration model

### Changed
- Renames CriticalPowerRegressor to PowerDurationRegressor

## [0.14.0] - 2020-06-09
### Added
- Adds sweat accessor to pandas series and data frames.
- Add to_timedelta_index() and mean_max() to accessors.
- Adds calculate_zones() and time_in_zone() to series accessor.

## [0.13.0] - 2020-06-05
### Added
- Rewrite of Strava implemention, now features a single read_strava() function.

### Removed
- Old Strava functionality is removed in favor of a new read_strava() function.

## [0.12.0] - 2020-06-05
### Added
- Added the CriticalPowerRegressor
- Some refactoring and documentation for W'balance functionality.

### Removed
- Removed the old critical power curve fitting functionality
- Removed WorkoutDataFrame model because it is not maintained.
- Removed Athlete model because it is not maintained.
- Removed GoldenCheetahClient because it is not maintained. Will be re-implemented later.

## [0.11.0] - 2020-06-04
### Added
- Adds lap and session data for FIT files
- Adds lap data for TCX files

## [0.10.0] - 2020-06-01
### Added
- Usage examples on docs home page
- Nomenclature for data frames
- Adds ability to resample and interpolate data frames

### Changed
- Changes the index of returned data frames to a pandas.DateTimeIndex

## [0.9.0] - 2020-05-23
### Added
- Added generic read_file function
- Added generic read_dir function

## [0.8.0] - 2020-04-26
### Added
- Added reading TCX files.

## [0.7.0] - 2020-04-21
### Added
- Added reading GPX files.

## [0.6.0] - 2020-04-21
### Added
- Added example data framework

### Changed
- Refactored reading FIT files to pandas-like interface: read_fit()

## [0.5.0] - 2020-17-04
### Added
- Python 3.8 support.
- Tests are now run in docker.
- Implements Poetry for packaging and dependencies.
- Adds Github Actions for tests and publishing.
- Updates copyright year in LICENSE.
- Adds CONTRIBUTING.md.
- Adds Jupyter notebook functionality for docs.
