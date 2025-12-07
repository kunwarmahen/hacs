"""Services for YouTube MP3 Downloader."""
import logging

from homeassistant.core import HomeAssistant, ServiceCall

from .api_client import YouTubeMp3DownloaderAPI
from .const import (
    ATTR_CUSTOM_NAME,
    ATTR_DOWNLOAD_ID,
    ATTR_URL,
    DOMAIN,
    SERVICE_DOWNLOAD,
    SERVICE_GET_FILES,
    SERVICE_GET_STATUS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for YouTube MP3 Downloader."""

    async def handle_download_video(call: ServiceCall) -> None:
        """Handle download video service call."""
        url = call.data.get(ATTR_URL)
        custom_name = call.data.get(ATTR_CUSTOM_NAME)

        _LOGGER.debug(f"Download service called with URL: {url}")

        # Get the first available entry
        if not hass.data.get(DOMAIN):
            _LOGGER.error("No YouTube MP3 Downloader entries configured")
            return

        # Use the first entry
        entry_id = list(hass.data[DOMAIN].keys())[0]
        config = hass.data[DOMAIN][entry_id]

        try:
            api = YouTubeMp3DownloaderAPI(
                config["host"], config["port"], config.get("verify_ssl", False)
            )
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
        except Exception as e:
            _LOGGER.error(f"Error downloading video: {e}")

    async def handle_get_status(call: ServiceCall) -> None:
        """Handle get download status service call."""
        download_id = call.data.get(ATTR_DOWNLOAD_ID)

        _LOGGER.debug(f"Get status service called for download_id: {download_id}")

        # Get the first available entry
        if not hass.data.get(DOMAIN):
            _LOGGER.error("No YouTube MP3 Downloader entries configured")
            return

        entry_id = list(hass.data[DOMAIN].keys())[0]
        config = hass.data[DOMAIN][entry_id]

        try:
            api = YouTubeMp3DownloaderAPI(
                config["host"], config["port"], config.get("verify_ssl", False)
            )
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
        except Exception as e:
            _LOGGER.error(f"Error getting status: {e}")

    async def handle_get_files(call: ServiceCall) -> None:
        """Handle get files service call."""
        _LOGGER.debug("Get files service called")

        # Get the first available entry
        if not hass.data.get(DOMAIN):
            _LOGGER.error("No YouTube MP3 Downloader entries configured")
            return

        entry_id = list(hass.data[DOMAIN].keys())[0]
        config = hass.data[DOMAIN][entry_id]

        try:
            api = YouTubeMp3DownloaderAPI(
                config["host"], config["port"], config.get("verify_ssl", False)
            )
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
        except Exception as e:
            _LOGGER.error(f"Error getting files: {e}")

    # Register services
    try:
        hass.services.async_register(
            DOMAIN,
            SERVICE_DOWNLOAD,
            handle_download_video,
        )
        _LOGGER.info(f"Registered service: {DOMAIN}.{SERVICE_DOWNLOAD}")
    except Exception as e:
        _LOGGER.error(f"Failed to register download_video service: {e}")

    try:
        hass.services.async_register(
            DOMAIN,
            SERVICE_GET_STATUS,
            handle_get_status,
        )
        _LOGGER.info(f"Registered service: {DOMAIN}.{SERVICE_GET_STATUS}")
    except Exception as e:
        _LOGGER.error(f"Failed to register get_status service: {e}")

    try:
        hass.services.async_register(
            DOMAIN,
            SERVICE_GET_FILES,
            handle_get_files,
        )
        _LOGGER.info(f"Registered service: {DOMAIN}.{SERVICE_GET_FILES}")
    except Exception as e:
        _LOGGER.error(f"Failed to register get_files service: {e}")

    _LOGGER.info("Services setup completed for YouTube MP3 Downloader")