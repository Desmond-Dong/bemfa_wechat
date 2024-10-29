from homeassistant import config_entries
import voluptuous as vol
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
import psycopg2
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.typing import ConfigType

DOMAIN = "postgresql_sensors"

CONF_DATABASE = "database"
CONF_SQL_QUERY = "sql_query"
CONF_HOST = "host"
CONF_PORT = "port"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

class PostgreSQLSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                # Test the connection
                conn = psycopg2.connect(
                    host=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                    database=user_input[CONF_DATABASE],
                    user=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD]
                )
                conn.close()
                return self.async_create_entry(title="PostgreSQL Sensors", data=user_input)
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PORT, default=5432): int,
                vol.Required(CONF_DATABASE): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_SQL_QUERY): str,
            }),
            errors=errors,
        )

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    """Set up PostgreSQL Sensors from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    try:
        # Test the connection
        conn = psycopg2.connect(
            host=entry.data[CONF_HOST],
            port=entry.data[CONF_PORT],
            database=entry.data[CONF_DATABASE],
            user=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD]
        )
        conn.close()
    except Exception as e:
        raise ConfigEntryNotReady(f"Failed to connect to PostgreSQL: {str(e)}")
    
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the PostgreSQL Sensors component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the PostgreSQL Sensors component."""
    return True