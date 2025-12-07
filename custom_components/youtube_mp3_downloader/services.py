"""Services for YouTube MP3 Downloader."""
import logging

from homeassistant.core import HomeAssistant, ServiceCall

from .api_client import YouTubeMp3DownloaderAPI
from .const import ATTR_CUSTOM_NAME, ATTR_DOWNLOAD_ID, ATTR_URL, DOMAIN, SERVICE_DOWNLOAD, SERVICE_GET_FILES, SERVICE_GET_STATUS

_LOGGER = logging.getLogger(__name__)


def get_api(hass: HomeAssistant) -> YouTubeMp3DownloaderAPI:
    """Get API instance from first config entry."""
    if not hass.data.get(DOMAIN):
        raise ValueError("No YouTube MP3 Downloader entries configured")
    
    entry_id = list(hass.data[DOMAIN].keys())[0]
    config = hass.data[DOMAIN][entry_id]
    
    return YouTubeMp3DownloaderAPI(
        config["host"],
        config["port"],
        config.get("verify_ssl", False)
    )


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services."""

    async def handle_download_video(call: ServiceCall) -> None:
        """Download video service."""
        try:
            api = get_api(hass)
            await api.async_download_video(
                call.data.get(ATTR_URL),
                call.data.get(ATTR_CUSTOM_NAME)
            )
            _LOGGER.info(f"Download started: {call.data.get(ATTR_URL)}")
        except Exception as e:
            _LOGGER.error(f"Download error: {e}")

    async def handle_get_status(call: ServiceCall) -> None:
        """Get download status service."""
        try:
            api = get_api(hass)
            await api.async_get_download_status(call.data.get(ATTR_DOWNLOAD_ID))
            _LOGGER.info(f"Status check: {call.data.get(ATTR_DOWNLOAD_ID)}")
        except Exception as e:
            _LOGGER.error(f"Status error: {e}")

    async def handle_get_files(call: ServiceCall) -> None:
        """Get files list service."""
        try:
            api = get_api(hass)
            files = await api.async_get_files()
            _LOGGER.info(f"Retrieved {len(files)} files")
        except Exception as e:
            _LOGGER.error(f"Files error: {e}")

    # Register all services
    hass.services.async_register(DOMAIN, SERVICE_DOWNLOAD, handle_download_video)
    hass.services.async_register(DOMAIN, SERVICE_GET_STATUS, handle_get_status)
    hass.services.async_register(DOMAIN, SERVICE_GET_FILES, handle_get_files)
    
    _LOGGER.info("Services registered")