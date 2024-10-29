import json
import aiohttp
import asyncio
from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID, STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.switch import SwitchEntity
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "konke_zigbee_switch"
CONF_JSON_URL = "json_url"
UPDATE_INTERVAL = 5  # Update interval in seconds

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Konke Zigbee switch platform."""
    json_url = config.get(CONF_JSON_URL, "http://127.0.0.1:8000/")

    # Fetch switch configurations from JSON URL
    async with aiohttp.ClientSession() as session:
        async with session.get(json_url) as response:
            if response.status == 200:
                switch_configs = await response.json()
            else:
                _LOGGER.error(f"Failed to fetch switch configurations: HTTP {response.status}")
                return

    # Create switch entities
    switches = []
    for switch_config in switch_configs:
        switch = KonkeZigbeeSwitch(switch_config, json_url)
        switches.append(switch)
        _LOGGER.info(f"Adding switch: {switch.name} with unique_id: {switch.unique_id}")

    add_entities(switches, True)

class KonkeZigbeeSwitch(SwitchEntity):
    """Representation of a Konke Zigbee switch."""

    def __init__(self, config, json_url):
        """Initialize the switch."""
        self._name = config.get("name")
        self._unique_id = f"konke_zigbee_switch_{self._name}"
        self._state = config.get("state") == "ON"
        self._available = True
        self._json_url = json_url
        self._update_time = config.get("update_time")
        self._attr_device_class = "switch"

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the switch."""
        return self._unique_id

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "update_time": self._update_time
        }

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        # Implement the logic to turn on the switch
        self._state = True
        await self.async_update()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        # Implement the logic to turn off the switch
        self._state = False
        await self.async_update()

    async def async_update(self):
        """Fetch new state data for the switch."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._json_url) as response:
                    if response.status == 200:
                        switch_configs = await response.json()
                        for switch in switch_configs:
                            if switch.get("name") == self._name:
                                self._state = switch.get("state") == "ON"
                                self._update_time = switch.get("update_time")
                                self._available = True
                                _LOGGER.debug(f"Updated switch {self._name}: state={self._state}, update_time={self._update_time}")
                                break
                    else:
                        _LOGGER.error(f"Failed to fetch switch states: HTTP {response.status}")
                        self._available = False
        except Exception as e:
            _LOGGER.error(f"Error updating switch state: {str(e)}")
            self._available = False
        self.async_write_ha_state()

# manifest.json content:
"""
{
    "domain": "konke_zigbee_switch",
    "name": "Konke Zigbee Switch",
    "documentation": "https://github.com/your_username/konke_zigbee_switch",
    "dependencies": [],
    "codeowners": ["@your_github_username"],
    "requirements": ["aiohttp"],
    "iot_class": "local_polling",
    "version": "0.1.0"
}
"""
