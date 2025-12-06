# 🌹 HiFi Rose Streamer - Home Assistant Integration

A custom integration for Home Assistant that provides local control of HiFi Rose Streamer devices over your LAN, without relying on cloud services. Includes complete API documentation and custom services for easy automation scripting.

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Integration-41BDF5.svg)](https://www.home-assistant.io/)
[![HiFi Rose](https://img.shields.io/badge/HiFi%20Rose-Streamer-red.svg)](https://www.hifirose.com/)

## 💡 Why This Exists

I built this integration for a fellow hi-fi enthusiast friend with a HiFi Rose RS150B. He wanted his Rose to power on automatically when he asked Alexa to "Turn on the TV" - a simple request, but there was no existing integration to make it happen.

With this plugin, Home Assistant listens for the TV power-on event, then sends a power-on command followed by an input select command to the Rose. The Rose then uses its 12V trigger outputs to power up the amps. Voila, problem solved. Now his entire system springs to life with a single voice command.

If you've got a similar setup or just want local control of your HiFi Rose without relying on cloud services, this integration is for you.

## ✨ Features

### Core Functionality
- **Power Control** - Turn the streamer on/off
- **Volume Control** - Set volume from 0-100%
- **Input Source Switching** - Switch between 6 input sources:
  - STREAMER (built-in streaming)
  - LINE IN
  - OPTICAL IN
  - eARC IN
  - USB IN
  - AES/EBU IN
- **State Polling** - Automatic state synchronization every 30 seconds
- **SSL Support** - Configurable HTTP/HTTPS with optional certificate verification

### Custom Services for Automations

The integration provides 7 custom services in the `hifirose_streamer` domain for easier automation scripting:

**Mute Toggle:**
- `hifirose_streamer.mute` - Toggle mute (sets volume to 0 or restores previous level)

**Quick Source Switches:**
- `hifirose_streamer.switch_to_streamer` - Switch to STREAMER
- `hifirose_streamer.switch_to_line_in` - Switch to LINE IN
- `hifirose_streamer.switch_to_optical` - Switch to OPTICAL IN
- `hifirose_streamer.switch_to_earc` - Switch to eARC IN
- `hifirose_streamer.switch_to_usb` - Switch to USB IN
- `hifirose_streamer.switch_to_aes_ebu` - Switch to AES/EBU IN

## 📁 Repository Structure

```
hifi-rose-has/
├── hifirose_streamer/          # Home Assistant custom integration
│   ├── __init__.py            # Entry point, service registration
│   ├── config_flow.py         # UI configuration flow
│   ├── media_player.py        # Media player entity implementation
│   ├── const.py               # Constants and defaults
│   ├── services.yaml          # Service definitions for HA UI
│   ├── manifest.json          # Integration metadata
│   └── README.md              # Integration-specific documentation
│
├── example-curl-requests/      # Complete API documentation
│   ├── README.md              # API overview and quick start
│   ├── power-on.md            # Power on endpoint
│   ├── power-off.md           # Power off endpoint
│   ├── set-volume.md          # Volume control endpoint
│   ├── set-input-source.md   # Input source endpoint
│   └── get-state.md           # State polling endpoint
│
└── CLAUDE.md                  # Development guide for AI assistants
```

## 📦 Installation

### Prerequisites

- Home Assistant Core 2024.x or later
- HiFi Rose Streamer with **static IP address**
- Network access to device port **9283** (configurable)

### Method 1: Manual Installation

1. Copy the `hifirose_streamer` directory to your Home Assistant `custom_components` directory:
   ```bash
   cp -r hifirose_streamer/ /config/custom_components/
   ```

2. Restart Home Assistant

3. Add the integration:
   - Navigate to **Settings → Devices & Services**
   - Click **Add Integration**
   - Search for **HiFi Rose Streamer**
   - Follow the configuration steps

### Method 2: HACS (Future)

*This integration is not yet published to HACS. Use manual installation for now.*

## ⚙️ Configuration

When adding the integration, you'll be prompted for:

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| **Host** | Yes | - | IP address of your HiFi Rose device (e.g., `192.168.0.102`) |
| **Port** | No | `9283` | Port number for API communication |
| **Use SSL** | No | `false` | Enable HTTPS instead of HTTP |
| **Verify SSL Certificate** | No | `true` | Verify SSL certificates (disable for self-signed certs) |
| **Name** | No | `HiFi Rose Streamer` | Custom name for the device |

The integration will test the connection before completing setup.

### Network Setup Tips

1. **Assign a static IP** to your HiFi Rose device via your router's DHCP reservation
2. **Test connectivity** before configuring Home Assistant:
   ```bash
   curl -X POST http://YOUR_DEVICE_IP:9283/get_current_state \
     -H "Content-Type: application/json" \
     -d '{}'
   ```
3. **Check firewall rules** if connection fails

## 🎛️ Usage

### Standard Media Player Services

Once configured, the device appears as a `media_player` entity with these standard Home Assistant services:

```yaml
# Turn on/off
service: media_player.turn_on
target:
  entity_id: media_player.hifi_rose_streamer

# Set volume (0.0 to 1.0 scale)
service: media_player.volume_set
target:
  entity_id: media_player.hifi_rose_streamer
data:
  volume_level: 0.5

# Select input source
service: media_player.select_source
target:
  entity_id: media_player.hifi_rose_streamer
data:
  source: "OPTICAL IN"
```

### Custom Services for Automations

Use the integration's custom services for cleaner automation scripts:

```yaml
# Mute toggle (remembers previous volume)
service: hifirose_streamer.mute
target:
  entity_id: media_player.hifi_rose_streamer

# Quick source switch (no need to remember source names)
service: hifirose_streamer.switch_to_optical
target:
  entity_id: media_player.hifi_rose_streamer
```

### Automation Examples

#### Morning Wake-Up Routine
```yaml
automation:
  - alias: "Morning music setup"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: media_player.turn_on
        target:
          entity_id: media_player.hifi_rose_streamer
      - service: hifirose_streamer.switch_to_line_in
        target:
          entity_id: media_player.hifi_rose_streamer
      - service: media_player.volume_set
        target:
          entity_id: media_player.hifi_rose_streamer
        data:
          volume_level: 0.3
```

#### Mute on Doorbell
```yaml
automation:
  - alias: "Mute audio when doorbell rings"
    trigger:
      - platform: state
        entity_id: binary_sensor.doorbell
        to: "on"
    action:
      - service: hifirose_streamer.mute
        target:
          entity_id: media_player.hifi_rose_streamer
```

#### TV Time Source Switch
```yaml
automation:
  - alias: "Switch to TV input at night"
    trigger:
      - platform: time
        at: "20:00:00"
    action:
      - service: hifirose_streamer.switch_to_earc
        target:
          entity_id: media_player.hifi_rose_streamer
```

## 📡 API Documentation

The `example-curl-requests/` directory contains complete API documentation with curl examples for all endpoints:

- **Power Control** - `/remote_bar_order` endpoint (on/off)
- **Volume** - `/volume` endpoint (0-100 scale)
- **Input Source** - `/input.mode.set` endpoint (funcMode 0-5)
- **State Polling** - `/get_current_state` endpoint (returns current state)

See [example-curl-requests/README.md](example-curl-requests/README.md) for full API reference and testing examples.

## ⚠️ Known Limitations

- **Volume sync**: Volume changes made directly on the device hardware are not reflected in Home Assistant (API limitation)
- **Power/Source sync**: Power state and input source sync correctly in both directions ✓
- **No media metadata**: API does not provide playback information, album art, or media controls
- **No transport controls**: No play/pause/next/previous functionality available

## 🔧 Troubleshooting

### Cannot Connect to Device

1. Verify the device has a static IP address
2. Test API connectivity with curl:
   ```bash
   curl -X POST http://YOUR_DEVICE_IP:9283/get_current_state \
     -H "Content-Type: application/json" \
     -d '{}'
   ```
3. Check firewall settings on your network
4. Verify device is on the same network as Home Assistant
5. Ensure port 9283 is not blocked

### Volume Not Syncing

This is a known API limitation. The device does not report volume changes made via hardware controls. Power state and input source sync correctly.

### SSL Certificate Errors

If using HTTPS with a self-signed certificate, disable SSL verification during setup:
- Set **Verify SSL Certificate** to `off` during configuration

## 🛠️ Development

### Testing the API Directly

All API endpoints can be tested with curl before integrating with Home Assistant. See the `example-curl-requests/` directory for examples.

### Architecture Overview

- **Entry Point**: `hifirose_streamer/__init__.py` - Handles setup, service registration, and lifecycle
- **Config Flow**: `hifirose_streamer/config_flow.py` - UI-based configuration with connection testing
- **Media Player**: `hifirose_streamer/media_player.py` - Main entity implementation with state polling
- **Services**: Custom services registered in `__init__.py`, defined in `services.yaml`

For detailed architecture documentation, see [CLAUDE.md](CLAUDE.md).

## ✅ Tested With

- **Home Assistant Core**: 2024.x and later
- **HiFi Rose Firmware**: 5.9.02 (RS520 model)
- **Python**: 3.11+

## 🤝 Contributing

Contributions are welcome! Please feel free to submit:
- Bug reports
- Feature requests
- Pull requests
- Documentation improvements

## 💬 Support

For issues and questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [API documentation](example-curl-requests/)
3. Open an issue on GitHub

If you find this integration useful and want to support its development, consider buying me a coffee ☕:

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Development-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/w3dave/)

## Disclaimer

This project is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

This integration is an independent, community-developed project and is not affiliated with, endorsed by, or supported by HiFi Rose or Citech Co., Ltd. "HiFi Rose" and related product names are trademarks of their respective owners. Use of these names is for identification purposes only and does not imply any endorsement or sponsorship.

Use this integration at your own risk. The authors are not responsible for any damage to your equipment, loss of data, or other issues that may arise from the use of this software.

## License

MIT License - see source files for details.

---

**Made for the Home Assistant community** 🏠
