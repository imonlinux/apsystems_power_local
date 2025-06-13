import logging
from datetime import timedelta, datetime
import voluptuous as vol

from homeassistant.core import HomeAssistant, callback
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
from homeassistant.util import dt as dt_util
from homeassistant.helpers.event import async_track_point_in_time

from .const import DOMAIN, CONF_PAUSE_AT_NIGHT

from bs4 import BeautifulSoup
import aiohttp

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    ip_address = entry.data["ip_address"]
    pause_at_night = entry.options.get(CONF_PAUSE_AT_NIGHT, entry.data.get(CONF_PAUSE_AT_NIGHT, False))
    coordinator = APSystemsDataUpdateCoordinator(hass, ip_address, pause_at_night)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([APSystemsPowerSensor(coordinator)])

class APSystemsDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, ip_address, pause_at_night):
        super().__init__(
            hass,
            _LOGGER,
            name="APSystems Power Local",
            update_interval=SCAN_INTERVAL,
        )
        self.url = f"http://{ip_address}/index.php/realtimedata/power_graph"
        self.pause_at_night = pause_at_night
        self._last_value = None

    async def _async_update_data(self):
        if self.pause_at_night and not self._is_sun_up():
            # If the sun is down, skip polling and schedule a refresh at sunrise
            self._schedule_refresh_at_sunrise()
            _LOGGER.info("Polling is paused until sunrise. Returning last known value.")
            if self._last_value is not None:
                return self._last_value
            raise UpdateFailed("Polling paused at night, and no data available yet.")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, timeout=10) as response:
                    text = await response.text()
                    soup = BeautifulSoup(text, "html.parser")
                    span = soup.find("span", id="total")
                    if span and "kWh" in span.text:
                        parts = span.text.split(":")
                        if len(parts) == 2 and "kWh" in parts[1]:
                            value = parts[1].split("kWh")[0].strip()
                            value_float = float(value)
                            self._last_value = value_float
                            return value_float
                    raise UpdateFailed("Could not parse solar energy value from page")
        except Exception as err:
            raise UpdateFailed(f"Error updating data: {err}")

    def _is_sun_up(self):
        sun = self.hass.states.get("sun.sun")
        if not sun or not sun.attributes:
            return True  # Fallback: always poll if we don't know
        # Between next_setting and next_rising = night
        now = dt_util.utcnow()
        next_rising = sun.attributes.get("next_rising")
        next_setting = sun.attributes.get("next_setting")
        state = sun.state  # 'above_horizon' or 'below_horizon'
        if state == "above_horizon":
            return True
        if next_rising and next_setting:
            try:
                rising = dt_util.parse_datetime(next_rising)
                setting = dt_util.parse_datetime(next_setting)
                # It's night if now is after setting and before rising
                if setting < now < rising:
                    return False
            except Exception as e:
                _LOGGER.debug("Failed sun parsing: %s", e)
        return False

    def _schedule_refresh_at_sunrise(self):
        """Schedule an immediate refresh at next sunrise if not already scheduled."""
        if hasattr(self, "_refresh_scheduled") and self._refresh_scheduled:
            return  # Already scheduled
        sun = self.hass.states.get("sun.sun")
        if not sun or not sun.attributes:
            return
        next_rising = sun.attributes.get("next_rising")
        if not next_rising:
            return
        when = dt_util.parse_datetime(next_rising)
        if not when:
            return
        @callback
        def _refresh_callback(_):
            self._refresh_scheduled = False
            self.async_set_updated_data(None)
        async_track_point_in_time(self.hass, _refresh_callback, when)
        self._refresh_scheduled = True

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
