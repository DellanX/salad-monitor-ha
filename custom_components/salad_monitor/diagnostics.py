from homeassistant.components.diagnostics import async_redact_data


async def async_get_device_diagnostics(hass, entry):
    coordinator = hass.data["salad_monitor"][entry.entry_id]
    return coordinator.data
