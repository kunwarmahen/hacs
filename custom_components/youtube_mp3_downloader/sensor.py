"""Sensor platform for YouTube MP3 Downloader."""
import logging
from typing import Optional

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from datetime import timedelta

from .api_client import YouTubeMp3DownloaderAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors from a config entry."""
    config = hass.data[DOMAIN][entry.entry_id]
    
    api = YouTubeMp3DownloaderAPI(
        config["host"],
        config["port"],
        config["verify_ssl"],
    )

    async def async_update_data():
        """Update sensor data."""
        downloads = await api.async_get_downloads()
        files = await api.async_get_files()
        
        return {
            "downloads": downloads,
            "files": files,
            "download_count": len([d for d in downloads.values() if d.get("status") in ["downloading", "queued"]]),
            "total_files": len(files),
        }

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="youtube_mp3_downloader",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()

    sensors = [
        YouTubeMp3DownloadCountSensor(coordinator, entry),
        YouTubeMp3FilesCountSensor(coordinator, entry),
    ]

    async_add_entities(sensors)


class YouTubeMp3SensorBase(CoordinatorEntity, SensorEntity):
    """Base class for YouTube MP3 Downloader sensors."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_has_entity_name = True

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": "YouTube MP3 Downloader",
            "manufacturer": "Home Assistant",
            "model": "YouTube MP3 Downloader",
        }


class YouTubeMp3DownloadCountSensor(YouTubeMp3SensorBase):
    """Sensor for active download count."""

    _attr_name = "Active Downloads"
    _attr_unique_id = "youtube_mp3_active_downloads"
    _attr_icon = "mdi:download"
    _attr_native_unit_of_measurement = "downloads"

    @property
    def native_value(self) -> Optional[int]:
        """Return the active download count."""
        if self.coordinator.data:
            return self.coordinator.data.get("download_count", 0)
        return None


class YouTubeMp3FilesCountSensor(YouTubeMp3SensorBase):
    """Sensor for total files count."""

    _attr_name = "Total Files"
    _attr_unique_id = "youtube_mp3_total_files"
    _attr_icon = "mdi:music"
    _attr_native_unit_of_measurement = "files"

    @property
    def native_value(self) -> Optional[int]:
        """Return the total files count."""
        if self.coordinator.data:
            return self.coordinator.data.get("total_files", 0)
        return None
