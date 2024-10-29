from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
from homeassistant.components.sensor import SensorEntity, PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import psycopg2
from homeassistant.config_entries import ConfigFlow

DOMAIN = "postgresql_sensors"

CONF_DATABASE = "database"
CONF_SQL_QUERY = "query"
CONF_SENSORS = "sensors"
CONF_NAME = "name"
CONF_COLUMN = "column"
CONF_UNIT = "unit"
CONF_ICON = "icon"

SENSOR_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_SQL_QUERY): cv.string,
    vol.Required(CONF_COLUMN): cv.string,
    vol.Optional(CONF_UNIT): cv.string,
    vol.Optional(CONF_ICON): cv.icon,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT, default=5432): cv.port,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_DATABASE): cv.string,
    vol.Required(CONF_SENSORS): vol.All(cv.ensure_list, [SENSOR_SCHEMA]),
})

class PostgreSQLSensorConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(title="PostgreSQL Sensor", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PORT, default=5432): int,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_DATABASE): str,
            })
        )

async def async_setup(hass, config):
    """Set up the PostgreSQL Sensors component."""
    return True

async def async_setup_entry(hass, entry):
    """Set up PostgreSQL Sensors from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the PostgreSQL Sensor platform."""
    host = config[CONF_HOST]
    port = config[CONF_PORT]
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]
    database = config[CONF_DATABASE]
    sensors = config[CONF_SENSORS]

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        conn.close()
    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return False

    entities = []
    for sensor_config in sensors:
        entities.append(PostgreSQLSensor(host, port, username, password, database, sensor_config))

    add_entities(entities, True)

class PostgreSQLSensor(SensorEntity):
    def __init__(self, host, port, username, password, database, sensor_config):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database
        self._name = sensor_config[CONF_NAME]
        self._query = sensor_config[CONF_SQL_QUERY]
        self._column = sensor_config[CONF_COLUMN]
        self._unit = sensor_config.get(CONF_UNIT)
        self._icon = sensor_config.get(CONF_ICON)
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f"{DOMAIN}_{self._name}"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def icon(self):
        return self._icon

    def update(self):
        try:
            conn = psycopg2.connect(
                host=self._host,
                port=self._port,
                database=self._database,
                user=self._username,
                password=self._password
            )
            cur = conn.cursor()
            cur.execute(self._query)
            result = cur.fetchone()
            if result:
                self._state = result[0]  # Assuming the first column is the state
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching sensor state from PostgreSQL: {e}")
#SELECT all_device_status.arg, all_device_status.update_time, all_node_config.name FROM all_device_status, all_node_config WHERE all_device_status.node_id = all_node_config.id and all_device_status.opcode = 'SWITCH' and all_node_id = 232;