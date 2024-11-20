"""Bluetooth speaker control for Home Assistant."""
import logging
import asyncio
import subprocess
from typing import Optional
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)

class BluetoothController:
    """Class to handle Bluetooth speaker connections using bluetoothctl."""
    
    def __init__(self, hass: HomeAssistant, address: str, name: str):
        """Initialize the Bluetooth controller."""
        self.hass = hass
        self.address = address
        self.name = name
        self.connected = False
        self._error_count = 0
        self.MAX_RETRIES = 3

    async def _run_bluetoothctl_command(self, *args) -> tuple[bool, str]:
        """Run a bluetoothctl command."""
        try:
            cmd = ["bluetoothctl"] + list(args)
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            success = process.returncode == 0
            output = stdout.decode().strip()
            
            if not success:
                error = stderr.decode().strip()
                _LOGGER.error("Bluetoothctl command failed: %s", error)
                return False, error
                
            return True, output
            
        except Exception as err:
            _LOGGER.error("Error running bluetoothctl command: %s", str(err))
            return False, str(err)

    async def connect(self) -> bool:
        """Establish connection to the Bluetooth speaker."""
        try:
            # First pair with the device if not already paired
            success, _ = await self._run_bluetoothctl_command("pair", self.address)
            if not success:
                return False

            # Then try to connect
            success, output = await self._run_bluetoothctl_command("connect", self.address)
            if success:
                self.connected = True
                self._error_count = 0
                _LOGGER.info("Successfully connected to %s (%s)", self.name, self.address)
                return True
            
            self._error_count += 1
            return False
            
        except Exception as err:
            self._error_count += 1
            _LOGGER.error("Failed to connect to %s: %s", self.name, str(err))
            self.connected = False
            return False

    async def disconnect(self) -> bool:
        """Disconnect from the Bluetooth speaker."""
        try:
            success, _ = await self._run_bluetoothctl_command("disconnect", self.address)
            if success:
                _LOGGER.info("Disconnected from %s", self.name)
            else:
                _LOGGER.warning("Failed to disconnect from %s", self.name)
            
            self.connected = False
            return success
            
        except Exception as err:
            _LOGGER.error("Error disconnecting from %s: %s", self.name, str(err))
            self.connected = False
            return False

    async def is_available(self) -> bool:
        """Check if the Bluetooth speaker is available."""
        try:
            success, output = await self._run_bluetoothctl_command("info", self.address)
            if not success:
                return False
                
            # Check if device is found in the output
            return "Device" in output and self.address in output
            
        except Exception as err:
            _LOGGER.error("Error checking device availability: %s", str(err))
            return False

    async def get_connection_status(self) -> bool:
        """Get the current connection status of the device."""
        try:
            success, output = await self._run_bluetoothctl_command("info", self.address)
            if not success:
                return False
                
            # Check if device is connected
            return "Connected: yes" in output
            
        except Exception as err:
            _LOGGER.error("Error getting connection status: %s", str(err))
            return False

    async def reconnect(self) -> bool:
        """Attempt to reconnect to the Bluetooth speaker."""
        if self._error_count >= self.MAX_RETRIES:
            _LOGGER.error(
                "Maximum reconnection attempts reached for %s", self.name
            )
            return False

        _LOGGER.info("Attempting to reconnect to %s", self.name)
        await self.disconnect()
        return await self.connect()

    async def trust_device(self) -> bool:
        """Trust the Bluetooth device for automatic connections."""
        try:
            success, _ = await self._run_bluetoothctl_command("trust", self.address)
            if success:
                _LOGGER.info("Successfully trusted device %s", self.name)
            return success
        except Exception as err:
            _LOGGER.error("Error trusting device %s: %s", self.name, str(err))
            return False
