from __future__ import annotations

from typing import Any

from homeassistant import config_entries
import voluptuous as vol

from .const import (
    DOMAIN,
    CONF_SUSPEND_AFTER_SUNSET,
    DEFAULT_SUSPEND_AFTER_SUNSET,
)


class APSystemsOptionsFlow(config_entries.OptionsFlow):
    """Handle APSystems Power Local options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Save options
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SUSPEND_AFTER_SUNSET,
                    default=self.config_entry.options.get(
                        CONF_SUSPEND_AFTER_SUNSET,
                        DEFAULT_SUSPEND_AFTER_SUNSET,
                    ),
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )

