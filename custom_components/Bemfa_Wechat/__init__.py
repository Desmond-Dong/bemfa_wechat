import logging
import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import service
from .const import DOMAIN, CONF_UID

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigType):
    """Set up Bemfa WeChat from a config entry."""
    uid = entry.data[CONF_UID]

    async def handle_send_message(call):
        """Handle the send_message service call."""
        device = call.data.get("device")
        message = call.data.get("message")
        group = call.data.get("group", "default")  # 默认分组
        url = call.data.get("url", "")  # 默认空链接

        if not device or not message:
            _LOGGER.error("Device and message must be provided")
            return

        api_url = "https://apis.bemfa.com/vb/wechat/v1/wechatAlertJson"
        payload = {
            "uid": uid,
            "device": device,
            "message": message,
            "group": group,
            "url": url,
        }

        headers = {"Content-Type": "application/json; charset=utf-8"}

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    _LOGGER.info("Message sent successfully!")
                else:
                    _LOGGER.error("Failed to send message: %s", await response.text())

    # 注册服务，确保通过 async_register 注册服务
    hass.services.async_register(DOMAIN, "send_message", handle_send_message)
    return True
