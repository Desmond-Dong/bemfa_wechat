from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

class BemfaWeChatButton(ButtonEntity):
    def __init__(self, hass, uid):
        self._hass = hass
        self._attr_name = "微信消息测试"
        self._attr_unique_id = f"{DOMAIN}_button_test"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, uid)},
            name="Bemfa 微信通知",
            manufacturer="Bemfa"
        )

    async def async_press(self):
        """执行按钮按压操作 - 发送测试消息"""
        await self._hass.services.async_call(
            DOMAIN,
            "send_message",
            {
                "device_entity": "sun.sun",
                "message": "这是一条来自 Home Assistant 的测试消息",
                "group": "test",
                "url": ""
            },
            blocking=True
        )