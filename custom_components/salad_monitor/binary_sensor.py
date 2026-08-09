from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, MANUFACTURER, MODEL

BINARY_SENSOR_DESCRIPTORS = (
    ("salad_active", "Salad GPU Active"),
    ("gpu_reserved", "Salad GPU Reserved"),
    ("salad_pending", "Salad Workload Pending"),
    ("is_downloading", "Salad Downloading"),
    ("bandwidth_active", "Salad Bandwidth Active"),
    ("miner_active", "Salad Miner Active"),
)


def _state_value(coordinator, key):
    return coordinator.data.get("state", {}).get(key)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        SaladBinarySensor(coordinator, entry, key, name)
        for key, name in BINARY_SENSOR_DESCRIPTORS
    ])


class SaladBinarySensor(CoordinatorEntity, BinarySensorEntity):
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
    def is_on(self):
        return bool(_state_value(self.coordinator, self._key))

    @property
    def available(self):
        return self.coordinator.last_update_success
