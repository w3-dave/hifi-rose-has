# HiFi Rose Streamer API - CURL Examples

This directory contains CURL request examples for controlling HiFi Rose Streamer devices via the local HTTP API.

## Prerequisites

- HiFi Rose Streamer with static IP address on your LAN
- Network access to port `9283`
- `curl` command-line tool installed

## Available API Endpoints

| Endpoint | Description | Documentation |
|----------|-------------|---------------|
| `/remote_bar_order` | Power on/off control | [power-on.md](power-on.md), [power-off.md](power-off.md) |
| `/volume` | Set volume level (0-100) | [set-volume.md](set-volume.md) |
| `/input.mode.set` | Switch input sources | [set-input-source.md](set-input-source.md) |
| `/get_current_state` | Poll current device state | [get-state.md](get-state.md) |

## Quick Start

Replace `192.168.0.102` in all examples with your device's actual IP address.

### Power Control

```bash
# Turn on
curl -X POST http://192.168.0.102:9283/remote_bar_order \
  -H "Content-Type: application/json" \
  -d '{"barControl": "remote_bar_order_sleep_on_off", "value": "1"}'

# Turn off
curl -X POST http://192.168.0.102:9283/remote_bar_order \
  -H "Content-Type: application/json" \
  -d '{"barControl": "remote_bar_order_sleep_on_off", "value": "-1"}'
```

### Volume Control

```bash
# Set volume to 50%
curl -X POST http://192.168.0.102:9283/volume \
  -H "Content-Type: application/json" \
  -d '{"volumeType": "volume_set", "volumeValue": 50}'
```

### Input Source Selection

```bash
# Switch to LINE IN (funcMode: 1)
curl -X POST http://192.168.0.102:9283/input.mode.set \
  -H "Content-Type: application/json" \
  -d '{"funcMode": 1}'
```

**Available inputs:**
- `0` = STREAMER
- `1` = LINE IN
- `2` = OPTICAL IN
- `3` = eARC IN
- `4` = USB IN
- `5` = AES/EBU IN

### Get Current State

```bash
curl -X POST http://192.168.0.102:9283/get_current_state \
  -H "Content-Type: application/json" \
  -d '{}'
```

## API Limitations

- Volume slider does not reflect manual changes made on the amplifier itself (API limitation)
- Power state and input source do sync correctly in both directions
- No media playback metadata or album art available

## Tested With

- HiFi Rose RS520 Firmware: 5.9.02

## Related Documentation

See the [hifirose_streamer](../hifirose_streamer/) directory for the complete Home Assistant integration implementation.
