# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a Home Assistant custom integration for HiFi Rose Streamer devices, plus complete API documentation. The integration provides local control (no cloud dependency) of HiFi Rose audio devices via their HTTP API on port 9283.

## Repository Structure

- **`hifirose_streamer/`**: Home Assistant custom integration (domain: `hifirose_streamer`)
  - Deploy by copying entire directory to `config/custom_components/`
  - Entry point: `__init__.py` (setup/unload lifecycle)
  - Config flow: `config_flow.py` (UI-based configuration)
  - Media player: `media_player.py` (HiFiRoseMediaPlayer entity)
  - Constants: `const.py` (DOMAIN, defaults, SSL configs)

- **`example-curl-requests/`**: API documentation with curl examples
  - Complete reference for all endpoints used by the integration
  - Useful for testing device connectivity outside Home Assistant

## Installation & Testing

### Deploy to Home Assistant
```bash
# Copy integration to Home Assistant custom_components
cp -r hifirose_streamer/ /config/custom_components/

# Restart Home Assistant, then add via:
# Settings → Devices & Services → Add Integration → "HiFi Rose Streamer"
```

### Test Device API Directly
```bash
# Verify device connectivity (replace IP)
curl -X POST http://192.168.0.102:9283/get_current_state \
  -H "Content-Type: application/json" \
  -d '{}'

# Set volume to 30
curl -X POST http://192.168.0.102:9283/volume \
  -H "Content-Type: application/json" \
  -d '{"volumeType": "volume_set", "volumeValue": 30}'
```

## Integration Architecture

### Entry Point Flow
1. `__init__.py::async_setup_entry()` - Stores config in `hass.data[DOMAIN]`
2. Forwards setup to `media_player` platform
3. `media_player.py::async_setup_entry()` - Creates HiFiRoseMediaPlayer entity

### Configuration Flow (`config_flow.py`)
- Uses `voluptuous` for schema validation
- Tests connection via `_test_connection()` before accepting config
- Stores: host, port (default 9283), SSL settings, name
- Sets unique_id to host IP (prevents duplicate entries)

### Media Player Entity (`media_player.py`)
**Key class:** `HiFiRoseMediaPlayer(MediaPlayerEntity)`

**State Management:**
- Polls device every 30 seconds via `async_update()` (Home Assistant default)
- Calls `/get_current_state` endpoint to sync volume, power, input source
- Uses `async_add_executor_job()` to run synchronous `requests` calls

**API Communication:**
- All commands go through `_send_command(endpoint, payload)` method
- 5-second timeout on all HTTP requests
- SSL verification configurable via `verify_ssl` parameter

**Input Sources:**
- Defined in `INPUT_SOURCES` dict (STREAMER=0, LINE IN=1, OPTICAL IN=2, eARC IN=3, USB IN=4, AES/EBU IN=5)
- `REVERSE_INPUT_SOURCES` maps funcMode integers back to names
- Source parsing from API: extracts `funcMode:N` from `tempArr` field

**Supported Features:**
- `TURN_ON` / `TURN_OFF` - via `/remote_bar_order` endpoint
- `VOLUME_SET` - via `/volume` endpoint (0-100 scale, converted from HA's 0.0-1.0)
- `SELECT_SOURCE` - via `/input.mode.set` endpoint

### Custom Services (`__init__.py`)

The integration registers 7 custom services in the `hifirose_streamer` domain for easier automation scripting:

**Mute Toggle:**
- `hifirose_streamer.mute` - Toggles mute by setting volume to 0 (mute) or restoring previous volume (unmute)
- Tracks mute state in `_is_muted` and stores last volume in `_last_volume` (media_player.py:83-84)
- Called via `async_mute_toggle()` method (media_player.py:150-157)

**Quick Source Switches:**
- `hifirose_streamer.switch_to_streamer` - Switch to STREAMER (funcMode 0)
- `hifirose_streamer.switch_to_line_in` - Switch to LINE IN (funcMode 1)
- `hifirose_streamer.switch_to_optical` - Switch to OPTICAL IN (funcMode 2)
- `hifirose_streamer.switch_to_earc` - Switch to eARC IN (funcMode 3)
- `hifirose_streamer.switch_to_usb` - Switch to USB IN (funcMode 4)
- `hifirose_streamer.switch_to_aes_ebu` - Switch to AES/EBU IN (funcMode 5)

**Service Registration:**
- Services registered in `async_setup_entry()` (__init__.py:53-97)
- Services unregistered when last integration entry removed (__init__.py:110-116)
- Service schemas defined in `services.yaml` for Home Assistant UI

**Automation Examples:**
```yaml
# Mute toggle in automation
automation:
  - alias: "Mute on doorbell"
    trigger:
      - platform: state
        entity_id: binary_sensor.doorbell
        to: "on"
    action:
      - service: hifirose_streamer.mute
        target:
          entity_id: media_player.hifi_rose_streamer

# Quick source switch
  - alias: "Switch to TV at night"
    trigger:
      - platform: time
        at: "20:00:00"
    action:
      - service: hifirose_streamer.switch_to_earc
        target:
          entity_id: media_player.hifi_rose_streamer
```

### API Quirks Handled in Code

1. **Volume sync limitation** (`media_player.py:176`)
   - Only updates volume if API returns > 0 (device doesn't report manual changes)
   - See: `if volume is not None and isinstance(volume, (int, float)) and volume > 0:`

2. **Input source parsing** (`media_player.py:179-188`)
   - Source stored in `tempArr` array as string `"funcMode:N"`
   - Code iterates array, splits on `:`, converts to int for mapping

3. **Power state detection** (`media_player.py:167-172`)
   - Checks both `isPlaying` and `isPowerOn` flags
   - Device considered ON if either flag is true

## Network Requirements

- Device must have static IP address (configured via router DHCP reservation)
- Port 9283 must be accessible on LAN
- Supports HTTP and HTTPS (configurable during setup)
- SSL certificate verification can be disabled for self-signed certs

## Known Limitations

- Volume changes made directly on device hardware are not reflected in Home Assistant (API limitation)
- Power state and input source sync correctly bidirectionally
- No media playback metadata or album art available from API
- No media transport controls (play/pause/next/previous)

## Tested With

- Home Assistant Core: 2024.x+
- HiFi Rose Firmware: 5.9.02 (RS520 model)
