from __future__ import annotations

import asyncio
import aiohttp
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from homeassistant.core import HomeAssistant
from .const import DEFAULT_SCAN_INTERVAL, HEALTH_ENDPOINTS


class SaladCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, host: str, port: int):
        self.host = host
        self.port = port
        self._health_endpoint = None
        logger = logging.getLogger(__name__)

        super().__init__(
            hass,
            logger=logger,
            name="Salad Monitor",
            update_interval=DEFAULT_SCAN_INTERVAL,
        )

    async def _async_fetch_health(self, session, endpoint):
        url = f"http://{self.host}:{self.port}{endpoint}"
        async with session.get(url, timeout=5) as resp:
            if resp.status != 200:
                raise UpdateFailed(f"HTTP {resp.status} from {endpoint}")
            payload = await resp.json()
            if not isinstance(payload, dict):
                raise UpdateFailed(f"Unexpected payload from {endpoint}")
            return payload

    async def _async_update_data(self):
        endpoints = []
        if self._health_endpoint:
            endpoints.append(self._health_endpoint)
        endpoints.extend(
            endpoint for endpoint in HEALTH_ENDPOINTS if endpoint not in endpoints
        )

        async with aiohttp.ClientSession() as session:
            errors = []
            for endpoint in endpoints:
                try:
                    payload = await self._async_fetch_health(session, endpoint)
                    self._health_endpoint = endpoint
                    return payload
                except (aiohttp.ClientError, asyncio.TimeoutError, ValueError, UpdateFailed) as err:
                    errors.append(f"{endpoint}: {err}")

            raise UpdateFailed(
                "Error fetching health from known endpoints: " + "; ".join(errors)
            )
