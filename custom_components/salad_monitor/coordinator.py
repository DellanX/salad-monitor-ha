from __future__ import annotations

import aiohttp
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from homeassistant.core import HomeAssistant
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL


class SaladCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, host: str, port: int):
        self.host = host
        self.port = port
        logger = logging.getLogger(__name__)

        super().__init__(
            hass,
            logger=logger,
            name="Salad Monitor",
            update_interval=DEFAULT_SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        url = f"http://{self.host}:{self.port}/health"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=5) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"HTTP {resp.status}")
                    return await resp.json()
            except Exception as err:
                raise UpdateFailed(f"Error fetching health: {err}") from err
