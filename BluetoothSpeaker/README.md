# Bluetooth Speaker Integration for Home Assistant

A custom integration to control Bluetooth speakers in Home Assistant.

## Features
- Connect to and control Bluetooth speakers
- Auto-connect option on Home Assistant startup
- Volume and playback controls
- Connection status monitoring
- Easy configuration through UI

## Requirements
- Home Assistant running on a Linux-based system
- Bluetooth capability
- `bluetoothctl` command available

## Installation via HACS
1. Go to HACS > Integrations > Add Repository
2. Enter the GitHub URL for this repository
3. Install the `Bluetooth Speaker` integration
4. Restart Home Assistant
5. Add the integration in Settings > Devices & Services

## Manual Installation
1. Copy the `custom_components/bluetooth_speaker` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Add the integration through the UI

## Configuration
The integration can be configured entirely through the UI. You'll need to:
1. Select your Bluetooth speaker from discovered devices
2. Set a name for the device
3. Choose whether to auto-connect on startup

## Troubleshooting
- Ensure Bluetooth is enabled on your Home Assistant system
- Check that the speaker is in pairing mode when setting up
- Verify that `bluetoothctl` is available by running it in SSH
- Check Home Assistant logs for detailed error messages

## Support
If you encounter issues or have feature requests, please:
1. Check existing issues on GitHub
2. Create a new issue with detailed information about your setup and the problem

## Contributing
Contributions are welcome! Please feel free to submit pull requests.
