# Changes

## 0.4 (11/01/2024)
* Bumped version of upstream aio_geojson_client library to 0.20.
* Improved JSON parsing error handling, especially when not using Python's built-in JSON parsing library.
* Code quality improvements.
* Added Python 3.12 support.
* Bumped library versions: black, flake8, isort.
* Migrated to pytest.

## 0.3 (30/01/2023)
* Restrict geojson dependency to smaller than version 3, to avoid a conflicting 
  dependency with pyowm in Home Assistant.

## 0.2 (30/01/2023)
* Added Python 3.11 support.
* Removed deprecated asynctest dependency.
* Small code quality enhancements.
* Bumped version of upstream aio_geojson_client library to 0.18.
* Bumped dependencies: geojson.

## 0.1 (14/03/2022)
* Initial release with support for generic GeoJSON feeds.
* Calculating distance to home coordinates.
* Support for filtering by distance for all feeds.
* Supporting all the features available in non-async library 
  ([python-geojson-client](https://github.com/exxamalte/python-geojson-client)).
