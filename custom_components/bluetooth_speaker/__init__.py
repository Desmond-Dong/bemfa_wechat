from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType


from .const import DOMAIN
from .media_player import BluetoothSpeakerEntity

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Bluetooth Speaker integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    hass.data[DOMAIN][entry.entry_id] = BluetoothSpeakerEntity(
        name=entry.data["name"], mac_address=entry.data["mac_address"]
    )

    # Forward the setup to the media_player platform
    await hass.config_entries.async_forward_entry_setups(entry, ["media_player"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["media_player"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
