"""The HiFi Rose Streamer integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

PLATFORMS = ["media_player"]

# Service names
SERVICE_MUTE = "mute"
SERVICE_SWITCH_TO_STREAMER = "switch_to_streamer"
SERVICE_SWITCH_TO_LINE_IN = "switch_to_line_in"
SERVICE_SWITCH_TO_OPTICAL = "switch_to_optical"
SERVICE_SWITCH_TO_EARC = "switch_to_earc"
SERVICE_SWITCH_TO_USB = "switch_to_usb"
SERVICE_SWITCH_TO_AES_EBU = "switch_to_aes_ebu"

# Service schemas
SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.entity_ids,
})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HiFi Rose Streamer from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def async_service_mute(call: ServiceCall) -> None:
        """Handle mute service call."""
        entity_ids = call.data[ATTR_ENTITY_ID]
        for entity_id in entity_ids:
            if entity := hass.data["entity_components"]["media_player"].get_entity(entity_id):
                if hasattr(entity, "async_mute_toggle"):
                    await entity.async_mute_toggle()

    async def async_service_switch_source(call: ServiceCall, source: str) -> None:
        """Handle input source switch service call."""
        entity_ids = call.data[ATTR_ENTITY_ID]
        for entity_id in entity_ids:
            if entity := hass.data["entity_components"]["media_player"].get_entity(entity_id):
                if hasattr(entity, "async_select_source"):
                    await entity.async_select_source(source)

    # Register mute service
    hass.services.async_register(
        DOMAIN,
        SERVICE_MUTE,
        async_service_mute,
        schema=SERVICE_SCHEMA,
    )

    # Register source switch services
    hass.services.async_register(
        DOMAIN,
        SERVICE_SWITCH_TO_STREAMER,
        lambda call: async_service_switch_source(call, "STREAMER"),
        schema=SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SWITCH_TO_LINE_IN,
        lambda call: async_service_switch_source(call, "LINE IN"),
        schema=SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SWITCH_TO_OPTICAL,
        lambda call: async_service_switch_source(call, "OPTICAL IN"),
        schema=SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SWITCH_TO_EARC,
        lambda call: async_service_switch_source(call, "eARC IN"),
        schema=SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SWITCH_TO_USB,
        lambda call: async_service_switch_source(call, "USB IN"),
        schema=SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SWITCH_TO_AES_EBU,
        lambda call: async_service_switch_source(call, "AES/EBU IN"),
        schema=SERVICE_SCHEMA,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

        # Unregister services only if this is the last entry
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, SERVICE_MUTE)
            hass.services.async_remove(DOMAIN, SERVICE_SWITCH_TO_STREAMER)
            hass.services.async_remove(DOMAIN, SERVICE_SWITCH_TO_LINE_IN)
            hass.services.async_remove(DOMAIN, SERVICE_SWITCH_TO_OPTICAL)
            hass.services.async_remove(DOMAIN, SERVICE_SWITCH_TO_EARC)
            hass.services.async_remove(DOMAIN, SERVICE_SWITCH_TO_USB)
            hass.services.async_remove(DOMAIN, SERVICE_SWITCH_TO_AES_EBU)

    return unload_ok
