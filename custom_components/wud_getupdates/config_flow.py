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
                    vol.Required("host"): str,
                    # port may be left empty; we'll treat empty string as no port
                    vol.Optional("port", default=""): str,
                    vol.Required("instance_name"): str  # Request instance name
                })
            )

        # Save host, port, and instance name
        return self.async_create_entry(
            title=user_input["instance_name"],
            data={
                "host": user_input["host"],
                "port": user_input.get("port", ""),
                "instance_name": user_input["instance_name"]
            }
        )
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return WUDMonitorOptionsFlowHandler()

class WUDMonitorOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    async def async_step_init(self, user_input=None):
        if user_input is None:
            # convert any existing port value to a string so the schema
            # validator does not complain (older entries may have stored it
            # as an int).
            existing_port = self.config_entry.data.get("port", "")
            if existing_port is None:
                existing_port = ""
            else:
                existing_port = str(existing_port)

            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({
                    vol.Optional("host", default=self.config_entry.data.get("host")): str,
                    vol.Optional("port", default=existing_port): str,
                    vol.Optional("instance_name", default=self.config_entry.data.get("instance_name")): str,
                })
            )

        self.hass.config_entries.async_update_entry(
            self.config_entry,
            data={
                "host": user_input.get("host", self.config_entry.data.get("host")),
                "port": user_input.get("port", self.config_entry.data.get("port", "")),
                "instance_name": user_input.get(
                    "instance_name", self.config_entry.data.get("instance_name")
                ),
            },
        )
        return self.async_create_entry(title="", data={})
