from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .options_flow import APSystemsOptionsFlowHandler
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Properly unload platform when integration is removed
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    
async def async_get_options_flow(config_entry):
    return APSystemsOptionsFlowHandler(config_entry)
