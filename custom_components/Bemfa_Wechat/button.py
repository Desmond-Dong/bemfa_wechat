from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

class BemfaWeChatButton(ButtonEntity):
    def __init__(self, hass, uid):
        self._hass = hass
        self._attr_name = "测试微信按钮"
        self._attr_unique_id = f"{DOMAIN}_button_test"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, uid)},
            name="Bemfa 微信",
            manufacturer="Bemfa"
        )

    async def async_press(self):
        await self._hass.services.async_call(
            DOMAIN,
            "send_message",
            {
                "device_entity": "test_device_entity",
                "message": "测试微信消息(this is a test message)",
                "group": "test",
                "url": ""
            },
            blocking=True
        )