# PhotoQuick ⚡

> **Professional Photo & Video Asset Fetcher — Built in Lebanon**

[![Version](https://img.shields.io/badge/release-v1.0-00E5FF?style=flat-square)](https://github.com/Fadellab/photoquick-pro/releases)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey?style=flat-square&logo=windows)
[![GitHub stars](https://img.shields.io/github/stars/Fadellab/photoquick-pro?style=flat-square)](https://github.com/Fadellab/photoquick-pro/stargazers)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)

---

## What is PhotoQuick?

**PhotoQuick** is a high-performance desktop utility built for professional photographers and media managers. It allows you to instantly search a folder by asset IDs or file name keywords, then automatically extract and export all matching photos, RAW files, and videos into a clean output folder — with zero duplicates.

Whether you're recovering specific shots from a 10,000-image card dump, or filtering client assets by reference number, PhotoQuick gets it done in seconds.

---

## Features

- 🔍 **ID-Based Asset Fetching** — Paste a list of IDs or keywords; PhotoQuick scans the directory and pulls every matching file
- 📁 **Auto Export Folder** — All results are copied to a `PhotoQuick_Export/` subfolder automatically
- 🚫 **Duplicate Guard** — Smart deduplication ensures no file is copied twice, even across repeated runs
- 🖼️ **Wide Format Support** — JPG, PNG, WEBP, HEIC, RAW formats (CR2, NEF, ARW, DNG, ORF), MP4, MOV, AVI
- 🌗 **Dark / Light Mode** — Toggle between themes in one click
- ⚡ **Threaded Engine** — Search runs in a background thread, keeping the UI fully responsive
- 💡 **Splash Screen** — Clean animated intro with a progress bar on launch
- 🪟 **About Window** — Version info, creator details, and quick-access contact links

---

## Screenshots

> *(Add your screenshots here)*

| Dark Mode | Light Mode |
|-----------|------------|
| ![dark](screenshots/dark.png) | ![light](screenshots/light.png) |

---

## Supported File Formats

| Category | Extensions |
|----------|-----------|
| **Standard Images** | `.jpg` `.jpeg` `.png` `.bmp` `.webp` `.heic` |
| **RAW Camera Files** | `.cr2` `.nef` `.arw` `.dng` `.orf` |
| **Video** | `.mp4` `.mov` `.avi` |

---

## How It Works

PhotoQuick follows a simple 3-step workflow shown directly in the UI:

```
[1. INPUT SEQUENCE] → [2. DIRECTORY] → [3. STATUS / EXTRACT]
```

1. **Enter your IDs** — Type or paste asset IDs / file name keywords into the input box (separated by spaces, commas, or newlines)
2. **Select a folder** — Browse to the directory containing your media files
3. **Hit START EXTRACTION** — PhotoQuick scans every file in the folder, matches it against your ID list, and copies all hits to `PhotoQuick_Export/` inside the selected directory

### Under the Hood

- The `SearchEngine` class handles all file matching logic in a daemon thread
- A file is matched if **any** of the provided IDs appear anywhere in the filename
- Files already present in the export folder are automatically skipped (no overwrites, no duplicates)
- The UI status label updates in real time as each match is found
- On completion, a summary dialog shows the total number of assets recovered

---

## Installation

### Option A — Run the `.exe` (Recommended for Windows users)

Download the latest release from the [Releases](https://github.com/Fadellab/photoquick-pro/releases) page and run `PhotoQuick.exe` directly. No Python installation required.

> Place `icon.ico` and `i.png` in the same folder as the `.exe` if running outside of the packaged build.

### Option B — Run from Source

**Requirements:**
- Python 3.8 or higher
- pip

**Clone the repo:**

```bash
git clone https://github.com/Fadellab/photoquick-pro.git
cd photoquick-pro
```

**Install dependencies:**

```bash
pip install customtkinter pillow
```

**Run:**

```bash
python PhotoQuick.py
```

---

## Building the EXE (PyInstaller)

To compile PhotoQuick into a standalone Windows executable:

```bash
pip install pyinstaller
```

```bash
pyinstaller --noconfirm --onefile --windowed \
  --icon=icon.ico \
  --add-data "icon.ico;." \
  --add-data "icon.png;." \
  --add-data "i.png;." \
  PhotoQuick.py
```

The compiled `.exe` will appear in the `dist/` folder.

> **Required assets to bundle:** `icon.ico`, `icon.png`, `i.png` (splash screen image)

---

## Project Structure

```
PhotoQuick/
├── PhotoQuick.py        # Main application source
├── icon.ico             # App icon (Windows)
├── icon.png             # App icon (fallback)
├── i.png                # Splash screen image
└── README.md
```

---

## Release Notes

### v1.0 — Initial Release

- ✅ Core ID-based file fetcher with multi-keyword support
- ✅ Background threaded search engine (UI stays responsive)
- ✅ Smart duplicate detection (by filename and source path)
- ✅ Auto-creation of `PhotoQuick_Export/` output directory
- ✅ Support for 14 file formats across images, RAW, and video
- ✅ Animated splash screen on launch
- ✅ Dark / Light mode toggle
- ✅ About window with creator info and contact links
- ✅ PyInstaller-compatible with `sys._MEIPASS` resource handling
- ✅ Packaged as a single `.exe` for Windows

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `customtkinter` | Modern UI framework |
| `Pillow (PIL)` | Image loading and processing |
| `tkinter` | Base windowing system (built into Python) |
| `shutil` | File copy operations |
| `threading` | Background search thread |

---

## About

| | |
|--|--|
| **Creator** | Mohammed Fadel |
| **Origin Year** | 2022 |
| **Last Update** | 2026.2 |
| **Region** | Beirut, Lebanon |
| **Website** | [photoquick.unaux.com](https://photoquick.unaux.com/) |
| **WhatsApp** | [+964 788 490 8775](https://wa.me/9647884908775) |

---

## Contact

Have a bug to report or a feature request?

- 🌐 **Website:** [photoquick.unaux.com](https://photoquick.unaux.com/)
- 💬 **WhatsApp:** [Chat directly](https://wa.me/9647884908775)

---

<p align="center">Made with precision in Lebanon 🇱🇧 — PhotoQuick © 2022–2026</p>
