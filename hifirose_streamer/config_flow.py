"""Config flow for HiFi Rose Streamer integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
import requests

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.data_entry_flow import FlowResult

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


class HiFiRoseConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HiFi Rose Streamer."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            name = user_input.get(CONF_NAME, DEFAULT_NAME)
            port = user_input.get(CONF_PORT, DEFAULT_PORT)
            use_ssl = user_input.get(CONF_USE_SSL, DEFAULT_USE_SSL)
            verify_ssl = user_input.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL)

            # Test connection
            try:
                await self.hass.async_add_executor_job(
                    self._test_connection, host, port, use_ssl, verify_ssl
                )
            except Exception as err:
                _LOGGER.error("Error connecting to HiFi Rose Streamer: %s", err)
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_HOST: host,
                        CONF_NAME: name,
                        CONF_PORT: port,
                        CONF_USE_SSL: use_ssl,
                        CONF_VERIFY_SSL: verify_ssl,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                    vol.Optional(CONF_USE_SSL, default=DEFAULT_USE_SSL): bool,
                    vol.Optional(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): bool,
                    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                }
            ),
            errors=errors,
        )

    def _test_connection(self, host: str, port: int, use_ssl: bool, verify_ssl: bool) -> None:
        """Test connection to the device."""
        protocol = "https" if use_ssl else "http"
        url = f"{protocol}://{host}:{port}/get_current_state"
        response = requests.post(url, json={}, timeout=5, verify=verify_ssl)
        response.raise_for_status()
