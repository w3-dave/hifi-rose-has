# HiFi Rose Streamer - Home Assistant Integration

A custom integration for Home Assistant that allows local control of HiFi Rose Streamer devices over your local network (LAN), without relying on cloud services.

## Features

- Turn the streamer on/off
- Set volume via Home Assistant (0-100%)
- Switch between input sources:
  - STREAMER (built-in streaming)
  - LINE IN
  - OPTICAL IN
  - eARC IN
  - USB IN
  - AES/EBU IN
- Entity exposed as a `media_player` in Home Assistant
- UI-configurable via the Integrations page

## Limitations

- Volume slider does not reflect changes made directly on the device (API limitation)
- Power state and input source sync correctly in both directions
- No media playback metadata or album art support

## Network Setup

**Important:** Ensure your HiFi Rose Streamer has a **static IP address** assigned via your router. The integration communicates with the device on **port 9283** (configurable), which must be accessible on your LAN.

Examples:
- HTTP: `http://192.168.0.102:9283`
- HTTPS: `https://192.168.0.102:9283`

## Installation

### Method 1: Manual Installation

1. Copy the `hifirose_streamer` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant
3. Navigate to **Settings → Devices & Services → Add Integration**
4. Search for **HiFi Rose Streamer**
5. Enter the IP address of your device

### Method 2: HACS (if published)

1. Open HACS in Home Assistant
2. Search for "HiFi Rose Streamer"
3. Install the integration
4. Restart Home Assistant
5. Add the integration via Settings → Devices & Services

## Configuration

After installation:

1. Go to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **HiFi Rose Streamer**
4. Enter:
   - **Host**: The IP address of your device (e.g., `192.168.0.102`)
   - **Port**: (Optional) Port number (default: `9283`)
   - **Use SSL**: (Optional) Enable HTTPS (default: `off`)
   - **Verify SSL Certificate**: (Optional) Verify SSL certificates (default: `on`, disable for self-signed certificates)
   - **Name**: (Optional) Custom name for your device

The integration will test the connection and create a media player entity.

### HTTPS / SSL Notes

- **Use SSL**: Enable this if your device uses HTTPS instead of HTTP
- **Verify SSL Certificate**:
  - Keep enabled (default) for trusted certificates
  - Disable if using self-signed certificates (will suppress SSL warnings)

## Usage

### Basic Controls

Once configured, you can:

- **Power**: Turn the device on/off
- **Volume**: Adjust volume from 0-100%
- **Source**: Switch between input sources

### Automation Example

```yaml
automation:
  - alias: "Turn on HiFi Rose in the morning"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: media_player.turn_on
        target:
          entity_id: media_player.hifi_rose_streamer
      - service: media_player.select_source
        target:
          entity_id: media_player.hifi_rose_streamer
        data:
          source: "OPTICAL IN"
      - service: media_player.volume_set
        target:
          entity_id: media_player.hifi_rose_streamer
        data:
          volume_level: 0.3
```

## Tested With

- **Home Assistant Core**: 2024.x and later
- **HiFi Rose Firmware**: 5.9.02

## API Documentation

For developers: See the `curl-requests/` directory for complete API documentation with CURL examples for testing the device API directly.

## Troubleshooting

### Cannot connect to device

1. Verify the device has a static IP address
2. Ensure port 9283 is accessible (test with curl):
   ```bash
   curl -X POST http://YOUR_DEVICE_IP:9283/get_current_state \
     -H "Content-Type: application/json" \
     -d '{}'
   ```
3. Check your firewall settings
4. Verify the device is on the same network as Home Assistant

### Volume not syncing

This is a known API limitation. Volume changes made directly on the device will not be reflected in Home Assistant.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This integration is provided as-is for personal use.
