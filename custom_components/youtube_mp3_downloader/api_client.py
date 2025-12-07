"""API client for YouTube MP3 Downloader."""
import aiohttp
import logging
from typing import Any, Dict, Optional

from .const import (
    API_CONFIG,
    API_DOWNLOAD,
    API_DOWNLOADS,
    API_FILES,
    API_HEALTH,
)

_LOGGER = logging.getLogger(__name__)


class YouTubeMp3DownloaderAPI:
    """API client for YouTube MP3 Downloader."""

    def __init__(self, host: str, port: int = 8000, verify_ssl: bool = False):
        """Initialize the API client."""
        self.host = host
        self.port = port
        self.verify_ssl = verify_ssl
        self.base_url = f"http://{host}:{port}"
        self.session: Optional[aiohttp.ClientSession] = None

    async def async_init_session(self) -> None:
        """Initialize aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def async_close_session(self) -> None:
        """Close aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def async_health_check(self) -> bool:
        """Check if the service is healthy."""
        try:
            await self.async_init_session()
            url = f"{self.base_url}{API_HEALTH}"
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                return resp.status == 200
        except Exception as err:
            _LOGGER.error("Health check failed: %s", err)
            return False

    async def async_get_config(self) -> Dict[str, Any]:
        """Get the current configuration."""
        try:
            await self.async_init_session()
            url = f"{self.base_url}{API_CONFIG}"
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    return await resp.json()
                _LOGGER.error("Failed to get config: %s", resp.status)
                return {}
        except Exception as err:
            _LOGGER.error("Error getting config: %s", err)
            return {}

    async def async_download_video(
        self, url: str, custom_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Start downloading a video."""
        try:
            await self.async_init_session()
            api_url = f"{self.base_url}{API_DOWNLOAD}"
            payload = {"url": url}
            if custom_name:
                payload["custom_name"] = custom_name
            
            async with self.session.post(
                api_url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                _LOGGER.error("Download request failed: %s", resp.status)
                return {"error": f"HTTP {resp.status}"}
        except Exception as err:
            _LOGGER.error("Error starting download: %s", err)
            return {"error": str(err)}

    async def async_get_downloads(self) -> Dict[str, Any]:
        """Get all downloads."""
        try:
            await self.async_init_session()
            url = f"{self.base_url}{API_DOWNLOADS}"
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    return await resp.json()
                _LOGGER.error("Failed to get downloads: %s", resp.status)
                return {}
        except Exception as err:
            _LOGGER.error("Error getting downloads: %s", err)
            return {}

    async def async_get_download_status(self, download_id: str) -> Dict[str, Any]:
        """Get status of a specific download."""
        try:
            await self.async_init_session()
            url = f"{self.base_url}{API_DOWNLOADS}/{download_id}"
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    return await resp.json()
                _LOGGER.error("Failed to get download status: %s", resp.status)
                return {}
        except Exception as err:
            _LOGGER.error("Error getting download status: %s", err)
            return {}

    async def async_get_files(self) -> list:
        """Get all downloaded files."""
        try:
            await self.async_init_session()
            url = f"{self.base_url}{API_FILES}"
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    return await resp.json()
                _LOGGER.error("Failed to get files: %s", resp.status)
                return []
        except Exception as err:
            _LOGGER.error("Error getting files: %s", err)
            return []
