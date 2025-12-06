"""Media player platform for HiFi Rose Streamer."""
from __future__ import annotations

import logging
from typing import Any

import requests

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_PORT,
    CONF_USE_SSL,
    CONF_VERIFY_SSL,
    DEFAULT_USE_SSL,
    DEFAULT_VERIFY_SSL,
)

_LOGGER = logging.getLogger(__name__)

# Input source mapping
INPUT_SOURCES = {
    "STREAMER": 0,
    "LINE IN": 1,
    "OPTICAL IN": 2,
    "eARC IN": 3,
    "USB IN": 4,
    "AES/EBU IN": 5,
}

REVERSE_INPUT_SOURCES = {v: k for k, v in INPUT_SOURCES.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the HiFi Rose Streamer media player."""
    host = config_entry.data[CONF_HOST]
    name = config_entry.data.get("name", DEFAULT_NAME)
    port = config_entry.data.get(CONF_PORT, DEFAULT_PORT)
    use_ssl = config_entry.data.get(CONF_USE_SSL, DEFAULT_USE_SSL)
    verify_ssl = config_entry.data.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL)

    async_add_entities([HiFiRoseMediaPlayer(host, name, port, use_ssl, verify_ssl, config_entry.entry_id)])


class HiFiRoseMediaPlayer(MediaPlayerEntity):
    """Representation of a HiFi Rose Streamer media player."""

    _attr_should_poll = True
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(self, host: str, name: str, port: int, use_ssl: bool, verify_ssl: bool, entry_id: str) -> None:
        """Initialize the media player."""
        self._host = host
        self._port = port
        self._use_ssl = use_ssl
        self._verify_ssl = verify_ssl
        self._protocol = "https" if use_ssl else "http"
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{host.replace('.', '_')}"
        self._attr_state = MediaPlayerState.OFF
        self._attr_volume_level = 0.5
        self._attr_source = None
        self._attr_source_list = list(INPUT_SOURCES.keys())
        self._entry_id = entry_id
        self._is_muted = False
        self._last_volume = 0.5

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._attr_name,
            "manufacturer": "HiFi Rose",
            "model": "Streamer",
        }

    async def async_turn_on(self) -> None:
        """Turn on the media player."""
        await self._send_command(
            "/remote_bar_order",
            {
                "barControl": "remote_bar_order_sleep_on_off",
                "value": "1",
            },
        )
        self._attr_state = MediaPlayerState.ON
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Turn off the media player."""
        await self._send_command(
            "/remote_bar_order",
            {
                "barControl": "remote_bar_order_sleep_on_off",
                "value": "-1",
            },
        )
        self._attr_state = MediaPlayerState.OFF
        self.async_write_ha_state()

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level (0.0 to 1.0)."""
        volume_value = int(volume * 100)
        await self._send_command(
            "/volume",
            {
                "volumeType": "volume_set",
                "volumeValue": volume_value,
            },
        )
        self._attr_volume_level = volume
        # Store non-zero volume for unmute restoration
        if volume > 0:
            self._last_volume = volume
            self._is_muted = False
        else:
            self._is_muted = True
        self.async_write_ha_state()

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        if source in INPUT_SOURCES:
            func_mode = INPUT_SOURCES[source]
            await self._send_command(
                "/input.mode.set",
                {"funcMode": func_mode},
            )
            self._attr_source = source
            self.async_write_ha_state()

    async def async_mute_toggle(self) -> None:
        """Toggle mute status."""
        if self._is_muted:
            # Unmute: restore previous volume
            await self.async_set_volume_level(self._last_volume)
        else:
            # Mute: set volume to 0
            await self.async_set_volume_level(0.0)

    async def async_update(self) -> None:
        """Update the state of the media player."""
        try:
            response = await self.hass.async_add_executor_job(
                self._get_state
            )
            data = response.get("data", {})

            # Update power state
            is_playing = data.get("isPlaying", False)
            is_power_on = data.get("isPowerOn", False)
            self._attr_state = (
                MediaPlayerState.ON if (is_playing or is_power_on) else MediaPlayerState.OFF
            )

            # Update volume (only if valid)
            volume = data.get("volume")
            if volume is not None and isinstance(volume, (int, float)) and volume > 0:
                self._attr_volume_level = int(volume) / 100.0

            # Update input source
            temp_arr = data.get("tempArr", [])
            for entry in temp_arr:
                if isinstance(entry, str) and entry.startswith("funcMode:"):
                    try:
                        func_mode = int(entry.split(":")[1])
                        self._attr_source = REVERSE_INPUT_SOURCES.get(func_mode)
                    except (ValueError, IndexError):
                        pass
                    break

        except Exception as err:
            _LOGGER.error("Error updating HiFi Rose Streamer: %s", err)
            self._attr_state = MediaPlayerState.OFF

    async def _send_command(self, endpoint: str, payload: dict[str, Any]) -> None:
        """Send a command to the device."""
        def _post():
            url = f"{self._protocol}://{self._host}:{self._port}{endpoint}"
            return requests.post(url, json=payload, timeout=5, verify=self._verify_ssl)

        try:
            await self.hass.async_add_executor_job(_post)
        except Exception as err:
            _LOGGER.error("Failed to send command to %s: %s", endpoint, err)

    def _get_state(self) -> dict[str, Any]:
        """Get the current state from the device."""
        url = f"{self._protocol}://{self._host}:{self._port}/get_current_state"
        response = requests.post(url, json={}, timeout=5, verify=self._verify_ssl)
        response.raise_for_status()
        return response.json()
