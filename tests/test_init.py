"""Test for the generic GeoJSON feed general setup."""
from aio_geojson_generic_client import __version__


def test_version():
    """Test for version tag."""
    assert __version__ is not None
