import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity,
    UpdateFailed,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy
from .const import DOMAIN

from bs4 import BeautifulSoup
import aiohttp

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    ip_address = entry.data["ip_address"]
    coordinator = APSystemsDataUpdateCoordinator(hass, ip_address)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([APSystemsPowerSensor(coordinator)])

class APSystemsDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, ip_address):
        super().__init__(
            hass,
            _LOGGER,
            name="APSystems Power Local",
            update_interval=SCAN_INTERVAL,
        )
        self.url = f"http://{ip_address}/index.php/realtimedata/power_graph"

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, timeout=10) as response:
                    text = await response.text()
                    # Use BeautifulSoup to find the value in <span id="total">
                    soup = BeautifulSoup(text, "html.parser")
                    span = soup.find("span", id="total")
                    if span and "kWh" in span.text:
                        # Example: "Solar Generated Today: 25.16 kWh"
                        parts = span.text.split(":")
                        if len(parts) == 2 and "kWh" in parts[1]:
                            value = parts[1].split("kWh")[0].strip()
                            return float(value)
                    raise UpdateFailed("Could not parse solar energy value from page")
        except Exception as err:
            raise UpdateFailed(f"Error updating data: {err}")

class APSystemsPowerSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator: APSystemsDataUpdateCoordinator):
        super().__init__(coordinator)
        self._attr_unique_id = "apsystems_solar_generated_today"

    @property
    def name(self):
        return "Solar Generated Today"

    @property
    def native_value(self):
        return self.coordinator.data
