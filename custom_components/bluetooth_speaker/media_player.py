import logging
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    MediaPlayerEntityFeature,
    MediaPlayerState,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Bluetooth speaker media player from a config entry."""
    
    # Retrieve data from hass data and log it
    data = hass.data["bluetooth_speaker"].get(config_entry.entry_id, {})
    _LOGGER.debug("Bluetooth Speaker Data: %s", data)
    
    # Check if data is a dictionary with required keys
    if isinstance(data, dict) and "name" in data and "mac_address" in data:
        name = data["name"]
        mac_address = data["mac_address"]
        async_add_entities([BluetoothSpeakerEntity(name, mac_address)])
    else:
        _LOGGER.error("Invalid data format. Missing 'name' or 'mac_address'.")
        raise ValueError("Invalid data format for Bluetooth speaker.")

class BluetoothSpeakerEntity(MediaPlayerEntity):
    """Representation of a Bluetooth Speaker."""

    def __init__(self, name, mac_address):
        """Initialize the Bluetooth Speaker."""
        self._name = name
        self._mac_address = mac_address
        self._state = MediaPlayerState.OFF
        self._supported_features = (
            MediaPlayerEntityFeature.TURN_ON
            | MediaPlayerEntityFeature.TURN_OFF
            | MediaPlayerEntityFeature.VOLUME_SET
        )

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return self._supported_features

    async def async_turn_on(self):
        """Turn the media player on."""
        self._state = MediaPlayerState.ON
        self.async_write_ha_state()

    async def async_turn_off(self):
        """Turn the media player off."""
        self._state = MediaPlayerState.OFF
        self.async_write_ha_state()

    async def async_set_volume_level(self, volume):
        """Set the volume level."""
        # Replace with Bluetooth volume control logic
        pass
