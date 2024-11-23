"""Config flow for Bluetooth Speaker integration."""
import logging
import subprocess
import voluptuous as vol
from typing import Any, Dict

from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.const import CONF_NAME, CONF_DEVICE
import homeassistant.helpers.config_validation as cv
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

_LOGGER = logging.getLogger(__name__)
DOMAIN = "bluetooth_speaker"

CONF_AUTO_CONNECT = "auto_connect"

class BluetoothSpeakerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bluetooth Speaker."""

    VERSION = 1
    CONNECTION_CLASS = "local_poll"

    async def async_step_user(self, user_input: Dict[str, Any] = None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Check if this device is already configured
                await self.async_set_unique_id(f"bluetooth_speaker_{user_input[CONF_DEVICE]}")
                self._abort_if_unique_id_configured()

                # Verify device is still available
                devices = await self._async_get_bluetooth_devices()
                if user_input[CONF_DEVICE] not in devices:
                    errors["base"] = "device_unavailable"
                else:
                    # Create the config entry
                    return self.async_create_entry(
                        title=user_input[CONF_NAME],
                        data=user_input
                    )

            except Exception as err:
                _LOGGER.error("Unexpected error: %s", err)
                errors["base"] = "unknown"

        # Get list of available devices
        devices = await self._async_get_bluetooth_devices()
        
        if not devices:
            return self.async_abort(reason="no_devices")

        # Show the configuration form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_DEVICE): vol.In(devices),
                vol.Optional(CONF_AUTO_CONNECT, default=False): bool,
            }),
            errors=errors,
        )

    async def _async_get_bluetooth_devices(self) -> Dict[str, str]:
        """Scan for Bluetooth devices using bluetoothctl."""
        try:
            # Turn on Bluetooth if it's not already on
            await self.hass.async_add_executor_job(
                subprocess.run, 
                ["bluetoothctl", "power", "on"],
                {"check": True, "capture_output": True}
            )
            
            # Start scanning
            result = await self.hass.async_add_executor_job(
                subprocess.run,
                ["bluetoothctl", "scan", "on"],
                {"capture_output": True, "text": True, "timeout": 10}
            )
            
            # Get list of devices
            devices = {}
            for line in result.stdout.splitlines():
                if "Device" in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        address = parts[1]
                        name = " ".join(parts[2:])
                        devices[address] = name
            
            if not devices:
                _LOGGER.warning("No Bluetooth devices found")
            return devices
            
        except subprocess.TimeoutExpired:
            _LOGGER.error("Bluetooth scan timed out")
            return {}
        except subprocess.CalledProcessError as err:
            _LOGGER.error("Failed to scan Bluetooth devices: %s", err)
            return {}
        except Exception as err:
            _LOGGER.error("Unexpected error scanning Bluetooth devices: %s", err)
            return {}

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return BluetoothSpeakerOptionsFlow(config_entry)

class BluetoothSpeakerOptionsFlow(OptionsFlow):
    """Handle options flow for the component."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: Dict[str, Any] = None) -> FlowResult:
        """Manage basic options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_AUTO_CONNECT,
                    default=self.config_entry.options.get(CONF_AUTO_CONNECT, False),
                ): bool,
            }),
        )
