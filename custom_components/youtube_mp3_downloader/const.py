"""Constants for YouTube MP3 Downloader."""
from typing import Final

DOMAIN: Final = "youtube_mp3_downloader"

# API Endpoints
API_HEALTH: Final = "/health"
API_CONFIG: Final = "/config"
API_DOWNLOAD: Final = "/download"
API_DOWNLOADS: Final = "/downloads"
API_DOWNLOADS_ID: Final = "/downloads/{id}"
API_FILES: Final = "/files"

# Service names
SERVICE_DOWNLOAD: Final = "download_video"
SERVICE_GET_STATUS: Final = "get_download_status"
SERVICE_GET_FILES: Final = "get_files"

# Service attributes
ATTR_DOWNLOAD_ID: Final = "download_id"
ATTR_URL: Final = "url"
ATTR_CUSTOM_NAME: Final = "custom_name"
ATTR_STATUS: Final = "status"
ATTR_FILES: Final = "files"
ATTR_PROGRESS: Final = "progress"

# Entity sensor attributes
SENSOR_DOWNLOAD_COUNT: Final = "download_count"
SENSOR_TOTAL_FILES: Final = "total_files"
SENSOR_DISK_USAGE: Final = "disk_usage"
