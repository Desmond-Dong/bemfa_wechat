from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class BluetoothSpeakerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Bluetooth Speaker integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the user input (e.g., MAC address format)
            mac_address = user_input["mac_address"]
            if self._is_valid_mac(mac_address):
                # Save the configuration
                return self.async_create_entry(title=user_input["name"], data=user_input)
            else:
                errors["mac_address"] = "invalid_mac"

        # Define the input schema for the form
        data_schema = vol.Schema({
            vol.Required("name", default="Bluetooth Speaker"): str,
            vol.Required("mac_address"): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    def _is_valid_mac(self, mac):
        """Validate MAC address format."""
        import re
        return re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac) is not None
