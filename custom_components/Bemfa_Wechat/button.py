from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
from .const import DOMAIN, CONF_UID

class BemfaWeChatButton(ButtonEntity):
    def __init__(self, hass: HomeAssistant, uid: str):
        self._hass = hass
        self._uid = uid
        self._attr_name = "发送测试微信消息"
        self._attr_unique_id = f"{DOMAIN}_test_button"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, uid)},
            name="Bemfa 微信设备",
            manufacturer="Bemfa",
        )

    @property
    def available(self) -> bool:
        return True

    async def async_press(self):
        _LOGGER.info("BemfaWeChatButton clicked, calling send_message service")
        await self._hass.services.async_call(
            DOMAIN,
            "send_message",
            {
                "device_entity": "sensor.example_entity",
                "message": "测试按钮触发的微信消息",
                "group": "default",
                "url": "",
            },
        )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    uid = entry.data[CONF_UID]
    async_add_entities([BemfaWeChatButton(hass, uid)])
