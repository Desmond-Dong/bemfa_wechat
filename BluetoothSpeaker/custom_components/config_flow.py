import subprocess
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_DEVICE
import homeassistant.helpers.config_validation as cv
from homeassistant.core import callback

DOMAIN = "bluetooth_speaker"

CONF_AUTO_CONNECT = "auto_connect"

def get_bluetooth_devices():
    """使用 bluetoothctl 列出附近的蓝牙设备。"""
    result = subprocess.run(
        ["bluetoothctl", "scan", "on"], capture_output=True, text=True, timeout=10
    )
    devices = {}
    for line in result.stdout.splitlines():
        if "Device" in line:
            parts = line.split()
            if len(parts) >= 3:
                devices[parts[1]] = " ".join(parts[2:])
    return devices

class BluetoothSpeakerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME], data=user_input
            )

        devices = get_bluetooth_devices()
        device_choices = {address: name for address, name in devices.items()}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_DEVICE): vol.In(device_choices),
                vol.Optional(CONF_AUTO_CONNECT, default=False): bool,
            }),
            errors=errors,
        )
