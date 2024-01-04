import requests
import re
from datetime import timedelta
from homeassistant.util import Throttle
from homeassistant.components.sensor import (
    SensorEntity, 
    SensorDeviceClass,
    SensorStateClass
)
from homeassistant.const import UnitOfEnergy

# Define the minimum time interval between updates
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)

def scrape_solar_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Use regular expression to find the solar energy data
        match = re.search(r"Solar Generated Today: (\d+\.\d+) kWh", response.text)
        if match:
            return float(match.group(1))
    except Exception as e:
        return None

class APSystemsSensor(SensorEntity):
    def __init__(self, ip_address):
        self._state = None
        self._ip_address = ip_address
        self._name = "APSystems Power"

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f"apsystems_power_{self._ip_address}"

    @property
    def device_class(self):
        return SensorDeviceClass.ENERGY

    @property
    def state_class(self):
        return SensorStateClass.TOTAL_INCREASING

    @property
    def unit_of_measurement(self):
        return UnitOfEnergy.KILO_WATT_HOUR

    @property
    def state(self):
        return self._state

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        url = f"http://{self._ip_address}/index.php/realtimedata/power_graph"
        self._state = await self.hass.async_add_executor_job(scrape_solar_data, url)

def setup_platform(hass, config, async_add_entities, discovery_info=None):
    ip_address = config.get('ip_address')
    async_add_entities([APSystemsSensor(ip_address)], True)
