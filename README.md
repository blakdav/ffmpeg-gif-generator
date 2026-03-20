# ffmpeg-gif-generator

Drop a video, get a GIF. Self-hosted Docker container with a clean web UI.

## Features
- Drag & drop any common video format (mp4, mov, avi, mkv, webm, wmv, flv, m4v)
- Adjustable FPS (1–30)
- Adjustable output width (120–960px)
- Trim by start time + duration
- High-quality GIF using FFmpeg 2-pass palette generation
- Live preview + download in browser

## Quick start
```bash
git clone <your-repo>
cd vid2gif
docker compose up -d --build
```

Then open `http://localhost:5757`

## Unraid

Add as a custom Docker container:
- **Image**: build locally or push to Docker Hub
- **Port**: 5757 → 5000
- **Path**: `/mnt/user/appdata/vid2gif/output` → `/app/output`

## Notes

- Converted GIFs are saved to `./output/` on the host (bind mount)
- Uploads are temp files — cleaned up after each conversion
- Large videos at high FPS + large width = big GIFs and slow conversion
  - Recommended: 10fps, 480px for most use cases
  - Use "Duration" to clip long videos before converting
```

---

Repo structure should be:
```
vid2gif/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py
├── README.md
└── static/
    └── index.html
