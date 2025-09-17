# Sentinel-D1  
A lightweight, async download manager with a live terminal dashboard.

## Features
-  **Concurrent downloads** using `asyncio` + `aiohttp`
-  Pause, resume, and cancel individual downloads
-  Live progress dashboard powered by [`rich`](https://github.com/Textualize/rich)
-  Resume interrupted downloads (HTTP Range support)

---

## Quick Start

### 1️ Clone & Install
```bash
git clone https://github.com/<sedegah>/sentinel-d1.git
cd sentinel-d1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

2️ Usage

Start the daemon:

sentinel-d1 serve


Add a download:

sentinel-d1 add https://example.com/file.zip


View active jobs:

sentinel-d1 list


Pause / resume / remove:

sentinel-d1 pause <job_id>
sentinel-d1 resume <job_id>
sentinel-d1 remove <job_id>


Downloaded files are saved in the current working directory unless you specify a custom path.

Project Structure
sentinel-d1/
├─ sentinel_d1/
│  ├─ cli.py          # CLI entrypoints
│  ├─ downloader.py   # DownloadJob class
│  ├─ manager.py      # DownloadManager + dashboard
│  └─ service.py      # FastAPI/uvicorn service
└─ pyproject.toml     # Build config

Requirements

Python 3.9+

aiohttp

rich

uvicorn

fastapi (if using the optional REST interface)
