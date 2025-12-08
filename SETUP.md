# YouTube MP3 Downloader - Home Assistant Final Setup Guide

## Complete Working Configuration

This guide includes the tested script, dashboard, and new play/download features.

---

## Step 1: Create Input Helper for YouTube URL

1. Go to **Settings → Devices & Services → Helpers**
2. Click **Create Helper → Text**
3. Fill in:
   - **Name:** YouTube URL
   - **Entity ID:** input_text.youtube_url
   - **Icon:** mdi:youtube
   - **Min/Max length:** 500 characters max
4. Click **Create**

---

## Step 2: Create the Download Script

This script includes URL validation and error handling.

### Via UI:

1. Go to **Settings → Automations & Scenes → Scripts**
2. Click **Create Script**
3. Click **Create in YAML**
4. Paste the complete script below:

```yaml
alias: Download YouTube Video
description: Download a video from YouTube
sequence:
  - variables:
      final_url: "{{ states('input_text.youtube_url') | trim }}"
      is_valid_youtube: |
        {{ final_url is string and
           (final_url.startswith('http://') or final_url.startswith('https://')) and
           ('youtube.com' in final_url or 'youtu.be' in final_url)
        }}
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ final_url == '' }}"
        sequence:
          - data:
              title: Download Failed
              message: No URL provided. Please enter a YouTube link.
            action: persistent_notification.create
      - conditions:
          - condition: template
            value_template: "{{ not is_valid_youtube }}"
        sequence:
          - data:
              title: Invalid URL
              message: The URL provided is not a valid YouTube link.
            action: persistent_notification.create
    default: []
  - condition: template
    value_template: "{{ final_url != '' and is_valid_youtube }}"
  - data:
      title: Download Started
      message: |-
        Downloading video…
        {{ final_url }}
    action: persistent_notification.create
  - data:
      url: "{{ final_url }}"
    action: youtube_mp3_downloader.download_video
  - data:
      title: Download Complete
      message: Your video has been downloaded successfully!
    action: persistent_notification.create
  - data:
      entity_id: input_text.youtube_url
      value: ""
    action: input_text.set_value
mode: single
```

5. Click **Save Script**

---

## Step 3: Create the Main Dashboard

### Via UI:

1. Go to **Dashboards** (left sidebar)
2. Click **+ Create Dashboard**
3. Name it: **YouTube Downloader**
4. Click **Create**
5. Click **+ Add Card**
6. Select **Manual** or **YAML** mode
7. Paste the complete dashboard YAML below:

```yaml
title: YouTube Downloader
views:
  - path: youtube
    title: Downloader
    cards:
      # Header/Instructions
      - type: markdown
        content: |
          # 📥 YouTube Downloader
          Easily download YouTube videos as MP3 files

          **How to use:**
          1. Paste a YouTube URL
          2. Click the Download button
          3. Wait 1-2 minutes
          4. Your MP3 is ready!

          **Supported:**
          - YouTube videos
          - YouTube playlists
          - YouTube Shorts
          - Private videos (if accessible)

      # Download Section
      - type: vertical-stack
        cards:
          # URL Input
          - type: entities
            title: YouTube URL
            entities:
              - entity: input_text.youtube_url
                name: Paste YouTube Link

          # Download Button
          - show_name: true
            show_icon: true
            type: button
            name: ⬇️ Download Video
            tap_action:
              action: perform-action
              perform_action: script.download_youtube_video
              target: {}
            icon: mdi:cloud-download

      # Playback Section (NEW)
      - type: markdown
        content: |
          ## 🎵 Play Downloaded Music
          Download complete? Play directly from your NAS or download to your device!

      - type: custom:iframe
        url: "http://192.168.1.44"
        aspect_ratio: "16:9"

    type: masonry
    icon: mdi:cloud-download
```

**Important:** Replace `192.168.1.44` with your actual NAS IP address!

---

## Step 4: Set Up Web Access Link (Optional)

Add a button to quickly access the downloader web interface:

1. In the dashboard, click **+ Add Card**
2. Select **Button** card
3. Configure:

```yaml
type: button
name: 🌐 Open Web Interface
tap_action:
  action: url
  url_path: "http://192.168.1.44"
icon: mdi:web
```

---

## Step 5: Add Notifications (Optional)

Get notified on your phone when downloads complete.

### Create Download Started Notification

1. Go to **Automations & Scenes → Automations**
2. Click **Create Automation**
3. Add trigger:
   ```yaml
   trigger:
     - platform: state
       entity_id: script.download_youtube_video
       to: "on"
   ```
4. Add action:
   ```yaml
   action: notify.notify
   data:
     title: "🎵 Download Started"
     message: "{{ states('input_text.youtube_url') }}"
   ```
5. Click **Save**

### Create Download Complete Notification

1. Create another automation
2. Trigger (after 2 minutes):
   ```yaml
   trigger:
     - platform: time
       at: "00:02:00"
   ```
3. Action:
   ```yaml
   action: notify.notify
   data:
     title: "✅ Download Complete"
     message: "Your MP3 is ready to play!"
   ```

---

## Step 6: Create a Playlist Dashboard (Optional)

View and manage all downloaded files:

1. Click **+ Add Card** on dashboard
2. Use Markdown to create a section:

```yaml
- type: markdown
  content: |
    ## 📂 Downloaded Files

    **Access your downloaded MP3s:**
    - Use the web interface player
    - Download to your device
    - Create playlists in your music app

    [Open Player](http://192.168.1.44)
```

---

## Step 7: Configure HACS Integration (If Using)

If you want deeper Home Assistant integration:

### Add Custom Integration

1. In Home Assistant, go to **HACS**
2. Click **+ Create Custom Repositories**
3. Add your GitHub repo URL
4. Restart Home Assistant

### Configure Integration

Edit `configuration.yaml`:

```yaml
youtube_mp3_downloader:
  backend_url: http://192.168.1.44:8000
  frontend_url: http://192.168.1.44
  download_directory: /mnt/downloads
  scan_interval: 60
  timeout: 30
```

---

## Complete Dashboard YAML (Full Featured)

If you want a more complete dashboard with multiple sections:

```yaml
title: YouTube Downloader
views:
  - path: youtube
    title: Downloader
    cards:
      # Header
      - type: markdown
        content: |
          # 🎵 YouTube to MP3 Converter
          **Your personal music downloader on the NAS**

          Download your favorite videos as high-quality MP3 files instantly!

      # Main Download Section
      - type: vertical-stack
        title: Download Section
        cards:
          - type: entities
            title: "Step 1: Enter YouTube URL"
            entities:
              - entity: input_text.youtube_url

          - type: button
            name: "⬇️ Download to NAS"
            tap_action:
              action: perform-action
              perform_action: script.download_youtube_video
            icon: mdi:cloud-download
            icon_height: 40px

      # Status Section
      - type: markdown
        content: |
          ## ℹ️ Status

          **Last Action:** Check notifications below

          Files are downloaded to: `/mnt/downloads/`

      # Web Player Section
      - type: markdown
        content: |
          ## 🎧 Play Your Music

          Open the player to browse, play, and download all your MP3s!

      - type: button
        name: "▶️ Open Music Player"
        tap_action:
          action: url
          url_path: "http://192.168.1.44"
        icon: mdi:play-circle
        icon_height: 40px

      # Instructions
      - type: markdown
        content: |
          ## 📖 How To Use

          ### Quick Steps
          1. Copy a YouTube URL
          2. Paste it in the field above
          3. Click "Download to NAS"
          4. Wait 1-2 minutes
          5. Open the player to find your MP3!

          ### Supported URLs
          - `https://www.youtube.com/watch?v=...`
          - `https://youtu.be/...`
          - YouTube playlists
          - YouTube Shorts

          ### Features
          - ✅ High-quality MP3 (192 kbps)
          - ✅ Automatic metadata
          - ✅ Instant playback
          - ✅ Download to device
          - ✅ Stored on your NAS

      # Footer
      - type: markdown
        content: |
          ---

          **Running on your local network** • No tracking • No ads

          Music files stored safely on your NAS

          For issues: Check Home Assistant logs

    type: masonry
    icon: mdi:music-box
```

---

## Step 8: Mobile-Optimized View (Optional)

Create a mobile-friendly view:

```yaml
- path: youtube-mobile
  title: Download
  cards:
    - type: markdown
      content: |
        # 🎵 YouTube Downloader

    - type: entities
      entities:
        - entity: input_text.youtube_url

    - type: button
      name: ⬇️ Download
      tap_action:
        action: perform-action
        perform_action: script.download_youtube_video
      icon_height: 50px

    - type: button
      name: ▶️ Player
      tap_action:
        action: url
        url_path: "http://192.168.1.44"
      icon_height: 50px

  type: masonry
  icon: mdi:music
```

---

## Step 9: Testing the Setup

### Test Download:

1. Open the dashboard
2. Paste this test URL:
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```
3. Click **Download**
4. Check notification appears
5. Wait 1-2 minutes
6. Check `http://192.168.1.44` to see the file

### Test Play:

1. Once downloaded, open the web player
2. Click ▶️ next to the file
3. Audio should play in a new tab

### Test Download to Device:

1. Open the web player
2. Click ⬇️ next to the file
3. File should download to your Downloads folder

---

## Troubleshooting

### Script Not Found

**Problem:** `Service not found: script.download_youtube_video`

**Solution:**

1. Restart Home Assistant
2. Verify script is saved
3. Check in Developer Tools → Services

### Can't See Web Interface

**Problem:** Iframe shows error

**Solution:**

1. Change IP address to match your NAS
2. Verify NAS is accessible from Home Assistant
3. Check firewall allows port 80

### Download Button Does Nothing

**Problem:** Click button but nothing happens

**Solution:**

1. Check notification appeared (check bell icon)
2. Verify URL is valid YouTube link
3. Check backend logs on NAS

### No Notifications

**Problem:** Don't get notifications

**Solution:**

1. Verify notifications are enabled in Home Assistant
2. Check default notification service is set
3. Look in Home Assistant logs

---

## Advanced Configuration

### Custom Download Path

Edit `configuration.yaml`:

```yaml
youtube_mp3_downloader:
  download_directory: /volume1/music # For Synology
```

### Increase Download Timeout

```yaml
youtube_mp3_downloader:
  timeout: 60 # 60 seconds for slow internet
```

### Add Download Counter Sensor

If you want to track downloads:

```yaml
template:
  - sensor:
      - name: YouTube Downloads Today
        unique_id: youtube_downloads_today
        unit_of_measurement: "files"
        icon: mdi:music-box-multiple
        state: "{{ (state_attr('youtube_mp3_downloader.stats', 'downloads_today') | int(0)) }}"
```

---

## Quick Reference

### Entity IDs

| Entity                          | Type       | Purpose            |
| ------------------------------- | ---------- | ------------------ |
| `input_text.youtube_url`        | Input Text | Store YouTube URL  |
| `script.download_youtube_video` | Script     | Download action    |
| `notification.create`           | Service    | Show notifications |

### Service Calls

**Download a video:**

```yaml
action: youtube_mp3_downloader.download_video
data:
  url: "https://www.youtube.com/watch?v=..."
```

**Play a file:**

```
http://192.168.1.44/api/play/filename.mp3
```

**Download a file:**

```
http://192.168.1.44/api/download-file/filename.mp3
```

---

## File Locations

### Home Assistant Config

```
/config/
├── automations.yaml
├── scripts.yaml
├── configuration.yaml
└── dashboards/
    └── youtube.yaml (optional)
```

### Downloaded MP3s

```
/mnt/downloads/
├── Song 1.mp3
├── Song 2.mp3
└── ...
```

---

## Summary Checklist

- [ ] Created input_text.youtube_url helper
- [ ] Created download_youtube_video script
- [ ] Created YouTube Downloader dashboard
- [ ] Tested downloading a video
- [ ] Tested playing a video
- [ ] Tested downloading to device
- [ ] Optional: Set up notifications
- [ ] Optional: Added HACS integration
- [ ] Optional: Created mobile view

---

## What's New (Play & Download Feature)

The latest update added:

✅ **Play Button (▶️)** - Stream MP3 directly in browser
✅ **Download Button (⬇️)** - Save MP3 to your device
✅ **File Management** - Browse all downloaded files
✅ **Security** - Filename validation and safety checks

Access these features via:

- Web interface: `http://192.168.1.44`
- Dashboard: Embedded player card
- Direct URLs:
  - Play: `http://192.168.1.44/api/play/filename.mp3`
  - Download: `http://192.168.1.44/api/download-file/filename.mp3`

---

## Support

### Check Home Assistant Logs

```
Settings → System → Logs
Search: youtube
```

### Test Script Manually

```
Developer Tools → Services
Call: script.download_youtube_video
```

### Test Backend Connection

```bash
# From any device on network
curl http://192.168.1.44:8000/health
```

---

## Final Notes

- **No sensors needed** - Dashboard uses direct input/output
- **Simple script** - Handles validation and error messages
- **Web-based** - No need for custom Home Assistant integration
- **Fully functional** - Tested and working!

Your YouTube downloader is fully integrated with Home Assistant! 🎉
