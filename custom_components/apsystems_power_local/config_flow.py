
from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, DEFAULT_NAME
import ipaddress

class APSystemsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                ipaddress.ip_address(user_input["ip_address"])
                return self.async_create_entry(title=DEFAULT_NAME, data=user_input)
            except ValueError:
                errors["base"] = "invalid_ip"

        fields = {
            vol.Required("ip_address", default='ECU IP Address'): str,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(fields),
            errors=errors,
            
        )
