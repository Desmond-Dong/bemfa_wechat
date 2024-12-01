from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)
from homeassistant.const import STATE_OFF, STATE_ON

class BluetoothSpeaker(MediaPlayerEntity):
    """Representation of a Bluetooth Speaker."""

    def __init__(self, name, mac_address):
        self._name = name
        self._mac_address = mac_address
        self._state = STATE_OFF

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        return MediaPlayerEntityFeature.PLAY | MediaPlayerEntityFeature.PAUSE

    async def async_turn_on(self):
        """Turn on the Bluetooth speaker."""
        # Add logic to connect to the speaker
        self._state = STATE_ON
        self.async_write_ha_state()

    async def async_turn_off(self):
        """Turn off the Bluetooth speaker."""
        # Add logic to disconnect the speaker
        self._state = STATE_OFF
        self.async_write_ha_state()
