# Home Assistant YouTube MP3 Downloader Integration

A Home Assistant integration for the YouTube MP3 Downloader service running on your NAS. Control downloads, monitor progress, and manage your MP3 collection directly from Home Assistant.

## Features

- 🎬 **Download Control** - Start YouTube downloads from Home Assistant
- 📊 **Monitoring** - Track download progress and file counts
- 🔄 **Real-time Updates** - Sensors show active downloads and total files
- 🎵 **Service Integration** - Call services to download, check status, and list files
- 🏠 **Local Network** - Works seamlessly with your home network setup. Follow steps to setup the backend system https://github.com/kunwarmahen/yt-dl-app

## Installation

### HACS Installation (Recommended)

1. Open HACS in Home Assistant
2. Click the three-dot menu → Custom repositories
3. Add repository: `https://github.com/yourusername/hacs`
4. Select category: Integration
5. Search for "YouTube MP3 Downloader" and install
6. Restart Home Assistant

### Manual Installation

1. Copy `custom_components/youtube_mp3_downloader` to your `custom_components` folder
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Create Integration
4. Search for "YouTube MP3 Downloader"

## Configuration

### Initial Setup

1. In Home Assistant, go to Settings → Devices & Services
2. Click "Create Integration"
3. Search for "YouTube MP3 Downloader"
4. Enter your NAS details:
   - **Host**: IP address or hostname of your NAS (e.g., `192.168.1.100`)
   - **Port**: API port (default: `8000`)
   - **Verify SSL**: Disable for local network (default: off)

### Example YAML Configuration

You can also configure via YAML:

```yaml
youtube_mp3_downloader:
  host: 192.168.1.100
  port: 8000
  verify_ssl: false
```

## Services

### Download Video

Start downloading a YouTube video:

```yaml
service: youtube_mp3_downloader.download_video
data:
  entry_id: "your_entry_id"
  url: "https://www.youtube.com/watch?v=VIDEO_ID"
  custom_name: "My Song Name"  # Optional
```

### Get Download Status

Check status of a specific download:

```yaml
service: youtube_mp3_downloader.get_download_status
data:
  entry_id: "your_entry_id"
  download_id: "dl_1234567890"
```

### Get Files

Retrieve list of all downloaded files:

```yaml
service: youtube_mp3_downloader.get_files
data:
  entry_id: "your_entry_id"
```

## Sensors

The integration provides two sensors:

- **Active Downloads** (`sensor.youtube_mp3_downloader_active_downloads`)
  - Shows number of downloads currently in progress
  - Updates every 30 seconds
  
- **Total Files** (`sensor.youtube_mp3_downloader_total_files`)
  - Shows total number of downloaded MP3 files
  - Updates every 30 seconds

### Using Sensors in Automations

```yaml
automation:
  - alias: "Notify when downloads complete"
    trigger:
      platform: state
      entity_id: sensor.youtube_mp3_downloader_active_downloads
      to: "0"
    action:
      service: notify.persistent_notification
      data:
        message: "All YouTube downloads completed!"
        title: "Downloads Complete"
```

## Automations & Scripts

### Automation Example

Download a video at a specific time:

```yaml
automation:
  - alias: "Download Morning Podcast"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      service: youtube_mp3_downloader.download_video
      data:
        entry_id: "your_entry_id"
        url: "https://www.youtube.com/watch?v=PODCAST_ID"
        custom_name: "Morning Podcast"
```

### Script Example

Create a reusable script:

```yaml
script:
  download_youtube_audio:
    description: "Download YouTube video as MP3"
    fields:
      url:
        description: "YouTube video URL"
        example: "https://www.youtube.com/watch?v=VIDEO_ID"
      name:
        description: "Custom file name (optional)"
        example: "My Song"
    sequence:
      - service: youtube_mp3_downloader.download_video
        data:
          entry_id: "your_entry_id"
          url: "{{ url }}"
          custom_name: "{{ name }}"
```

Then call it from UI:
```yaml
service: script.download_youtube_audio
data:
  url: "https://www.youtube.com/watch?v=VIDEO_ID"
  name: "Song Name"
```

## Events

The integration fires events that can be used in automations:

- **youtube_mp3_downloader_download_started**
  - Fired when a download is queued
  - Data: `download_id`, `url`, `custom_name`

- **youtube_mp3_downloader_status_updated**
  - Fired when status changes
  - Data: `download_id`, `status`, `progress`, `title`

- **youtube_mp3_downloader_files_retrieved**
  - Fired when files are retrieved
  - Data: `count`, `files`

### Event Automation Example

```yaml
automation:
  - alias: "Log download started"
    trigger:
      platform: event
      event_type: youtube_mp3_downloader_download_started
    action:
      service: logger.log
      data:
        message: "Download started: {{ trigger.event.data.url }}"
        level: info
```

## Troubleshooting

### Integration Won't Add

1. Verify your YouTube MP3 Downloader service is running:
   ```bash
   docker-compose ps
   ```

2. Check that your NAS is accessible:
   ```bash
   ping <your-nas-ip>
   ```

3. Verify the API is responding:
   ```bash
   curl http://<your-nas-ip>:8000/health
   ```

### Sensors Not Updating

1. Check the Home Assistant logs for errors
2. Verify the integration is configured correctly
3. Try reloading the integration:
   - Settings → Devices & Services
   - Find "YouTube MP3 Downloader"
   - Click the three-dot menu → Reload

### Download Service Fails

1. Verify the YouTube URL is valid
2. Check that the NAS has internet connectivity
3. Check download logs on the NAS:
   ```bash
   docker-compose logs backend
   ```

## Advanced Configuration

### Multiple YouTube Downloader Instances

You can add multiple instances of the integration if you have multiple downloaders running:

1. Settings → Devices & Services → Create Integration
2. Search for "YouTube MP3 Downloader"
3. Enter different host/port for each instance
4. Each instance will have separate sensors and services

### Custom Update Interval

To change how often sensors update, edit `sensor.py` and change `SCAN_INTERVAL`:

```python
SCAN_INTERVAL = timedelta(seconds=60)  # Update every 60 seconds instead of 30
```

## Requirements

- Home Assistant 2024.1.0 or later
- YouTube MP3 Downloader service running on your NAS
- HACS (for easy installation)

## Links

- **YouTube MP3 Downloader**: [GitHub Repository](https://github.com/yourusername/youtube-downloader)
- **Home Assistant Documentation**: [Custom Integration Development](https://developers.home-assistant.io/)
- **HACS**: [Home Assistant Community Store](https://hacs.xyz/)

## Support

Having issues? 

1. Check the [troubleshooting](#troubleshooting) section
2. Review Home Assistant logs (Settings → System → Logs)
3. Check YouTube MP3 Downloader logs on your NAS
4. Open an issue on GitHub

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made for Home Assistant and home networks 🏠
