"""Platform for sensor integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from pyezviz import EzvizClient
import voluptuous as vol

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import Throttle

from .const import DOMAIN, CONF_ACCOUNT, CONF_PASSWORD, CONF_DEVICE_SERIAL

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="battery",
        name="Battery",
        native_unit_of_measurement="%",
        icon="mdi:battery",
    ),
    SensorEntityDescription(
        key="last_capture",
        name="Last Capture",
        icon="mdi:camera",
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the EZVIZ Doorbell sensor."""
    account = config_entry.data[CONF_ACCOUNT]
    password = config_entry.data[CONF_PASSWORD]
    device_serial = config_entry.data[CONF_DEVICE_SERIAL]

    client = EzvizClient(account, password)
    doorbell = EzvizDoorbellData(hass, client, device_serial)

    async_add_entities(
        EzvizDoorbellSensor(doorbell, description)
        for description in SENSOR_TYPES
    )

class EzvizDoorbellData:
    """Get the latest data from EZVIZ."""

    def __init__(self, hass, client, device_serial):
        """Initialize."""
        self.hass = hass
        self.client = client
        self.device_serial = device_serial
        self.battery = None
        self.last_capture = None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Update the data from EZVIZ."""
        try:
            await self.hass.async_add_executor_job(self.client.login)
            devices = await self.hass.async_add_executor_job(self.client.get_devices)
            for device in devices:
                if device['serial'] == self.device_serial:
                    self.battery = device.get('battery', None)
                    break

            # Get the last capture image URL
            captures = await self.hass.async_add_executor_job(
                self.client.get_detection_sensibility, self.device_serial
            )
            if captures and 'url' in captures:
                self.last_capture = captures['url']
        except Exception as error:
            _LOGGER.error("Error updating EZVIZ data: %s", error)

class EzvizDoorbellSensor(SensorEntity):
    """Representation of a EZVIZ Doorbell sensor."""

    def __init__(self, doorbell, description: SensorEntityDescription):
        """Initialize the sensor."""
        self.doorbell = doorbell
        self.entity_description = description
        self._attr_unique_id = f"{doorbell.device_serial}_{description.key}"
        self._attr_name = f"EZVIZ Doorbell {description.name}"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.entity_description.key == "battery":
            return self.doorbell.battery
        elif self.entity_description.key == "last_capture":
            return self.doorbell.last_capture

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        await self.doorbell.async_update()