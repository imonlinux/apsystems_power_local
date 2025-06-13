from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_PAUSE_AT_NIGHT

class APSystemsOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        pause_at_night = options.get(
            CONF_PAUSE_AT_NIGHT, 
            self.config_entry.data.get(CONF_PAUSE_AT_NIGHT, False)
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(CONF_PAUSE_AT_NIGHT, default=pause_at_night): bool,
            }),
        )
