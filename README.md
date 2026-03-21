# vid2gif

A self-hosted web app for converting video clips to GIFs. Built with Flask and FFmpeg, runs in Docker. Includes a file size estimator for use in sharing GIFs to platforms with file size limits, such as Discord and GitHub.

![Replay_2026-03-19_22-18-16_f56fe458](https://github.com/user-attachments/assets/1d29efcc-d6d9-4537-9a4e-498bd2ad09a1)

## Features

- Browse and select any common video format (mp4, mov, avi, mkv, webm, wmv, flv, m4v)
- Adjustable FPS (1–30) and output width (120–960px)
- Visual trim slider with dual handles to set start and end points. Supports manual timestamp input in h:mm:ss format for precise control on long videos
- Live output size estimator that accounts for source video complexity via input bitrate, and learns from previous conversions of the same file for improved accuracy
- High quality GIF output using FFmpeg 2-pass palette generation
- GIFs are never saved to the server; delivered directly to the browser and downloaded client-side only
- Inline GIF preview with one-click download
- Sequential conversions without page refresh, with a history of previous conversions in the session

## Usage

Point your browser at the app, browse for a video, adjust your parameters, trim your clip, and hit Convert. The estimated output size updates live as you adjust settings. Aim to keep it under 10 MB for easy sharing. After your first conversion of a file, the size estimator will be calibrated to that specific video for more accurate future estimates.

## Security

**This app has no authentication, no authorization, and no rate limiting.** It is designed exclusively for use on a trusted local network.

- Do not expose this to the public internet
- Anyone with network access to the app can upload files and trigger FFmpeg conversions on your server
- No input sanitization beyond basic file extension checking is guaranteed

Run it on your LAN or Tailnet only.

## Stack

- **Backend**: Python / Flask
- **Conversion**: FFmpeg (2-pass palette GIF encoding)
- **Frontend**: Vanilla HTML/CSS/JS, no dependencies
- **Container**: Docker
