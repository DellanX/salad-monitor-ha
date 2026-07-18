from __future__ import annotations

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, DEFAULT_PORT

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Optional("port", default=DEFAULT_PORT): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict):
    """Validate the user input by calling /health."""
    host = data["host"]
    port = data["port"]

    url = f"http://{host}:{port}/health"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status != 200:
                    raise CannotConnect
                payload = await resp.json()
        except Exception as err:
            raise CannotConnect from err

    return {
        "title": f"Salad Monitor ({host}:{port})",
        "version": payload.get("version", "unknown"),
    }


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
