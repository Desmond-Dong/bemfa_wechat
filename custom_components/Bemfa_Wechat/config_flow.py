import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class BemfaWeChatConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bemfa WeChat."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Bemfa WeChat", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("uid"): str,
                vol.Required("device", default="DefaultDevice"): str,
                vol.Optional("group", default="default"): str,
                vol.Optional("url", default=""): str,
            })
        )
