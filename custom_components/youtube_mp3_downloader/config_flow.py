"""Config flow for YouTube MP3 Downloader."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
import aiohttp

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class YouTubeMp3DownloaderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for YouTube MP3 Downloader."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            # Validate the connection
            try:
                await self._test_connection(
                    user_input.get("host"), 
                    user_input.get("port", 8000)
                )
            except Exception as err:
                _LOGGER.error("Error testing connection: %s", err)
                errors["base"] = "cannot_connect"
            
            if not errors:
                await self.async_set_unique_id(f"{user_input['host']}_{user_input['port']}")
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=f"YouTube MP3 ({user_input['host']})",
                    data=user_input,
                )

        data_schema = vol.Schema({
            vol.Required("host", description="Host"): str,
            vol.Optional("port", default=8000, description="Port"): int,
            vol.Optional("verify_ssl", default=False): bool,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={},
        )

    async def _test_connection(self, host: str, port: int) -> bool:
        """Test connection to the YouTube MP3 downloader service."""
        url = f"http://{host}:{port}/health"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    return resp.status == 200
        except Exception as err:
            _LOGGER.error("Connection test failed: %s", err)
            raise


class YouTubeMp3DownloaderOptionsFlow(config_entries.OptionsFlow):
    """Handle options for YouTube MP3 Downloader."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the options step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional(
                "auto_cleanup",
                default=self.config_entry.options.get("auto_cleanup", False),
            ): bool,
            vol.Optional(
                "max_concurrent",
                default=self.config_entry.options.get("max_concurrent", 3),
            ): int,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )


@callback
def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> YouTubeMp3DownloaderOptionsFlow:
    """Get the options flow for this integration."""
    return YouTubeMp3DownloaderOptionsFlow(config_entry)
