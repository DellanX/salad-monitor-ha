from __future__ import annotations

import asyncio
import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DEFAULT_PORT, DOMAIN, HEALTH_ENDPOINTS

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Optional("port", default=DEFAULT_PORT): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict):
    """Validate the user input by calling known health endpoints."""
    host = data["host"]
    port = data["port"]

    async with aiohttp.ClientSession() as session:
        errors = []
        for endpoint in HEALTH_ENDPOINTS:
            url = f"http://{host}:{port}{endpoint}"
            try:
                async with session.get(url, timeout=5) as resp:
                    if resp.status != 200:
                        errors.append(f"{endpoint}: HTTP {resp.status}")
                        continue
                    payload = await resp.json()
                    if not isinstance(payload, dict):
                        errors.append(f"{endpoint}: unexpected payload")
                        continue
                    return {
                        "title": f"Salad Monitor ({host}:{port})",
                        "version": payload.get("version", "unknown"),
                    }
            except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as err:
                errors.append(f"{endpoint}: {err}")

    raise CannotConnect("; ".join(errors))


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Salad Monitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA_SCHEMA,
                errors={"base": "cannot_connect"},
            )

        await self.async_set_unique_id(f"{user_input['host']}_{user_input['port']}")
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=info["title"],
            data=user_input,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
