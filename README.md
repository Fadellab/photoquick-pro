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

### Supported File Formats
| Type | Extensions |
|------|------------|
| **Images** | `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`, `.heic` |
| **RAW** | `.cr2` (Canon), `.nef` (Nikon), `.arw` (Sony), `.dng` (Adobe), `.orf` (Olympus) |
| **Video** | `.mp4`, `.mov`, `.avi` |

---

## ⚠️ Important Legal Notices & Disclaimers

### Software Disclaimer
**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.** By downloading and using PhotoQuick Pro, you acknowledge and agree to the following:

1. **No Warranty:** This software is provided without any guarantees regarding performance, reliability, or fitness for a particular purpose. The entire risk as to the quality and performance of the program is with you.

2. **Data Safety:** While PhotoQuick Pro only **copies** files (never moves or deletes), you are strongly advised to maintain backups of your original photo libraries. The authors assume no responsibility for data loss, corruption, or unintended file operations.

3. **Filename Matching Limitation:** The software performs partial string matching on filenames. It may match unintended files if your ID numbers appear within other filenames (e.g., searching for "123" will match "1234", "4123", "12345"). Always verify exported files before delivery.

4. **System Compatibility:** This software is designed for Windows 10/11. Operation on other platforms or Windows versions is not guaranteed.

5. **Resource Usage:** Large photo libraries (10,000+ files) may cause temporary high CPU/disk usage during scanning. Ensure adequate system resources before processing.

### Copyright & Intellectual Property
- **Copyright © 2022-2026 Mohammed Fadel. All Rights Reserved.**
- PhotoQuick Pro and its associated code, design, and documentation are protected by copyright law.
- The name "PhotoQuick", "PhotoQuick Pro", and the application icon are trademarks of the author.

### Third-Party Licenses
This software uses the following open-source components under their respective licenses:

| Component | License | Purpose |
|-----------|---------|---------|
| CustomTkinter | MIT License | Modern GUI framework |
| Pillow (PIL) | HPND License | Image processing |
| PyInstaller | GPL-2.0+ with exception | Executable building |

Full license texts for third-party components are available in the `THIRD_PARTY_LICENSES.txt` file included with the distribution.

### Privacy Policy
**PhotoQuick Pro is 100% offline software.** 
- No internet connection required for core functionality
- No user data, photo metadata, or usage statistics are collected
- No telemetry, analytics, or tracking mechanisms are implemented
- Your photo files remain exclusively on your local machine
- The only network activity is optional: clicking "Visit Official Website" or "Contact via WhatsApp" buttons opens your default browser

### Limitation of Liability
**IN NO EVENT SHALL THE AUTHORS, COPYRIGHT HOLDERS, OR DISTRIBUTORS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY** — whether in an action of contract, tort, or otherwise — arising from, out of, or in connection with the software or the use or other dealings in the software.

This includes but is not limited to:
- Loss of profits, data, or business interruption
- Damage to computer systems or storage devices
- Client dissatisfaction due to incorrect file matching
- Time lost due to software malfunction

### User Responsibilities
By using this software, you agree to:
1. Verify all exported files before delivering to clients
2. Maintain secure backups of your original photo libraries
3. Use the software in compliance with all applicable laws
4. Not attempt to reverse engineer, decompile, or modify the executable
5. Not redistribute modified versions without explicit permission

### DMCA & Copyright Compliance
PhotoQuick Pro is designed to help photographers manage their own intellectual property. Users are solely responsible for ensuring they have legal rights to copy, distribute, or modify any files processed through this software. The developers assume no liability for copyright infringement or misuse of the software to violate third-party rights.

---

## 🤝 Contributing

This tool was built to solve a real photographer's workflow problem in Beirut, Lebanon. Community contributions are welcome!

### How to Contribute
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
git clone https://github.com/fadellab/PhotoQuick-Pro.git
cd PhotoQuick-Pro
pip install -r requirements.txt
python PhotoQuick.py
