from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, MANUFACTURER, MODEL

SENSOR_DESCRIPTORS = (
    ("last_event", "Salad Last Event"),
    ("current_logfile", "Salad Current Logfile"),
    ("wallet_balance", "Salad Wallet Balance"),
    ("wallet_projected", "Salad Wallet Projected"),
    ("wallet_last_update", "Salad Wallet Last Update"),
    ("job_id", "Salad Job ID"),
    ("job_start_time", "Salad Job Start Time"),
    ("job_uptime_seconds", "Salad Job Uptime Seconds"),
    ("container_status", "Salad Container Status"),
    ("matrix_status", "Salad Matrix Status"),
    ("download_progress_pct", "Salad Download Progress %"),
    ("download_active_layer", "Salad Download Active Layer"),
    ("download_layer_progress", "Salad Download Layer Progress"),
    ("download_speed_kbps", "Salad Download Speed KB/s"),
    ("download_total_mb", "Salad Download Total MB"),
    ("download_estimated_mb", "Salad Download Estimated MB"),
    ("download_eta_seconds", "Salad Download ETA Seconds"),
    ("wsl_status", "Salad WSL Status"),
    ("wsl_ram_mb", "Salad WSL RAM MB"),
    ("wsl_disk_size_gb", "Salad WSL Disk Size GB"),
    ("bandwidth_node_name", "Salad Bandwidth Node Name"),
    ("vnet_rx_kbps", "Salad VNET RX KB/s"),
    ("vnet_tx_kbps", "Salad VNET TX KB/s"),
    ("vnet_total_rx_gb", "Salad VNET Total RX GB"),
    ("vnet_total_tx_gb", "Salad VNET Total TX GB"),
    ("sgs_rx_kbps", "Salad SGS RX KB/s"),
    ("sgs_tx_kbps", "Salad SGS TX KB/s"),
    ("sgs_total_rx_mb", "Salad SGS Total RX MB"),
    ("sgs_total_tx_mb", "Salad SGS Total TX MB"),
    ("sgs_ram_mb", "Salad SGS RAM MB"),
    ("cpu_name", "Salad CPU Name"),
    ("cpu_load_pct", "Salad CPU Load %"),
    ("ram_used_gb", "Salad RAM Used GB"),
    ("ram_total_gb", "Salad RAM Total GB"),
    ("ram_load_pct", "Salad RAM Load %"),
    ("gpu_name", "Salad GPU Name"),
    ("gpu_utilization_pct", "Salad GPU Utilization %"),
    ("gpu_power_watts", "Salad GPU Power Watts"),
    ("gpu_temperature_c", "Salad GPU Temperature C"),
    ("disk_type", "Salad Disk Type"),
    ("disk_size_gb", "Salad Disk Size GB"),
    ("disk_utilization_pct", "Salad Disk Utilization %"),
    ("disk_read_mbps", "Salad Disk Read MB/s"),
    ("disk_write_mbps", "Salad Disk Write MB/s"),
    ("gpu_demand_tier", "Salad GPU Demand Tier"),
    ("gpu_demand_utilization_pct", "Salad GPU Demand Utilization %"),
    ("gpu_earning_avg_24h", "Salad GPU Earning Avg 24h"),
    ("gpu_earning_max_24h", "Salad GPU Earning Max 24h"),
    ("gpu_recommended_ram_gb", "Salad GPU Recommended RAM GB"),
    ("gpu_demand_last_update", "Salad GPU Demand Last Update"),
    ("salad_version", "Salad App Version"),
    ("salad_uptime_seconds", "Salad App Uptime Seconds"),
    ("salad_bowl_version", "Salad Bowl Version"),
    ("salad_bowl_uptime_seconds", "Salad Bowl Uptime Seconds"),
    ("miner_name", "Salad Miner Name"),
    ("last_warning", "Salad Last Warning"),
    ("last_warning_time", "Salad Last Warning Time"),
)


def _state_value(coordinator, key):
    return coordinator.data.get("state", {}).get(key)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [SaladSensor(coordinator, entry, key, name) for key, name in SENSOR_DESCRIPTORS]
        + [SaladVersionSensor(coordinator, entry)]
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
        return _state_value(self.coordinator, self._key)

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
