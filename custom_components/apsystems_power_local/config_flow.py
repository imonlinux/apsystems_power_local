from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
import ipaddress

from .const import DOMAIN, DEFAULT_NAME, CONF_IP_ADDRESS
from .options_flow import APSystemsOptionsFlow


class APSystemsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                ipaddress.ip_address(user_input[CONF_IP_ADDRESS])

                # If we get here, IP is valid – create the entry
                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data=user_input,
                )
            except ValueError:
                errors[CONF_IP_ADDRESS] = "invalid_ip"

        fields = {
            vol.Required(CONF_IP_ADDRESS, default=""): str,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(fields),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Return the options flow handler."""
        return APSystemsOptionsFlow(config_entry)
