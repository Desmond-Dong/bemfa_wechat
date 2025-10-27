"""巴法微信按钮平台"""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class BemfaWeChatButton(ButtonEntity):
    """巴法微信测试按钮"""

    def __init__(self, hass: HomeAssistant, uid: str) -> None:
        """初始化按钮"""
        self._hass = hass
        self._uid = uid
        self._attr_name = "微信消息测试"
        self._attr_unique_id = f"{DOMAIN}_{uid}_test"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, uid)},
            name="Bemfa 微信通知",
            manufacturer="Bemfa"
        )

    async def async_press(self) -> None:
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

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """设置巴法微信按钮实体"""
    uid = entry.data.get("uid")

    # 创建测试按钮
    button = BemfaWeChatButton(hass, uid)
    async_add_entities([button], True)

    _LOGGER.info("巴法微信按钮已添加: %s", button.name)