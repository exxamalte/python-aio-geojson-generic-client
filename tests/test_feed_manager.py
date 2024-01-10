"""Test for the generic GeoJSON feed manager."""
import asyncio
import datetime
from http import HTTPStatus

import aiohttp
import pytest

from aio_geojson_generic_client.feed_manager import GenericFeedManager
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_feed_manager(mock_aioresponse):
    """Test the feed manager."""
    home_coordinates = (-31.0, 151.0)
    mock_aioresponse.get(
        "https://www.rfs.nsw.gov.au/feeds/majorIncidents.json",
        status=HTTPStatus.OK,
        body=load_fixture("feed-1.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []

        async def _generate_entity(external_id):
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        async def _update_entity(external_id):
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        async def _remove_entity(external_id):
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        feed_manager = GenericFeedManager(
            websession,
            _generate_entity,
            _update_entity,
            _remove_entity,
            home_coordinates,
            "https://www.rfs.nsw.gov.au/feeds/majorIncidents.json",
        )
        assert (
            repr(feed_manager) == "<GenericFeedManager("
            "feed=<GenericFeed("
            "home=(-31.0, 151.0), url=https://"
            "www.rfs.nsw.gov.au"
            "/feeds/majorIncidents.json, "
            "radius=None)>)>"
        )
        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 4
        assert feed_manager.last_timestamp == datetime.datetime(
            2018, 9, 21, 6, 40, tzinfo=datetime.UTC
        )
        assert len(generated_entity_external_ids) == 4
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0
