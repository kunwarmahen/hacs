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


def register_services(hass: HomeAssistant) -> None:
    """Register services (synchronous registration for services.yaml integration)."""

    def handle_download_video(call: ServiceCall) -> None:
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
            # Schedule async function
            hass.async_create_task(api.async_download_video(url, custom_name))
            _LOGGER.info(f"Download started for URL: {url}")
        except Exception as e:
            _LOGGER.error(f"Error downloading video: {e}")

    def handle_get_status(call: ServiceCall) -> None:
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
            hass.async_create_task(api.async_get_download_status(download_id))
            _LOGGER.info(f"Status check initiated for download_id: {download_id}")
        except Exception as e:
            _LOGGER.error(f"Error getting status: {e}")

    def handle_get_files(call: ServiceCall) -> None:
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
            hass.async_create_task(api.async_get_files())
            _LOGGER.info("Files list retrieval initiated")
        except Exception as e:
            _LOGGER.error(f"Error getting files: {e}")

    # Register services using synchronous registration
    # This works with services.yaml for parameter validation
    hass.services.register(
        DOMAIN,
        SERVICE_DOWNLOAD,
        handle_download_video,
    )
    _LOGGER.info(f"✅ Registered service: {DOMAIN}.{SERVICE_DOWNLOAD}")

    hass.services.register(
        DOMAIN,
        SERVICE_GET_STATUS,
        handle_get_status,
    )
    _LOGGER.info(f"✅ Registered service: {DOMAIN}.{SERVICE_GET_STATUS}")

    hass.services.register(
        DOMAIN,
        SERVICE_GET_FILES,
        handle_get_files,
    )
    _LOGGER.info(f"✅ Registered service: {DOMAIN}.{SERVICE_GET_FILES}")

    _LOGGER.info("✅ All services registered for YouTube MP3 Downloader")