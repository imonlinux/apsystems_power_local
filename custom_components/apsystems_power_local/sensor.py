import logging
import re
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity,
    UpdateFailed,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy

from .const import (
    DOMAIN,
    CONF_IP_ADDRESS,
    CONF_SUSPEND_AFTER_SUNSET,
    DEFAULT_SUSPEND_AFTER_SUNSET,
)

from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up APSystems Power Local sensor from a config entry."""
    ip_address = entry.data[CONF_IP_ADDRESS]
    suspend_after_sunset = entry.options.get(
        CONF_SUSPEND_AFTER_SUNSET, DEFAULT_SUSPEND_AFTER_SUNSET
    )

    coordinator = APSystemsDataUpdateCoordinator(
        hass,
        ip_address=ip_address,
        suspend_after_sunset=suspend_after_sunset,
    )

    await coordinator.async_config_entry_first_refresh()
    async_add_entities([APSystemsPowerSensor(coordinator)])


class APSystemsDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from the APSystems ECU page."""

    def __init__(
        self,
        hass: HomeAssistant,
        ip_address: str,
        suspend_after_sunset: bool,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="APSystems Power Local",
            update_interval=SCAN_INTERVAL,
        )

        self.hass = hass
        self.ip_address = ip_address
        self.url = f"http://{ip_address}/index.php/realtimedata/power_graph"
        self._session = async_get_clientsession(hass)
        self._suspend_after_sunset = suspend_after_sunset

    def _should_suspend_polling(self) -> bool:
        """Return True if we should skip HTTP polling due to sunset."""
        if not self._suspend_after_sunset:
            return False

        sun_state = self.hass.states.get("sun.sun")
        if not sun_state:
            # If sun entity is missing, don't try to be clever – just keep polling.
            return False

        # In modern HA, the state is just the string "below_horizon"
        return sun_state.state == "below_horizon"

    async def _async_update_data(self):
        """Fetch updated data from the ECU."""
        try:
            # Optionally skip polling at night
            if self._should_suspend_polling():
                if self.data is not None:
                    _LOGGER.debug(
                        "Sun is below horizon and suspend_after_sunset is enabled; "
                        "reusing previous value: %s",
                        self.data,
                    )
                    return self.data

                _LOGGER.debug(
                    "Sun is below horizon and suspend_after_sunset is enabled; "
                    "no previous value available, returning 0.0",
                )
                return 0.0

            async with self._session.get(self.url, timeout=10) as response:
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                span = soup.find("span", id="total")

                if not span or not span.text:
                    raise UpdateFailed("Could not find solar total span on page")

                # Extract the numeric value before "kWh", e.g. "Solar Generated Today: 25.16 kWh"
                match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*kWh", span.text)
                if not match:
                    raise UpdateFailed(
                        f"Could not parse kWh value from total span text: {span.text!r}"
                    )

                return float(match.group(1))

        except Exception as err:
            _LOGGER.error("Error fetching APSystems Power data: %s", err)
            raise UpdateFailed(f"Error updating data: {err}") from err


class APSystemsPowerSensor(CoordinatorEntity, SensorEntity):
    """Sensor representing today's solar energy from APSystems ECU."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_name = "APSystems Power"  # Entity name

    def __init__(self, coordinator: APSystemsDataUpdateCoordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "apsystems_power"
        self._attr_extra_state_attributes = {}

    @property
    def native_value(self):
        """Return the current energy value in kWh."""
        return self.coordinator.data

    @property
    def device_info(self):
        """Return device info for the ECU."""
        return {
            "identifiers": {(DOMAIN, "apsystems_ecu")},
            "name": "APSystems ECU",
            "manufacturer": "APSystems",
            "model": "ECU",
            "configuration_url": f"http://{self.coordinator.ip_address}/",
        }
