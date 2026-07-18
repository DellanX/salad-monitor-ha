from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, MANUFACTURER, MODEL


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            SaladSensor(coordinator, entry, "last_event", "Salad Last Event"),
            SaladSensor(coordinator, entry, "current_logfile", "Salad Current Logfile"),
            SaladVersionSensor(coordinator, entry),
        ]
    )


class SaladSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, key, name):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._entry = entry
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "Salad GPU Monitor",
            "manufacturer": MANUFACTURER,
            "model": MODEL,
            "sw_version": self.coordinator.data.get("version"),
        }

    @property
    def native_value(self):
        return self.coordinator.data["state"].get(self._key)

    @property
    def available(self):
        return self.coordinator.last_update_success


class SaladVersionSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._entry = entry
        self._attr_name = "Salad Monitor Version"
        self._attr_unique_id = f"{entry.entry_id}_version"

    @property
    def native_value(self):
        return self.coordinator.data.get("version")

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "Salad GPU Monitor",
            "manufacturer": MANUFACTURER,
            "model": MODEL,
            "sw_version": self.coordinator.data.get("version"),
        }
