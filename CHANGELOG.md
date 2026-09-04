# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- `Date.to_jdn()` and `Date.from_jdn()`, converting to and from Julian Day
  Numbers.
- Support for years before 1. Dates now use astronomical year numbering,
  where 1 AD is 1, 1 BC is 0, 2 BC is -1, and so on, back to year -4720.

### Changed
- `Date.is_leap_year()` now takes the year that holds the extra day, rather
  than the year after it. Asking whether 2011 has a sixth day in month 13
  was `is_leap_year(2012)` and is now `is_leap_year(2011)`.
- `Date.to_gregorian()` raises `ValueError` for dates outside the range
  `datetime.date` can represent, instead of failing inside the standard
  library.
- `Date.isoformat()` pads years before 1 to four digits, so year -1 is
  `-0001-01-01` rather than `-001-01-01`.

### Fixed
- `from abyssinica.calendar import Date` works again. Splitting `calendar.py`
  into a package left it raising `ImportError`.
- The `abyssinica.calendar` package is included in the distribution again.

### Removed
- `Date.toordinal()` and `Date.fromordinal()`. They were plumbing for the
  old `to_gregorian()`, which reached a `datetime.date` by adding a fixed
  number of days to them. Julian Day Numbers do that job now. The names
  also clashed with `datetime.date.toordinal()`, which counts from a
  different day and so returns a different number for the same date.
  Use `to_jdn()` and `from_jdn()` instead.

## [2.0.0] - 2024-01-01
### Added
- `Date`, converting between Ethiopic and Gregorian dates.

### Changed
- *None*

### Removed
- *None*

## [1.0.0] - 2021-12-16
### Added
- `geez_to_arabic()`
- `arabic_to_geez()`
- `romanize()`

### Changed
- *None*

### Removed
- *None*
