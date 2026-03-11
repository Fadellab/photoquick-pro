# PhotoQuick Pro ⚡

&gt; **Save 15 Minutes On Every Client.**  
&gt; Stop wasting time searching for photo numbers manually. Paste your client's list, click once, and let PhotoQuick Pro find and copy all photos in 3 seconds instead of 15 minutes.

[![Download](https://img.shields.io/badge/Download-PhotoQuick_Pro-00E5FF?style=for-the-badge)](https://github.com/fadellab/PhotoQuick-Pro/releases)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge)]()
[![Made In](https://img.shields.io/badge/Made%20In-Lebanon-%23EE3344?style=for-the-badge)]()

---

## 🎯 The Problem

**The Old Way:**
- Client sends list: `"3428, 3634, 5343, 5421, 6123..."`
- Open File Explorer, search for 3428...
- Copy, paste to folder. Repeat 50 times.
- **15-20 minutes wasted per client.**

**The PhotoQuick Way:**
1. Paste the entire list at once (supports spaces, commas, or new lines)
2. Select your photos folder
3. Click **"Start Extraction"**
4. **Done in 3 seconds** — all files organized in `PhotoQuick_Export` folder

---

## ✨ Features

| Feature | Benefit |
|---------|---------|
| ⚡ **3-Second Processing** | What used to take 15-20 minutes now happens instantly |
| 📋 **Bulk List Support** | Paste hundreds of numbers at once from email/messages/Excel |
| 🖼️ **Multi-Format Support** | Works with JPG, PNG, BMP, WEBP, HEIC, RAW (CR2, NEF, ARW, DNG, ORF) and videos (MP4, MOV, AVI) |
| 🔒 **100% Offline** | Your photos never leave your computer. Complete privacy |
| 🚫 **Duplicate Protection** | Smart tracking prevents copying the same file twice |
| 🌓 **Dark/Light Mode** | Choose your preferred interface theme |
| 🆓 **Free Forever** | Made for photographers, not for profit |

---

## 📥 Download & Installation

**[⬇️ Download PhotoQuick Pro v1.0](https://github.com/fadellab/PhotoQuick-Pro/releases)**  
*100% Free • Portable Executable • No Installation Required • Works Offline*

### System Requirements
- **OS:** Windows 10/11 (64-bit)
- **RAM:** 4GB minimum (8GB recommended for large libraries)
- **Storage:** 50MB for application + space for exported photos
- **Display:** 1366×768 or higher resolution

### Installation
1. Download `PhotoQuick-Pro.exe` from the [Releases](https://github.com/fadellab/PhotoQuick-Pro/releases) page
2. Extract to your preferred location
3. Run `PhotoQuick-Pro.exe` — no installation needed

---

## 🎬 How It Works

![Demo](assets/demo.gif) *(add a screen recording here)*

### Step-by-Step Usage

1. **Launch the Application**
   - Splash screen appears while loading (3 seconds)
   - Main interface opens with three columns

2. **Input Sequence (Left Column)**
   - Paste client photo numbers in the text box
   - **Supported formats:** `3428, 3634, 5343` or `3428 3634 5343` or one per line
   - The app automatically parses spaces, commas, and new lines

3. **Select Directory (Middle Column)**
   - Click **"SELECT FOLDER"** button
   - Navigate to your photo library containing original files
   - Supported files are automatically detected by extension

4. **Start Extraction (Right Column)**
   - Click **"START EXTRACTION"**
   - Watch real-time status updates in the Status column
   - Progress bar shows processing state
   - Found files are copied to `PhotoQuick_Export` subfolder

5. **Retrieve Your Photos**
   - Open the `PhotoQuick_Export` folder inside your selected directory
   - All matched files are organized and ready for delivery

### Technical Workflow
- **Scanning:** Recursively scans selected directory for supported media files
- **Matching:** Checks if any input ID exists in filenames (partial match supported)
- **Copying:** Uses `shutil.copy2()` to preserve metadata and timestamps
- **Duplicate Prevention:** Tracks copied source files to prevent duplicates
- **Naming:** If filename exists, appends timestamp to prevent overwrites

---

## 🛠️ Technical Architecture

### Core Technologies
- **Language:** Python 3.11+
- **GUI Framework:** CustomTkinter (modern tkinter alternative)
- **Image Processing:** Pillow (PIL) for splash screen and icons
- **Build Tool:** PyInstaller (single executable)
- **Threading:** Multi-threaded search to prevent UI freezing

### File Structure
