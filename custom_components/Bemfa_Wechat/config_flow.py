import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_UID

_LOGGER = logging.getLogger(__name__)

class BemfaWeChatConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理巴法微信配置流程"""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """处理用户输入的初始步骤"""
        errors = {}

        if user_input is not None:
            uid = user_input.get(CONF_UID, "").strip()

            if not uid:
                errors["base"] = "empty_uid"
            elif len(uid) < 8:
                errors["base"] = "invalid_uid"
            else:
                # 验证UID格式（巴法UID通常为特定格式）
                await self.async_set_unique_id(uid)
                self._abort_if_unique_id_configured()

                # 创建配置条目
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, "Bemfa 微信"),
                    data={
                        CONF_UID: uid,
                        CONF_NAME: user_input.get(CONF_NAME, "Bemfa 微信")
                    }
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default="Bemfa 微信"): str,
                vol.Required(CONF_UID): str,
            }),
            errors=errors,
        )

    async def async_step_import(self, import_config):
        """处理配置文件导入"""
        return await self.async_step_user(import_config)