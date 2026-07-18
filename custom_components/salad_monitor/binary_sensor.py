from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, MANUFACTURER, MODEL


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            SaladBinarySensor(coordinator, entry, "salad_active", "Salad GPU Active"),
            SaladBinarySensor(coordinator, entry, "gpu_reserved", "Salad GPU Reserved"),
            SaladBinarySensor(
                coordinator, entry, "salad_pending", "Salad Workload Pending"
            ),
        ]
    )


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
        return bool(self.coordinator.data["state"].get(self._key))

    @property
    def available(self):
        return self.coordinator.last_update_success
