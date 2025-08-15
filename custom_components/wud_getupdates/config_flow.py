import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

class WUDMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for WUD Monitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("container_api_url"): str,
                    vol.Required("instance_name"): str  # Request instance name
                })
            )

        # Save host, port, and instance name
        return self.async_create_entry(
            title=user_input["instance_name"],
            data={
                "host": user_input["container_api_url"],
                "instance_name": user_input["instance_name"]
            }
        )
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return WUDMonitorOptionsFlowHandler(config_entry)

class WUDMonitorOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({
                    vol.Optional("container_api_url", default=self.config_entry.data.get("container_api_url")): str,
                    vol.Optional("instance_name", default=self.config_entry.data.get("instance_name")): str,
                })
            )

        self.hass.config_entries.async_update_entry(
            self.config_entry, data=user_input
        )
        return self.async_create_entry(title="", data={})
