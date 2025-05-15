from __future__ import annotations

import dataclasses
import logging
from typing import Any

from bleak import BleakError

from homeassistant.components import bluetooth
from homeassistant.components.bluetooth import (
    BluetoothServiceInfo,
    async_discovered_service_info,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_ADDRESS


from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

import voluptuous as vol

class BasestationConfigFlow(ConfigFlow, domain=DOMAIN):
    """Initial config flow for adding a Basestation"""
    
    VERSION = 1
    MINOR_VERSION = 2

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfo
    ) -> ConfigFlowResult:
        """Handle the bluetooth discovery step."""
        _LOGGER.debug("Discovered BT device: %s", discovery_info)
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=discovery_info.name, data={})


    
    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            address = user_input["mac"]
            name = user_input["name"]
            await self.async_set_unique_id(address, raise_on_progress=False)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=name, data={})


        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({vol.Required("mac"): str, vol.Required("name"): str})
        )
