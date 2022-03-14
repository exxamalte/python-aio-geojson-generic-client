"""Test for the generic GeoJSON feed."""
import datetime

import aiohttp
import pytest
from aio_geojson_client.consts import UPDATE_OK

from aio_geojson_generic_client.feed import GenericFeed
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_update_ok(aresponses, event_loop):
    """Test updating feed is ok."""
    home_coordinates = (-31.0, 151.0)
    aresponses.add(
        "www.rfs.nsw.gov.au",
        "/feeds/majorIncidents.json",
        "get",
        aresponses.Response(text=load_fixture("feed-1.json"), status=200),
        match_querystring=True,
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = GenericFeed(
            websession,
            home_coordinates,
            "https://www.rfs.nsw.gov.au/feeds/majorIncidents.json",
        )
        assert (
            repr(feed) == "<GenericFeed("
            "home=(-31.0, 151.0), "
            "url=https://www.rfs.nsw.gov.au"
            "/feeds/majorIncidents.json, "
            "radius=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 4

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (-37.2345, 149.1234)
        assert round(abs(feed_entry.distance_to_home - 714.4), 1) == 0
        assert repr(feed_entry) == "<GenericFeedEntry(id=1234)>"
        assert feed_entry.publication_date == datetime.datetime(
            2018, 9, 21, 6, 30, tzinfo=datetime.timezone.utc
        )
        assert feed_entry.properties == {
            "title": "Title 1",
            "category": "Category 1",
            "guid": "1234",
            "pubDate": "21/09/2018 6:30:00 AM",
            "description": "ALERT LEVEL: Alert Level 1 <br />LOCATION: Location 1 <br />COUNCIL AREA: Council 1 <br />STATUS: Status 1 <br />TYPE: Type 1 <br />FIRE: Yes <br />SIZE: 10 ha <br />RESPONSIBLE AGENCY: Agency 1 <br />UPDATED: 21 Sep 2018 16:45",
        }

        feed_entry = entries[1]
        assert feed_entry is not None
        assert feed_entry.title == "Title 2"
        assert feed_entry.external_id == "Title 2"

        feed_entry = entries[2]
        assert feed_entry.external_id == hash((-37.2345, 149.1234))

        feed_entry = entries[3]
        assert feed_entry.title == "Badja Forest Rd, Countegany"
        assert feed_entry.geometries is not None
        assert len(feed_entry.geometries) == 4
        assert round(abs(feed_entry.distance_to_home - 578.5), 1) == 0


@pytest.mark.asyncio
async def test_empty_feed(aresponses, event_loop):
    """Test updating feed is ok when feed does not contain any entries."""
    home_coordinates = (-41.2, 174.7)
    aresponses.add(
        "www.rfs.nsw.gov.au",
        "/feeds/majorIncidents.json",
        "get",
        aresponses.Response(text=load_fixture("feed-2.json"), status=200),
        match_querystring=True,
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = GenericFeed(
            websession,
            home_coordinates,
            "https://www.rfs.nsw.gov.au/feeds/majorIncidents.json",
        )
        assert (
            repr(feed) == "<GenericFeed("
            "home=(-41.2, 174.7), "
            "url=https://www.rfs.nsw.gov.au"
            "/feeds/majorIncidents.json, "
            "radius=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 0
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_feed_entry_properties(aresponses, event_loop):
    """Test updating feed is ok with focus on properties."""
    home_coordinates = (-41.2, 174.7)
    aresponses.add(
        "www.rfs.nsw.gov.au",
        "/feeds/majorIncidents.json",
        "get",
        aresponses.Response(text=load_fixture("feed-3.json"), status=200),
        match_querystring=True,
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = GenericFeed(
            websession,
            home_coordinates,
            "https://www.rfs.nsw.gov.au/feeds/majorIncidents.json",
        )
        assert (
            repr(feed) == "<GenericFeed("
            "home=(-41.2, 174.7), "
            "url=https://www.rfs.nsw.gov.au"
            "/feeds/majorIncidents.json, "
            "radius=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 3

        feed_entry = entries[0]
        assert feed_entry.properties == {
            "property1": "value1",
            "property2": "value2",
        }

        feed_entry = entries[1]
        assert feed_entry.properties is None

        feed_entry = entries[2]
        assert feed_entry.properties is None
