"""The basestation integration."""

from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .switch import BasestationSwitchConfigEntry, BasestationSwitch

PLATFORMS: list[Platform] = [Platform.SWITCH]


async def async_setup_entry(
    hass: HomeAssistant, entry: BasestationSwitchConfigEntry
) -> bool:
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: BasestationSwitchConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
