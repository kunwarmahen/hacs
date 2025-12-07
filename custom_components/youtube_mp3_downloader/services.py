"""Services for YouTube MP3 Downloader."""
import logging
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall
import voluptuous as vol

from .api_client import YouTubeMp3DownloaderAPI
from .const import (
    ATTR_CUSTOM_NAME,
    ATTR_DOWNLOAD_ID,
    ATTR_FILES,
    ATTR_PROGRESS,
    ATTR_STATUS,
    ATTR_URL,
    DOMAIN,
    SERVICE_DOWNLOAD,
    SERVICE_GET_FILES,
    SERVICE_GET_STATUS,
)

_LOGGER = logging.getLogger(__name__)

# Service schemas
DOWNLOAD_SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_URL): cv.string,
    vol.Optional(ATTR_CUSTOM_NAME): cv.string,
})

GET_STATUS_SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_DOWNLOAD_ID): cv.string,
})


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for YouTube MP3 Downloader."""

    async def handle_download_video(call: ServiceCall) -> None:
        """Handle download video service call."""
        entry_id = call.data.get("entry_id")
        url = call.data.get(ATTR_URL)
        custom_name = call.data.get(ATTR_CUSTOM_NAME)

        if not entry_id or entry_id not in hass.data[DOMAIN]:
            _LOGGER.error(f"Invalid entry_id: {entry_id}")
            return

        config = hass.data[DOMAIN][entry_id]
        api = YouTubeMp3DownloaderAPI(config["host"], config["port"], config["verify_ssl"])

        result = await api.async_download_video(url, custom_name)
        
        _LOGGER.info(f"Download started: {result}")
        
        # Fire event with result
        hass.bus.async_fire(
            f"{DOMAIN}_download_started",
            {
                "download_id": result.get("download_id"),
                "url": url,
                "custom_name": custom_name,
            },
        )

    async def handle_get_status(call: ServiceCall) -> None:
        """Handle get download status service call."""
        entry_id = call.data.get("entry_id")
        download_id = call.data.get(ATTR_DOWNLOAD_ID)

        if not entry_id or entry_id not in hass.data[DOMAIN]:
            _LOGGER.error(f"Invalid entry_id: {entry_id}")
            return

        config = hass.data[DOMAIN][entry_id]
        api = YouTubeMp3DownloaderAPI(config["host"], config["port"], config["verify_ssl"])

        status = await api.async_get_download_status(download_id)
        
        _LOGGER.info(f"Download status: {status}")
        
        # Fire event with status
        hass.bus.async_fire(
            f"{DOMAIN}_status_updated",
            {
                "download_id": download_id,
                "status": status.get("status"),
                "progress": status.get("progress"),
                "title": status.get("title"),
            },
        )

    async def handle_get_files(call: ServiceCall) -> None:
        """Handle get files service call."""
        entry_id = call.data.get("entry_id")

        if not entry_id or entry_id not in hass.data[DOMAIN]:
            _LOGGER.error(f"Invalid entry_id: {entry_id}")
            return

        config = hass.data[DOMAIN][entry_id]
        api = YouTubeMp3DownloaderAPI(config["host"], config["port"], config["verify_ssl"])

        files = await api.async_get_files()
        
        _LOGGER.info(f"Files retrieved: {len(files)} files")
        
        # Fire event with files
        hass.bus.async_fire(
            f"{DOMAIN}_files_retrieved",
            {
                "count": len(files),
                "files": files,
            },
        )

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_DOWNLOAD,
        handle_download_video,
        schema=DOWNLOAD_SERVICE_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_STATUS,
        handle_get_status,
        schema=GET_STATUS_SERVICE_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_FILES,
        handle_get_files,
    )

    _LOGGER.info("Services registered for YouTube MP3 Downloader")


# Import validation
import homeassistant.helpers.config_validation as cv
