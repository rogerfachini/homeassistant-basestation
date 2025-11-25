"""The basestation switch."""
from __future__ import annotations

from bleak import BleakError
from bleak_retry_connector import (
    establish_connection,
    BleakClientWithServiceCache,
)
from homeassistant.components.switch import SwitchEntity
from homeassistant.components import bluetooth
import asyncio
from homeassistant.config_entries import ConfigEntry
import logging

from .const import (
    PWR_CHARACTERISTIC,
    PWR_ON,
    PWR_STANDBY,
)

_LOGGER = logging.getLogger(__name__)

type BasestationSwitchConfigEntry = ConfigEntry[BasestationSwitch]

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    mac = config.get("mac")
    name = config.get("name")
    add_entities([BasestationSwitch(hass, mac, name)], update_before_add=True)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: BasestationSwitchConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Switches."""
    mac = config_entry.unique_id
    name = config_entry.title

    async_add_entities([BasestationSwitch(hass, mac, name)], update_before_add=True)

    _LOGGER.debug("got switch: %s %s", mac, name)


class BasestationSwitch(SwitchEntity):
    """The basestation switch implementtion."""

    def __init__(self, hass, mac, name):
        """Initialize the switch."""
        self._hass = hass
        self._mac = mac
        self._name = name
        self._is_on = False
        self._is_available = False
        self._attr_unique_id = mac

    @property
    def icon(self):
        """Return the icon."""
        return "mdi:virtual-reality"

    @property
    def should_poll(self):
        return True

    @property
    def available(self):
        """Return the connection status of this switch"""
        return self._is_available

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        asyncio.run(self.async_turn_on())

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        asyncio.run(self.async_turn_off())

    @property
    def name(self):
        """Return the name of the switch."""
        if self._name is not None:
            return self._name

        return "Valve Basestation"

    def update(self):
        """Fetch new state data for the sensor."""
        asyncio.run(self.async_update())

    async def async_turn_on(self):
        device = self.get_ble_device()
        client = await establish_connection(
            BleakClientWithServiceCache,
            device,
            self._name or "Valve Basestation",
            max_attempts=3
        )
        try:
            await client.write_gatt_char(PWR_CHARACTERISTIC, PWR_ON)
        finally:
            await client.disconnect()

    async def async_turn_off(self):
        device = self.get_ble_device()
        client = await establish_connection(
            BleakClientWithServiceCache,
            device,
            self._name or "Valve Basestation",
            max_attempts=3
        )
        try:
            await client.write_gatt_char(PWR_CHARACTERISTIC, PWR_STANDBY)
        finally:
            await client.disconnect()

    async def async_update(self):
        try:
            device = self.get_ble_device()
            client = await establish_connection(
                BleakClientWithServiceCache,
                device,
                self._name or "Valve Basestation",
                max_attempts=3
            )
            try:
                self._is_on = await client.read_gatt_char(PWR_CHARACTERISTIC) != PWR_STANDBY
                self._is_available = True
            finally:
                await client.disconnect()
        except BleakError:
            self._is_on = False
            self._is_available = False
        

    def get_ble_device(self):
        return bluetooth.async_ble_device_from_address(self._hass, str(self._mac))
