"""Generic GeoJSON feed."""
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from aio_geojson_client.feed import GeoJsonFeed
from aiohttp import ClientSession
from geojson import FeatureCollection

from .feed_entry import GenericFeedEntry

_LOGGER = logging.getLogger(__name__)


class GenericFeed(GeoJsonFeed[GenericFeedEntry]):
    """Generic GeoJSON feed."""

    def __init__(
        self,
        websession: ClientSession,
        home_coordinates: Tuple[float, float],
        url: str,
        filter_radius: float = None,
    ):
        """Initialise this service."""
        super().__init__(websession, home_coordinates, url, filter_radius=filter_radius)

    def __repr__(self):
        """Return string representation of this feed."""
        return "<{}(home={}, url={}, radius={})>".format(
            self.__class__.__name__,
            self._home_coordinates,
            self._url,
            self._filter_radius,
        )

    def _new_entry(
        self, home_coordinates: Tuple[float, float], feature, global_data: Dict
    ) -> GenericFeedEntry:
        """Generate a new entry."""
        return GenericFeedEntry(home_coordinates, feature)

    def _extract_last_timestamp(
        self, feed_entries: List[GenericFeedEntry]
    ) -> Optional[datetime]:
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates = sorted(
                filter(None, [entry.publication_date for entry in feed_entries]),
                reverse=True,
            )
            return dates[0]
        return None

    def _extract_from_feed(self, feed: FeatureCollection) -> Optional[Dict]:
        """Extract global metadata from feed."""
        return None
