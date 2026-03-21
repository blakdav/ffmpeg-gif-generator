# vid2gif

A self-hosted web app for converting video clips to GIFs. Built with Flask and FFmpeg, runs in Docker.

## Features

- Browse and select any common video format (mp4, mov, avi, mkv, webm, wmv, flv, m4v)
- Adjustable FPS (1–30) and output width (120–960px)
- Visual trim slider with dual handles to set start and end points — supports manual timestamp input in h:mm:ss format for precise control on long videos
- Live output size estimator that accounts for source video complexity via input bitrate
- High quality GIF output using FFmpeg 2-pass palette generation
- Inline GIF preview with one-click download
- Sequential conversions without page refresh, with a history of previous conversions in the session

## Usage

Point your browser at the app, browse for a video, adjust your parameters, trim your clip, and hit Convert. The estimated output size updates live as you adjust settings — aim to keep it under 10 MB for easy sharing.

## Security

**This app has no authentication, no authorization, and no rate limiting.** It is designed exclusively for use on a trusted local network or behind a VPN.

- Do not expose this to the public internet
- Anyone with network access to the app can upload files and trigger FFmpeg conversions on your server
- No input sanitization beyond basic file extension checking

## Stack

- **Backend**: Python / Flask
- **Conversion**: FFmpeg (2-pass palette GIF encoding)
- **Frontend**: Vanilla HTML/CSS/JS, no dependencies
- **Container**: Docker
