from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_SCAN_INTERVAL

class OpenWrtConfigFlow(config_entries.ConfigFlow, domain="openwrt"):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=self._get_data_schema())

        # Process the input
        return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

    def _get_data_schema(self):
        from homeassistant.helpers import config_entry_flow
        from homeassistant.helpers import schema

        return schema.Schema({
            schema.Required(CONF_HOST): str,
            schema.Required(CONF_USERNAME): str,
            schema.Required(CONF_PASSWORD): str,
            schema.Optional(CONF_SCAN_INTERVAL, default=60): int,  # Adding scan interval with a default value
        })
