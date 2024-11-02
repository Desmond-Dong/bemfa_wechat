import logging
import subprocess
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    SUPPORT_PLAY,
    SUPPORT_PAUSE,
    SUPPORT_VOLUME_SET,
)
from homeassistant.const import STATE_PLAYING, STATE_PAUSED, STATE_IDLE
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

SUPPORT_BLUETOOTH_SPEAKER = SUPPORT_PLAY | SUPPORT_PAUSE | SUPPORT_VOLUME_SET

class BluetoothSpeaker(MediaPlayerEntity):
    def __init__(self, name, device_address, auto_connect):
        self._name = name
        self._device_address = device_address
        self._auto_connect = auto_connect
        self._state = STATE_IDLE
        self._volume = 0.5

    async def async_added_to_hass(self):
        """在 Home Assistant 启动时调用。如果启用了自动连接，尝试连接蓝牙设备。"""
        if self._auto_connect:
            _LOGGER.info("Auto-connecting to Bluetooth device %s", self._device_address)
            self.connect()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def volume_level(self):
        return self._volume

    @property
    def supported_features(self):
        return SUPPORT_BLUETOOTH_SPEAKER

    def connect(self):
        """使用 bluetoothctl 连接蓝牙设备。"""
        try:
            subprocess.run(["bluetoothctl", "power", "on"], check=True)
            subprocess.run(["bluetoothctl", "agent", "on"], check=True)
            subprocess.run(["bluetoothctl", "connect", self._device_address], check=True)
            self._state = STATE_IDLE
            _LOGGER.info("Connected to Bluetooth device %s", self._device_address)
        except subprocess.CalledProcessError as e:
            _LOGGER.error("Failed to connect: %s", e)
            self._state = None

    def disconnect(self):
        """使用 bluetoothctl 断开蓝牙设备。"""
        try:
            subprocess.run(["bluetoothctl", "disconnect", self._device_address], check=True)
            self._state = STATE_IDLE
            _LOGGER.info("Disconnected from Bluetooth device %s", self._device_address)
        except subprocess.CalledProcessError as e:
            _LOGGER.error("Failed to disconnect: %s", e)

    def media_play(self):
        self._state = STATE_PLAYING
        # 实现播放逻辑

    def media_pause(self):
        self._state = STATE_PAUSED
        # 实现暂停逻辑

    def set_volume_level(self, volume):
        self._volume = volume
        # 实现音量控制逻辑
