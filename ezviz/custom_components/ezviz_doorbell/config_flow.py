"""Config flow for EZVIZ Doorbell integration."""
from __future__ import annotations

import logging
from typing import Any

from pyezviz import EzvizClient
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_ACCOUNT, CONF_PASSWORD, CONF_DEVICE_SERIAL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCOUNT): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_DEVICE_SERIAL): str,
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    client = EzvizClient(data[CONF_ACCOUNT], data[CONF_PASSWORD])

    try:
        await hass.async_add_executor_job(client.login)
        devices = await hass.async_add_executor_job(client.get_devices)
    except Exception as error:
        raise InvalidAuth from error

    if not any(device['serial'] == data[CONF_DEVICE_SERIAL] for device in devices):
        raise DeviceNotFound

    return {"title": f"EZVIZ Doorbell {data[CONF_DEVICE_SERIAL]}"}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EZVIZ Doorbell."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except DeviceNotFound:
                errors["base"] = "device_not_found"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

class DeviceNotFound(HomeAssistantError):
    """Error to indicate the device was not found."""