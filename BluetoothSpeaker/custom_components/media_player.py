"""Media player platform for Bluetooth speaker integration."""
import logging
import voluptuous as vol
from typing import Optional
from homeassistant.core import HomeAssistant
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)
from homeassistant.const import (
    STATE_PLAYING,
    STATE_PAUSED,
    STATE_IDLE,
    STATE_OFF,
    STATE_UNAVAILABLE,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .Bluetooth import BluetoothController

_LOGGER = logging.getLogger(__name__)

SUPPORT_BLUETOOTH_SPEAKER = (
    MediaPlayerEntityFeature.PLAY 
    | MediaPlayerEntityFeature.PAUSE
    | MediaPlayerEntityFeature.VOLUME_SET
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bluetooth Speaker from a config entry."""
    name = config_entry.data["name"]
    address = config_entry.data["device"]
    auto_connect = config_entry.data.get("auto_connect", False)

    async_add_entities(
        [BluetoothSpeaker(hass, name, address, auto_connect)],
        True,
    )

class BluetoothSpeaker(MediaPlayerEntity):
    """Representation of a Bluetooth speaker."""

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        device_address: str,
        auto_connect: bool,
    ):
        """Initialize the Bluetooth speaker."""
        self._hass = hass
        self._name = name
        self._device_address = device_address
        self._auto_connect = auto_connect
        self._state = STATE_OFF
        self._volume = 0.5
        self._available = False
        self._attr_unique_id = f"bluetooth_speaker_{device_address}"
        
        self._bluetooth = BluetoothController(
            hass=hass,
            address=device_address,
            name=name,
        )

    async def async_added_to_hass(self) -> None:
        """Handle entity being added to Home Assistant."""
        if self._auto_connect:
            _LOGGER.info("Auto-connecting to Bluetooth device %s", self._device_address)
            await self._connect()

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return self._name

    @property
    def state(self) -> Optional[str]:
        """Return the state of the device."""
        return self._state

    @property
    def volume_level(self) -> float:
        """Volume level of the media player (0..1)."""
        return self._volume

    @property
    def supported_features(self) -> int:
        """Flag media player features that are supported."""
        return SUPPORT_BLUETOOTH_SPEAKER

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    async def _connect(self) -> None:
        """Connect to the Bluetooth device."""
        if await self._bluetooth.connect():
            self._state = STATE_IDLE
            self._available = True
            if self._auto_connect:
                await self._bluetooth.trust_device()
        else:
            self._state = STATE_UNAVAILABLE
            self._available = False

    async def _disconnect(self) -> None:
        """Disconnect from the Bluetooth device."""
        if await self._bluetooth.disconnect():
            self._state = STATE_OFF
        self._available = False

    async def async_media_play(self) -> None:
        """Send play command."""
        if not self._available:
            await self._connect()
        if self._available:
            self._state = STATE_PLAYING

    async def async_media_pause(self) -> None:
        """Send pause command."""
        if self._available:
            self._state = STATE_PAUSED

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        if self._available:
            self._volume = volume
            # Here you would implement the actual volume control
            # This might require additional bluetoothctl commands or other methods
            # depending on your speaker's capabilities

    async def async_update(self) -> None:
        """Fetch state from the device."""
        # Check if device is still available
        if await self._bluetooth.is_available():
            if not self._available and self._auto_connect:
                await self._connect()
            elif self._available:
                # Update connection status
                self._available = await self._bluetooth.get_connection_status()
                if not self._available:
                    self._state = STATE_UNAVAILABLE
        else:
            self._available = False
            self._state = STATE_UNAVAILABLE

    async def async_turn_off(self) -> None:
        """Turn the media player off."""
        await self._disconnect()

    async def async_turn_on(self) -> None:
        """Turn the media player on."""
        await self._connect()
