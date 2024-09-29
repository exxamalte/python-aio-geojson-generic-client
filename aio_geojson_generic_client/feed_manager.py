"""Feed Manager for Generic GeoJSON feed."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from aio_geojson_client.feed_manager import FeedManagerBase
from aio_geojson_client.status_update import StatusUpdate
from aiohttp import ClientSession

from .feed import GenericFeed


class GenericFeedManager(FeedManagerBase):
    """Feed Manager for Generic GeoJSON feed."""

    def __init__(
        self,
        websession: ClientSession,
        generate_callback: Callable[[str], Awaitable[None]],
        update_callback: Callable[[str], Awaitable[None]],
        remove_callback: Callable[[str], Awaitable[None]],
        coordinates: tuple[float, float],
        url: str,
        filter_radius: float | None = None,
        status_callback: Callable[[StatusUpdate], Awaitable[None]] | None = None,
    ):
        """Initialize the Generic GeoJSON Feed Manager."""
        feed = GenericFeed(
            websession,
            coordinates,
            url,
            filter_radius=filter_radius,
        )
        super().__init__(
            feed,
            generate_callback,
            update_callback,
            remove_callback,
            status_async_callback=status_callback,
        )
