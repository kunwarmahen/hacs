"""YouTube MP3 Downloader integration for Home Assistant."""
import asyncio
import logging
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery

DOMAIN: Final = "youtube_mp3_downloader"
PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the YouTube MP3 Downloader component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up YouTube MP3 Downloader from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Store the config
    hass.data[DOMAIN][entry.entry_id] = {
        "host": entry.data.get("host"),
        "port": entry.data.get("port", 8000),
        "verify_ssl": entry.data.get("verify_ssl", False),
    }
    
    # Set up services
    from .services import async_setup_services
    await async_setup_services(hass)
    
    # Forward the setup to the platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    
    return True
    
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)