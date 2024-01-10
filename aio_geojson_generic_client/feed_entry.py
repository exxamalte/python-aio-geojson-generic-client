"""Generic GeoJSON feed entry."""
from __future__ import annotations

import calendar
import logging
from datetime import datetime
from time import strptime

import pytz
from aio_geojson_client.feed_entry import FeedEntry
from geojson import Feature

from .consts import ATTR_GUID, ATTR_ID, ATTR_PUB_DATE, ATTR_TITLE

_LOGGER = logging.getLogger(__name__)


class GenericFeedEntry(FeedEntry):
    """Generic GeoJSON feed entry."""

    def __init__(self, home_coordinates: tuple[float, float], feature: Feature):
        """Initialise this service."""
        super().__init__(home_coordinates, feature)

    @property
    def title(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties(ATTR_TITLE)

    @property
    def external_id(self) -> str:
        """Return the external id of this entry."""
        # Find a suitable ID for the provided entry.
        external_id = self._search_in_feature(ATTR_ID)
        if not external_id:
            external_id = self._search_in_properties(ATTR_ID)
        if not external_id:
            external_id = self._search_in_properties(ATTR_GUID)
        if not external_id:
            external_id = self.title
        if not external_id:
            # Use geometry as ID as a fallback.
            external_id = hash(self.coordinates)
        return external_id

    @property
    def publication_date(self) -> datetime:
        """Return the publication date of this entry."""
        publication_date = self._search_in_properties(ATTR_PUB_DATE)
        if publication_date:
            # Parse the date. Example: 15/09/2018 9:31:00 AM
            date_struct = strptime(publication_date, "%d/%m/%Y %I:%M:%S %p")
            publication_date = datetime.fromtimestamp(
                calendar.timegm(date_struct), tz=pytz.utc
            )
        return publication_date

    @property
    def properties(self) -> dict | None:
        """Return all properties found for this entry."""
        if self._feature and self._feature.properties:
            return self._feature.properties
        return None
