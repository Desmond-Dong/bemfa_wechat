import logging
import aiohttp
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, CONF_UID

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    uid = entry.data[CONF_UID]

    async def handle_send_message(call: ServiceCall):
        device = call.data.get("device_entity")
        message = call.data.get("message", "").strip()
        group = call.data.get("group", "default")
        url = call.data.get("url", "")

        if not device or not message:
            _LOGGER.error("device_entity 和 message 参数必填")
            return

        state_obj = hass.states.get(device)
        if state_obj:
            friendly_name = state_obj.attributes.get("friendly_name", device)
            state_value = state_obj.state
        else:
            friendly_name = device
            state_value = "无实体状态"

        final_message = f"{friendly_name}（状态：{state_value}）: {message}"
        _LOGGER.debug("最终发送微信消息内容：%s", final_message)

        payload = {
            "uid": uid,
            "device": device.replace(".", "_"),
            "message": final_message,
            "group": group,
            "url": url,
        }

        headers = {"Content-Type": "application/json; charset=utf-8"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://apis.bemfa.com/vb/wechat/v1/wechatAlertJson",
                    json=payload,
                    headers=headers
                ) as response:
                    resp_text = await response.text()
                    if response.status == 200:
                        _LOGGER.info("微信消息发送成功")
                    else:
                        _LOGGER.error("发送失败 [%s]: %s", response.status, resp_text)
        except Exception as e:
            _LOGGER.exception("发送微信消息异常: %s", e)

    hass.services.async_register(DOMAIN, "send_message", handle_send_message)
    await hass.config_entries.async_forward_entry_setups(entry, ["button"])
    return True