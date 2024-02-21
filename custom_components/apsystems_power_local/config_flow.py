
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN  # Ensure this is defined in your const.py
import requests  # Used for validating the IP address by making a request

class APSystemsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Attempt to validate the IP address by accessing the APSystems webpage
            valid = await self.hass.async_add_executor_job(self._validate_ip, user_input["ip_address"])
            if valid:
                # Optionally, provide a link for manual verification by the user
                self.hass.components.persistent_notification.create(
                    f"Please verify the APSystems ECU by visiting http://{user_input['ip_address']}.",
                    title="Verify APSystems ECU",
                )
                return self.async_create_entry(title="APSystems ECU", data=user_input)
            else:
                errors["base"] = "invalid_ip"

        return self.async_show_form(
            step_id="user", 
            data_schema=vol.Schema({
                vol.Required("ip_address"): str
            }), 
            errors=errors
        )

    def _validate_ip(self, ip_address):
        try:
            response = requests.get(f"http://{ip_address}", timeout=5)
            # Consider the IP valid if the request succeeds
            return response.status_code == 200
        except requests.RequestException:
            return False
