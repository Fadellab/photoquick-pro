<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=00E5FF&height=200&section=header&text=PhotoQuick&fontSize=80&fontColor=ffffff&fontAlignY=38&desc=Precision%20Asset%20Fetcher%20%E2%80%94%20Find.%20Extract.%20Done.&descAlignY=58&descSize=18" width="100%"/>

<br/>

[![Release](https://img.shields.io/badge/⚡%20Release-v1.0-00E5FF?style=for-the-badge&labelColor=0a0a0a)](https://github.com/Fadellab/photoquick-pro/releases)
[![License](https://img.shields.io/badge/📄%20License-MIT-brightgreen?style=for-the-badge&labelColor=0a0a0a)](LICENSE)
[![Free](https://img.shields.io/badge/💸%20Price-Free%20Forever-gold?style=for-the-badge&labelColor=0a0a0a)](#-free--open-source)
[![Open Source](https://img.shields.io/badge/❤️%20Open-Source-ff69b4?style=for-the-badge&labelColor=0a0a0a)](#-free--open-source)
[![Python](https://img.shields.io/badge/Python-3.8+-3670A0?style=for-the-badge&logo=python&logoColor=white&labelColor=0a0a0a)](https://python.org)
[![Platform](https://img.shields.io/badge/Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white&labelColor=0a0a0a)](https://github.com/Fadellab/photoquick-pro/releases)
[![Stars](https://img.shields.io/github/stars/Fadellab/photoquick-pro?style=for-the-badge&logo=github&color=yellow&labelColor=0a0a0a)](https://github.com/Fadellab/photoquick-pro/stargazers)

<br/>

> **"You have thousands of photos. You have a list of IDs. You need them now."**
> 
> PhotoQuick scans, matches, and extracts your files in seconds — zero manual hunting, zero duplicates.

<br/>

</div>

---

<div align="center">

## ✦ &nbsp; Quick Navigation &nbsp; ✦

[🎯 What It Does](#-what-it-does) · [🖥️ Interface](#%EF%B8%8F-the-interface) · [🔧 How It Works](#-how-the-fetcher-works) · [🚀 Install](#-installation) · [⚖️ License](#%EF%B8%8F-free--open-source) · [👤 Author](#-author)

</div>

---

## 🎯 What It Does

PhotoQuick is a **professional-grade desktop utility** built for photographers and media managers.

Give it a list of file IDs or keywords. Point it at a folder. It will find every matching photo, RAW file, or video and copy them all into a clean `PhotoQuick_Export/` folder — automatically, instantly, with **no duplicates ever**.

Whether you're recovering specific shots from a 10,000-image card dump or filtering a client delivery by reference number, PhotoQuick gets it done in seconds.

<br/>

---

## 🖥️ The Interface

A clean, three-column layout. No menus, no complexity. Just the three things you need:

```
╔══════════════════╦══════════════════╦══════════════════╗
║  1. INPUT        ║  2. DIRECTORY    ║  3. STATUS       ║
║  SEQUENCE        ║                  ║                  ║
║                  ║  ┌────────────┐  ║   ◉  READY       ║
║  DSC_0042        ║  │  SELECT    │  ║  ──────────────  ║
║  IMG_1187        ║  │  FOLDER    │  ║                  ║
║  CLIENT_009      ║  └────────────┘  ║  ┌────────────┐  ║
║  WEDDING_33      ║                  ║  │   START    │  ║
║  ...             ║  /Volumes/Card/  ║  │ EXTRACTION │  ║
║                  ║  Shoot_2026/     ║  └────────────┘  ║
╚══════════════════╩══════════════════╩══════════════════╝
```

| Step | Action |
|:----:|--------|
| **①** | Paste your asset IDs or keywords — separated by space, comma, or newline |
| **②** | Browse to the folder that contains your media files |
| **③** | Hit **START EXTRACTION** and watch matches appear in real time |

> 📂 All results are saved to **`PhotoQuick_Export/`** inside your selected folder

<br/>

---

## 🎨 Formats Supported

```
┌───────────────┬──────────────────────────────────────────────┐
│  📷 Images    │  .jpg  .jpeg  .png  .bmp  .webp  .heic       │
│  🎞️ RAW       │  .cr2  .nef  .arw  .dng  .orf               │
│  🎬 Video     │  .mp4  .mov  .avi                            │
└───────────────┴──────────────────────────────────────────────┘
                        14 formats total
```

<br/>

---

## 🔧 How the Fetcher Works

The `SearchEngine` class is the brain of PhotoQuick. This is exactly what runs when you press START:

```
  ┌──────────────────────────────────────────┐
  │         Your ID Input                    │
  │  "DSC_042, IMG_1187, CLIENT_09 ..."      │
  └────────────────────┬─────────────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │   Scan Target Directory  │
         │   (all 14 valid formats) │
         └─────────────┬───────────┘
                       │
          ┌────────────▼────────────┐
          │  Does filename contain  │
          │     any input ID?       │
          └──────┬──────────┬───────┘
                NO           YES
                 │            │
              (skip)          ▼
                    ┌─────────────────────┐
                    │  Already exists in  │
                    │  PhotoQuick_Export? │
                    └────┬───────────┬────┘
                        YES          NO
                         │            │
                      (skip)          ▼
                              ┌──────────────────┐
                              │  shutil.copy2()  │
                              │  → Export Folder │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │  Mark source in  │
                              │  tracking set    │
                              └────────┬─────────┘
                                       │
                                       ▼
                              Status: "FOUND: file.jpg"
```

**🛡️ Duplicate Guard — Two Layers of Protection:**

- **Layer 1** — Checks if the file name already exists in the export folder
- **Layer 2** — Tracks source paths in memory, prevents re-copying even if names differ

**⚡ Threaded Engine** — The scan runs on a background daemon thread. The UI stays fully responsive no matter how large the directory is.

<br/>

---

## 🚀 Installation

### 🪟 Option A — Windows EXE *(Recommended — No Python needed)*

<div align="center">

[![Download EXE](https://img.shields.io/badge/⬇️%20Download-PhotoQuick%20v1.0.exe-00E5FF?style=for-the-badge&labelColor=0a0a0a)](https://github.com/Fadellab/photoquick-pro/releases)

</div>

Download from the [Releases page](https://github.com/Fadellab/photoquick-pro/releases), run the `.exe`. No installation, no setup.

> **Note:** Keep `icon.ico` and `i.png` in the same folder as the `.exe` if running outside the packaged build.

---

### 🐍 Option B — Run from Source

```bash
# Clone the repository
git clone https://github.com/Fadellab/photoquick-pro.git
cd photoquick-pro

# Install dependencies
pip install customtkinter pillow

# Launch the app
python PhotoQuick.py
```

> Requires **Python 3.8+** · `tkinter` ships with Python by default

---

### 🛠️ Option C — Build Your Own EXE

```bash
pip install pyinstaller

pyinstaller --noconfirm --onefile --windowed ^
  --icon=icon.ico ^
  --add-data "icon.ico;." ^
  --add-data "icon.png;." ^
  --add-data "i.png;." ^
  PhotoQuick.py
```

Compiled binary lands in `dist/`. The app uses `sys._MEIPASS` to locate bundled assets at runtime.

<br/>

---

## 📁 Project Structure

```
photoquick-pro/
│
├── 📄  PhotoQuick.py     ← Full application source
├── 🖼️   i.png             ← Splash screen image
├── 🔷  icon.ico          ← Windows taskbar icon
├── 🖼️   icon.png          ← Icon fallback (PNG)
└── 📋  README.md
```

---

## 📦 Dependencies

| Package | Role |
|---|---|
| `customtkinter` | Modern themed UI framework (dark/light mode) |
| `Pillow` | Image rendering for splash screen and icons |
| `tkinter` | Native OS windowing system (built into Python) |
| `shutil` | File copy engine with metadata preservation |
| `threading` | Background thread for non-blocking scans |

<br/>

---

## ⚖️ Free & Open Source

<div align="center">

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║    PhotoQuick is 100% FREE and OPEN SOURCE.                ║
║                                                            ║
║    ✅  Free to download, use, and share — forever          ║
║    ✅  Full source code publicly available on GitHub       ║
║    ✅  No license fees, no subscriptions, no paywalls      ║
║    ✅  Modify and adapt for your own projects              ║
║    ✅  Contributions and pull requests are welcome         ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

</div>

PhotoQuick is released under the **MIT License** — one of the most permissive open-source licenses available. This means:

- ✔ **Use it** personally, commercially, or professionally
- ✔ **Modify it** — change anything you want in the source
- ✔ **Distribute it** — share it with anyone, anywhere
- ✔ **No warranty required** — use at your own discretion

The only condition is that the original copyright notice and license text must be included in any copies or distributions.

```
MIT License — Copyright (c) 2022–2026 Mohammed Fadel
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software to use, copy, modify, merge, publish, distribute, and/or sell
copies of the software, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

> 📄 See the full [`LICENSE`](LICENSE) file in this repository for complete legal text.

<br/>

---

## 📋 v1.0 — What's Shipped

| # | Feature | Status |
|---|---------|:------:|
| 1 | ID-based asset fetcher with multi-keyword input | ✅ |
| 2 | Background threaded scan engine (non-blocking UI) | ✅ |
| 3 | Dual-layer duplicate guard (filename + source path) | ✅ |
| 4 | Auto-creates `PhotoQuick_Export/` output directory | ✅ |
| 5 | 14 file formats — images, RAW, video | ✅ |
| 6 | Real-time status updates during extraction | ✅ |
| 7 | Animated splash screen with live progress bar | ✅ |
| 8 | Dark mode / Light mode toggle | ✅ |
| 9 | About window with contact links | ✅ |
| 10 | PyInstaller-compatible single `.exe` for Windows | ✅ |

<br/>

---

## 👤 Author

<div align="center">

```
  ╭────────────────────────────────────────╮
  │                                        │
  │   Mohammed Fadel                       │
  │   Beirut, Lebanon 🇱🇧                  │
  │                                        │
  │   Building tools for photographers    │
  │   since 2022.                          │
  │                                        │
  ╰────────────────────────────────────────╯
```

[![Website](https://img.shields.io/badge/🌐%20Website-photoquick.unaux.com-00E5FF?style=for-the-badge&labelColor=0a0a0a)](https://photoquick.unaux.com/)
[![WhatsApp](https://img.shields.io/badge/💬%20WhatsApp-Contact-25D366?style=for-the-badge&logo=whatsapp&logoColor=white&labelColor=0a0a0a)](https://wa.me/9647884908775)
[![GitHub](https://img.shields.io/badge/GitHub-Fadellab-white?style=for-the-badge&logo=github&logoColor=black&labelColor=0a0a0a)](https://github.com/Fadellab)

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=00E5FF&height=100&section=footer" width="100%"/>

**PhotoQuick** — Open Source · Free Forever · Made with ❤️ in Lebanon · 2022–2026

⭐ If PhotoQuick saved you time, consider starring the repo — it means a lot!

</div>
