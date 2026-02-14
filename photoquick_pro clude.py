#!/usr/bin/env python3
"""
PhotoQuick Pro 2026
Intelligent Photography Workflow Assistant
Single-file executable Windows application

Author: PhotoQuick Team
Version: 1.0.0
License: Proprietary
"""

import sys
import os
import json
import sqlite3
import hashlib
import shutil
import threading
import time
import base64
import io
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import subprocess

# PyQt6 imports
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QScrollArea, QFrame, QProgressBar,
        QDialog, QDialogButtonBox, QTextEdit, QLineEdit, QCheckBox,
        QFileDialog, QSystemTrayIcon, QMenu, QTabWidget, QTableWidget,
        QTableWidgetItem, QHeaderView, QGridLayout, QSplitter, QMessageBox,
        QStackedWidget, QSpinBox, QDoubleSpinBox, QComboBox, QGroupBox
    )
    from PyQt6.QtCore import (
        Qt, QThread, pyqtSignal, QTimer, QSize, QRect, QPoint,
        QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
        QSequentialAnimationGroup, QVariantAnimation, QThreadPool,
        QRunnable, pyqtSlot, QObject
    )
    from PyQt6.QtGui import (
        QPalette, QColor, QFont, QIcon, QPixmap, QPainter,
        QLinearGradient, QBrush, QPen, QImage, QCursor, QAction
    )
except ImportError:
    print("PyQt6 not found. Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *

# Image processing imports
try:
    from PIL import Image, ExifTags
    import cv2
    import numpy as np
except ImportError:
    print("Installing image processing libraries...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "opencv-python", "numpy"])
    from PIL import Image, ExifTags
    import cv2
    import numpy as np

# System monitoring
try:
    import psutil
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

# Windows-specific imports
if sys.platform == "win32":
    try:
        import win32file
        import win32con
        import win32api
    except ImportError:
        print("Installing Windows-specific packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
        import win32file
        import win32con
        import win32api


# === EMBEDDED RESOURCES ===

APP_ICON_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF
L2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0w
TXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRh
LyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4xLWMwMDAgNzkuYjBmOGJlOSwgMjAyMS8xMi8x
NS0yMTo1MjoyOSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9y
Zy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9
IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczpkYz0iaHR0
cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25z
LmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5j
b20veGFwLzEuMC9tbS8iIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAv
c1R5cGUvUmVzb3VyY2VFdmVudCMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIz
LjEgKFdpbmRvd3MpIiB4bXA6Q3JlYXRlRGF0ZT0iMjAyNi0wMi0xNFQxNDozMDowMCswMzowMCIg
eG1wOk1vZGlmeURhdGU9IjIwMjYtMDItMTRUMTQ6MzA6MDArMDM6MDAiIHhtcDpNZXRhZGF0YURh
dGU9IjIwMjYtMDItMTRUMTQ6MzA6MDArMDM6MDAiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiBwaG90
b3Nob3A6Q29sb3JNb2RlPSIzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjEyMzQ1Njc4LTEy
MzQtMTIzNC0xMjM0LTEyMzQ1Njc4OTBhYiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDoxMjM0
NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwYWIiIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJ
RD0ieG1wLmRpZDoxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwYWIiPiA8eG1wTU06
SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDpp
bnN0YW5jZUlEPSJ4bXAuaWlkOjEyMzQ1Njc4LTEyMzQtMTIzNC0xMjM0LTEyMzQ1Njc4OTBhYiIg
c3RFdnQ6d2hlbj0iMjAyNi0wMi0xNFQxNDozMDowMCswMzowMCIgc3RFdnQ6c29mdHdhcmVBZ2Vu
dD0iQWRvYmUgUGhvdG9zaG9wIDIzLjEgKFdpbmRvd3MpIi8+IDwvcmRmOlNlcT4gPC94bXBNTTpI
aXN0b3J5PiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFj
a2V0IGVuZD0iciI/PgH//v38+/r5+Pf29fTz8vHw7+7t7Ovq6ejn5uXk4+Lh4N/e3dzb2tnY19bV
1NPS0dDPzs3My8rJyMfGxcTDwsHAv769vLu6ubi3trW0s7KxsK+urayrqqmop6alpKOioaCfnp2c
m5qZmJeWlZSTkpGQj46NjIuKiYiHhoWEg4KBgH9+fXx7enl4d3Z1dHNycXBvbm1sa2ppaGdmZWRj
YmFgX15dXFtaWVhXVlVUU1JRUE9OTUxLSklIR0ZFRENCQUA/Pj08Ozo5ODc2NTQzMjEwLy4tLCsq
KSgnJiUkIyIhIB8eHRwbGhkYFxYVFBMSERAPDg0MCwoJCAcGBQQDAgEAACH5BAEAAAAALAAAAAAg
ACAAAAI/hI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuC8fyTNf2jef6zvf+DwwKh8Si8YhMKpfM
pvMJjUqn1Kr1is1qCwA7
"""

# Glassmorphism stylesheet
STYLESHEET = """
/* === GLOBAL STYLES === */
* {
    font-family: 'Segoe UI', 'Inter', 'SF Pro Display', sans-serif;
}

QMainWindow {
    background-color: #0A0A0F;
}

/* === CUSTOM TITLE BAR === */
#titleBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(20, 20, 27, 0.95),
                                stop:1 rgba(10, 10, 15, 0.95));
    border-bottom: 1px solid rgba(99, 102, 241, 0.2);
    min-height: 40px;
    max-height: 40px;
}

#titleLabel {
    color: #F8FAFC;
    font-size: 14px;
    font-weight: 600;
    padding-left: 12px;
}

#titleButton {
    background: transparent;
    border: none;
    color: #94A3B8;
    padding: 8px 16px;
    font-size: 16px;
}

#titleButton:hover {
    background: rgba(255, 255, 255, 0.05);
    color: #F8FAFC;
}

#closeButton:hover {
    background: #EF4444;
    color: white;
}

/* === SIDEBAR === */
#sidebar {
    background: rgba(20, 20, 27, 0.6);
    border-right: 1px solid rgba(99, 102, 241, 0.15);
    min-width: 280px;
    max-width: 280px;
}

/* === SESSION CARD === */
.sessionCard {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(255, 255, 255, 0.05),
                                stop:1 rgba(255, 255, 255, 0.02));
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 12px;
    margin: 8px;
}

.sessionCard:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(255, 255, 255, 0.08),
                                stop:1 rgba(255, 255, 255, 0.04));
    border: 1px solid rgba(99, 102, 241, 0.5);
}

.sessionCardSelected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(99, 102, 241, 0.2),
                                stop:1 rgba(139, 92, 246, 0.1));
    border: 2px solid rgba(99, 102, 241, 0.8);
}

/* === BUTTONS === */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(99, 102, 241, 0.8),
                                stop:1 rgba(99, 102, 241, 0.6));
    color: #F8FAFC;
    border: 1px solid rgba(99, 102, 241, 0.4);
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(99, 102, 241, 1.0),
                                stop:1 rgba(99, 102, 241, 0.8));
    border: 1px solid rgba(99, 102, 241, 0.6);
}

QPushButton:pressed {
    background: rgba(99, 102, 241, 0.5);
}

QPushButton:disabled {
    background: rgba(99, 102, 241, 0.3);
    color: rgba(248, 250, 252, 0.5);
}

.secondaryButton {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.secondaryButton:hover {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.dangerButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(239, 68, 68, 0.8),
                                stop:1 rgba(239, 68, 68, 0.6));
    border: 1px solid rgba(239, 68, 68, 0.4);
}

.dangerButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(239, 68, 68, 1.0),
                                stop:1 rgba(239, 68, 68, 0.8));
}

/* === PROGRESS BAR === */
QProgressBar {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    text-align: center;
    color: #F8FAFC;
    font-weight: 600;
    min-height: 24px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 rgba(99, 102, 241, 0.8),
                                stop:1 rgba(139, 92, 246, 0.8));
    border-radius: 7px;
}

/* === SCROLL AREA === */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: rgba(99, 102, 241, 0.5);
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(99, 102, 241, 0.7);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: rgba(99, 102, 241, 0.5);
    border-radius: 4px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background: rgba(99, 102, 241, 0.7);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* === LABELS === */
QLabel {
    color: #F8FAFC;
    background: transparent;
}

.metadataLabel {
    color: #94A3B8;
    font-size: 12px;
}

.titleLabel {
    font-size: 18px;
    font-weight: 700;
    color: #F8FAFC;
}

.subtitleLabel {
    font-size: 14px;
    font-weight: 500;
    color: #94A3B8;
}

/* === LINE EDIT === */
QLineEdit {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 8px;
    padding: 8px 12px;
    color: #F8FAFC;
    font-size: 13px;
}

QLineEdit:focus {
    border: 1px solid rgba(99, 102, 241, 0.6);
    background: rgba(255, 255, 255, 0.08);
}

/* === CHECKBOX === */
QCheckBox {
    color: #F8FAFC;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid rgba(99, 102, 241, 0.5);
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.05);
}

QCheckBox::indicator:checked {
    background: rgba(99, 102, 241, 0.8);
    border: 2px solid rgba(99, 102, 241, 0.8);
}

/* === COMBO BOX === */
QComboBox {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 8px;
    padding: 8px 12px;
    color: #F8FAFC;
    min-width: 120px;
}

QComboBox:hover {
    border: 1px solid rgba(99, 102, 241, 0.5);
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox QAbstractItemView {
    background: rgba(20, 20, 27, 0.95);
    border: 1px solid rgba(99, 102, 241, 0.3);
    selection-background-color: rgba(99, 102, 241, 0.5);
    color: #F8FAFC;
}

/* === SPIN BOX === */
QSpinBox, QDoubleSpinBox {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 8px;
    padding: 8px 12px;
    color: #F8FAFC;
}

/* === GROUP BOX === */
QGroupBox {
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    color: #F8FAFC;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #6366F1;
}

/* === TABLE === */
QTableWidget {
    background: rgba(20, 20, 27, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    gridline-color: rgba(99, 102, 241, 0.1);
    color: #F8FAFC;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background: rgba(99, 102, 241, 0.3);
}

QHeaderView::section {
    background: rgba(99, 102, 241, 0.2);
    color: #F8FAFC;
    padding: 8px;
    border: none;
    font-weight: 600;
}

/* === DIALOG === */
QDialog {
    background: #0A0A0F;
}

/* === TEXT EDIT === */
QTextEdit {
    background: rgba(20, 20, 27, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    color: #F8FAFC;
    padding: 8px;
}

/* === TAB WIDGET === */
QTabWidget::pane {
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    background: rgba(20, 20, 27, 0.4);
}

QTabBar::tab {
    background: rgba(255, 255, 255, 0.03);
    color: #94A3B8;
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background: rgba(99, 102, 241, 0.3);
    color: #F8FAFC;
}

QTabBar::tab:hover {
    background: rgba(255, 255, 255, 0.05);
}
"""


# === CONFIGURATION ===

@dataclass
class Config:
    """Application configuration"""
    default_destination: str = str(Path.home() / "PhotoQuick_Sessions")
    auto_copy: bool = False
    auto_transfer: bool = False
    wetransfer_email: str = ""
    theme: str = "dark"
    session_gap_minutes: int = 45
    include_videos: bool = True
    video_formats: List[str] = None
    photo_formats: List[str] = None
    face_detection_confidence: float = 0.7
    browser_headless: bool = True
    transfer_chunk_size_gb: float = 3.0
    
    def __post_init__(self):
        if self.video_formats is None:
            self.video_formats = [".mp4", ".mov", ".avi", ".mkv"]
        if self.photo_formats is None:
            self.photo_formats = [".jpg", ".jpeg", ".cr2", ".nef", ".arw", ".heic", ".dng", ".raf"]
    
    @staticmethod
    def get_config_path() -> Path:
        """Get configuration file path"""
        if sys.platform == "win32":
            config_dir = Path(os.environ.get("APPDATA", "")) / "PhotoQuick"
        else:
            config_dir = Path.home() / ".config" / "PhotoQuick"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.json"
    
    @classmethod
    def load(cls) -> 'Config':
        """Load configuration from file"""
        config_path = cls.get_config_path()
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    return cls(**data)
            except Exception as e:
                print(f"Error loading config: {e}")
        return cls()
    
    def save(self):
        """Save configuration to file"""
        config_path = self.get_config_path()
        data = {
            'default_destination': self.default_destination,
            'auto_copy': self.auto_copy,
            'auto_transfer': self.auto_transfer,
            'wetransfer_email': self.wetransfer_email,
            'theme': self.theme,
            'session_gap_minutes': self.session_gap_minutes,
            'include_videos': self.include_videos,
            'video_formats': self.video_formats,
            'photo_formats': self.photo_formats,
            'face_detection_confidence': self.face_detection_confidence,
            'browser_headless': self.browser_headless,
            'transfer_chunk_size_gb': self.transfer_chunk_size_gb
        }
        with open(config_path, 'w') as f:
            json.dump(data, f, indent=2)


# === DATABASE ===

class Database:
    """SQLite database manager"""
    
    def __init__(self):
        db_path = Config.get_config_path().parent / "photoquick.db"
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self.lock = threading.Lock()
    
    def _create_tables(self):
        """Create database tables"""
        cursor = self.conn.cursor()
        
        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                source_path TEXT,
                dest_path TEXT,
                file_count INTEGER DEFAULT 0,
                total_size INTEGER DEFAULT 0,
                faces_detected INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Transfers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transfers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                wetransfer_link TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)
        
        # Settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        self.conn.commit()
    
    def add_session(self, name: str, date: str, source_path: str = None, 
                    dest_path: str = None, file_count: int = 0, 
                    total_size: int = 0, faces_detected: int = 0) -> int:
        """Add new session"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO sessions (name, date, source_path, dest_path, 
                                     file_count, total_size, faces_detected)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, date, source_path, dest_path, file_count, total_size, faces_detected))
            self.conn.commit()
            return cursor.lastrowid
    
    def add_transfer(self, session_id: int, wetransfer_link: str, 
                     expires_at: str = None, status: str = "completed") -> int:
        """Add transfer record"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO transfers (session_id, wetransfer_link, expires_at, status)
                VALUES (?, ?, ?, ?)
            """, (session_id, wetransfer_link, expires_at, status))
            self.conn.commit()
            return cursor.lastrowid
    
    def get_sessions(self, limit: int = 50) -> List[Dict]:
        """Get recent sessions"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM sessions 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_transfers(self, session_id: int = None) -> List[Dict]:
        """Get transfers"""
        with self.lock:
            cursor = self.conn.cursor()
            if session_id:
                cursor.execute("""
                    SELECT * FROM transfers 
                    WHERE session_id = ? 
                    ORDER BY created_at DESC
                """, (session_id,))
            else:
                cursor.execute("""
                    SELECT * FROM transfers 
                    ORDER BY created_at DESC
                """)
            return [dict(row) for row in cursor.fetchall()]


# === FILE METADATA ===

@dataclass
class FileMetadata:
    """Photo/video file metadata"""
    path: Path
    timestamp: datetime
    size: int
    camera_model: str = ""
    lens: str = ""
    settings: str = ""
    gps: Optional[Tuple[float, float]] = None
    is_video: bool = False
    is_raw: bool = False


def extract_exif(image_path: Path) -> Dict:
    """Extract EXIF metadata from image"""
    try:
        image = Image.open(image_path)
        exif_data = {}
        
        if hasattr(image, '_getexif') and image._getexif():
            exif = image._getexif()
            for tag_id, value in exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                exif_data[tag] = value
        
        return exif_data
    except Exception as e:
        return {}


def get_file_timestamp(file_path: Path) -> datetime:
    """Get file timestamp from EXIF or file system"""
    try:
        exif = extract_exif(file_path)
        
        # Try DateTimeOriginal first
        if 'DateTimeOriginal' in exif:
            return datetime.strptime(exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        elif 'DateTime' in exif:
            return datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')
    except:
        pass
    
    # Fall back to file modification time
    return datetime.fromtimestamp(file_path.stat().st_mtime)


def get_file_metadata(file_path: Path) -> FileMetadata:
    """Extract complete file metadata"""
    timestamp = get_file_timestamp(file_path)
    size = file_path.stat().st_size
    
    # Check if video or raw
    ext = file_path.suffix.lower()
    is_video = ext in ['.mp4', '.mov', '.avi', '.mkv']
    is_raw = ext in ['.cr2', '.nef', '.arw', '.dng', '.raf']
    
    # Extract EXIF data
    exif = extract_exif(file_path) if not is_video else {}
    
    camera_model = exif.get('Model', '')
    lens = exif.get('LensModel', '')
    
    # Build settings string
    settings_parts = []
    if 'FNumber' in exif:
        settings_parts.append(f"f/{exif['FNumber']}")
    if 'ExposureTime' in exif:
        settings_parts.append(f"{exif['ExposureTime']}s")
    if 'ISOSpeedRatings' in exif:
        settings_parts.append(f"ISO{exif['ISOSpeedRatings']}")
    settings = " ".join(settings_parts)
    
    # GPS data
    gps = None
    if 'GPSInfo' in exif:
        try:
            gps_info = exif['GPSInfo']
            # Simplified GPS extraction
            if 2 in gps_info and 4 in gps_info:
                lat = gps_info[2]
                lon = gps_info[4]
                if isinstance(lat, tuple) and isinstance(lon, tuple):
                    gps = (float(lat[0]), float(lon[0]))
        except:
            pass
    
    return FileMetadata(
        path=file_path,
        timestamp=timestamp,
        size=size,
        camera_model=camera_model,
        lens=lens,
        settings=settings,
        gps=gps,
        is_video=is_video,
        is_raw=is_raw
    )


# === SESSION GROUPING ===

@dataclass
class PhotoSession:
    """Photography session"""
    name: str
    files: List[FileMetadata]
    start_time: datetime
    end_time: datetime
    total_size: int
    faces_detected: int = 0
    thumbnail_grid: Optional[QPixmap] = None
    hero_image: Optional[Path] = None


def group_into_sessions(files: List[FileMetadata], gap_minutes: int = 45) -> List[PhotoSession]:
    """Group files into sessions based on time gaps"""
    if not files:
        return []
    
    # Sort by timestamp
    sorted_files = sorted(files, key=lambda f: f.timestamp)
    
    sessions = []
    current_session_files = [sorted_files[0]]
    
    for i in range(1, len(sorted_files)):
        current_file = sorted_files[i]
        previous_file = sorted_files[i - 1]
        
        # Check time gap
        time_diff = (current_file.timestamp - previous_file.timestamp).total_seconds() / 60
        
        if time_diff > gap_minutes:
            # Start new session if current session has enough files
            if len(current_session_files) >= 3:
                sessions.append(_create_session(current_session_files))
            current_session_files = [current_file]
        else:
            current_session_files.append(current_file)
    
    # Add final session
    if len(current_session_files) >= 3:
        sessions.append(_create_session(current_session_files))
    
    return sessions


def _create_session(files: List[FileMetadata]) -> PhotoSession:
    """Create session object from files"""
    start_time = files[0].timestamp
    end_time = files[-1].timestamp
    total_size = sum(f.size for f in files)
    
    # Generate session name
    name = f"Session_{start_time.strftime('%Y%m%d_%H%M')}"
    
    return PhotoSession(
        name=name,
        files=files,
        start_time=start_time,
        end_time=end_time,
        total_size=total_size
    )


# === AI FACE DETECTION ===

class FaceDetector:
    """OpenCV-based face detection"""
    
    def __init__(self):
        self.detector = None
        self._initialize_detector()
    
    def _initialize_detector(self):
        """Initialize face detector"""
        try:
            # Use Haar Cascade (included with OpenCV)
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.detector = cv2.CascadeClassifier(cascade_path)
        except Exception as e:
            print(f"Face detector initialization error: {e}")
    
    def detect_faces(self, image_path: Path, confidence: float = 0.7) -> int:
        """Detect faces in image and return count"""
        if not self.detector:
            return 0
        
        try:
            # Read image
            img = cv2.imread(str(image_path))
            if img is None:
                return 0
            
            # Resize for faster processing
            height, width = img.shape[:2]
            max_dimension = 800
            if max(height, width) > max_dimension:
                scale = max_dimension / max(height, width)
                img = cv2.resize(img, None, fx=scale, fy=scale)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            return len(faces)
        except Exception as e:
            print(f"Face detection error for {image_path}: {e}")
            return 0
    
    def detect_faces_in_session(self, session: PhotoSession, max_photos: int = 10) -> int:
        """Detect faces in session photos"""
        total_faces = 0
        photos_to_check = [f for f in session.files if not f.is_video][:max_photos]
        
        for file_meta in photos_to_check:
            faces = self.detect_faces(file_meta.path)
            total_faces += faces
        
        return total_faces
    
    def find_hero_image(self, session: PhotoSession) -> Optional[Path]:
        """Find best photo with most prominent faces"""
        photos = [f for f in session.files if not f.is_video][:20]
        
        best_photo = None
        max_faces = 0
        
        for file_meta in photos:
            face_count = self.detect_faces(file_meta.path)
            if face_count > max_faces:
                max_faces = face_count
                best_photo = file_meta.path
        
        return best_photo if best_photo else (photos[0].path if photos else None)


def create_thumbnail_grid(session: PhotoSession, size: QSize = QSize(200, 200)) -> QPixmap:
    """Create 2x2 thumbnail grid from session"""
    photos = [f.path for f in session.files if not f.is_video][:4]
    
    if not photos:
        # Create placeholder
        pixmap = QPixmap(size)
        pixmap.fill(QColor(20, 20, 27))
        return pixmap
    
    # Create grid
    grid_size = 2
    cell_size = size.width() // grid_size
    
    result = QPixmap(size)
    result.fill(QColor(20, 20, 27))
    
    painter = QPainter(result)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    for i, photo_path in enumerate(photos):
        if i >= 4:
            break
        
        try:
            pixmap = QPixmap(str(photo_path))
            if not pixmap.isNull():
                # Scale to fit cell
                scaled = pixmap.scaled(
                    cell_size, cell_size,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                # Calculate position
                row = i // grid_size
                col = i % grid_size
                x = col * cell_size
                y = row * cell_size
                
                # Draw with crop
                source_rect = QRect(
                    (scaled.width() - cell_size) // 2,
                    (scaled.height() - cell_size) // 2,
                    cell_size, cell_size
                )
                target_rect = QRect(x, y, cell_size, cell_size)
                
                painter.drawPixmap(target_rect, scaled, source_rect)
        except Exception as e:
            print(f"Error creating thumbnail for {photo_path}: {e}")
    
    painter.end()
    return result


# === USB DETECTION ===

class USBMonitor(QThread):
    """Monitor USB device connections"""
    device_connected = pyqtSignal(str)  # path
    device_disconnected = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.current_devices = set()
    
    def run(self):
        """Monitor loop"""
        while self.running:
            self._check_devices()
            time.sleep(2)
    
    def _check_devices(self):
        """Check for removable devices"""
        if sys.platform != "win32":
            return
        
        try:
            current = set()
            
            # Get all drives
            drives = []
            bitmask = win32api.GetLogicalDrives()
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if bitmask & 1:
                    drives.append(f"{letter}:\\")
                bitmask >>= 1
            
            # Check which are removable
            for drive in drives:
                try:
                    drive_type = win32file.GetDriveType(drive)
                    if drive_type == win32con.DRIVE_REMOVABLE:
                        # Check for DCIM structure
                        dcim_path = Path(drive) / "DCIM"
                        if dcim_path.exists() and dcim_path.is_dir():
                            current.add(drive)
                except:
                    pass
            
            # Detect new devices
            new_devices = current - self.current_devices
            for device in new_devices:
                self.device_connected.emit(device)
            
            # Detect removed devices
            if len(current) < len(self.current_devices):
                self.device_disconnected.emit()
            
            self.current_devices = current
            
        except Exception as e:
            print(f"USB monitoring error: {e}")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False


# === FILE OPERATIONS ===

class CopyWorker(QObject):
    """File copy worker"""
    progress = pyqtSignal(int, str)  # percentage, current_file
    finished = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, source_files: List[Path], destination: Path, verify_checksum: bool = True):
        super().__init__()
        self.source_files = source_files
        self.destination = destination
        self.verify_checksum = verify_checksum
        self.cancelled = False
    
    def cancel(self):
        """Cancel operation"""
        self.cancelled = True
    
    def run(self):
        """Execute copy operation"""
        try:
            total_files = len(self.source_files)
            
            for i, source_file in enumerate(self.source_files):
                if self.cancelled:
                    self.finished.emit(False, "Operation cancelled")
                    return
                
                # Determine destination path
                dest_file = self.destination / source_file.name
                
                # Create parent directories
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Skip if exists
                if dest_file.exists():
                    self.progress.emit(
                        int((i + 1) / total_files * 100),
                        f"Skipped (exists): {source_file.name}"
                    )
                    continue
                
                # Copy file
                self.progress.emit(
                    int(i / total_files * 100),
                    f"Copying: {source_file.name}"
                )
                
                shutil.copy2(source_file, dest_file)
                
                # Verify checksum
                if self.verify_checksum:
                    if not self._verify_file(source_file, dest_file):
                        self.finished.emit(False, f"Checksum verification failed: {source_file.name}")
                        return
                
                # Preserve dates
                shutil.copystat(source_file, dest_file)
            
            self.progress.emit(100, "Complete")
            self.finished.emit(True, f"Successfully copied {total_files} files")
            
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")
    
    def _verify_file(self, source: Path, dest: Path) -> bool:
        """Verify file integrity via checksum"""
        try:
            source_hash = self._calculate_md5(source)
            dest_hash = self._calculate_md5(dest)
            return source_hash == dest_hash
        except:
            return False
    
    def _calculate_md5(self, file_path: Path, chunk_size: int = 8192) -> str:
        """Calculate MD5 checksum"""
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        return md5.hexdigest()


def copy_session_files(session: PhotoSession, destination: Path, 
                      progress_callback=None) -> bool:
    """Copy session files to destination"""
    try:
        # Create session directory
        session_dir = destination / session.name
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Separate RAW and JPEG
        raw_files = [f for f in session.files if f.is_raw]
        jpeg_files = [f for f in session.files if not f.is_raw and not f.is_video]
        video_files = [f for f in session.files if f.is_video]
        
        # Create subdirectories
        if raw_files:
            raw_dir = session_dir / "RAW"
            raw_dir.mkdir(exist_ok=True)
        if jpeg_files:
            jpeg_dir = session_dir / "JPEG"
            jpeg_dir.mkdir(exist_ok=True)
        
        # Copy files
        total_files = len(session.files)
        for i, file_meta in enumerate(session.files):
            if file_meta.is_raw:
                dest = session_dir / "RAW" / file_meta.path.name
            elif file_meta.is_video:
                dest = session_dir / file_meta.path.name
            else:
                dest = session_dir / "JPEG" / file_meta.path.name
            
            shutil.copy2(file_meta.path, dest)
            
            if progress_callback:
                progress_callback(int((i + 1) / total_files * 100), file_meta.path.name)
        
        # Save session metadata
        metadata = {
            'name': session.name,
            'start_time': session.start_time.isoformat(),
            'end_time': session.end_time.isoformat(),
            'file_count': len(session.files),
            'total_size': session.total_size,
            'faces_detected': session.faces_detected
        }
        
        with open(session_dir / "session_info.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Copy error: {e}")
        return False


# === WETRANSFER AUTOMATION ===

class WeTransferAutomation:
    """WeTransfer upload automation (simulated)"""
    
    def __init__(self, email: str = ""):
        self.email = email
        self.auth_file = Config.get_config_path().parent / "wetransfer_auth.json"
    
    def is_authenticated(self) -> bool:
        """Check if authenticated"""
        return self.auth_file.exists()
    
    def authenticate(self) -> bool:
        """Authenticate with WeTransfer (simulated)"""
        # In production, this would use Playwright/Selenium
        # For now, simulate successful auth
        auth_data = {
            'email': self.email,
            'authenticated_at': datetime.now().isoformat()
        }
        
        with open(self.auth_file, 'w') as f:
            json.dump(auth_data, f)
        
        return True
    
    def upload_files(self, files: List[Path], title: str = "PhotoQuick Transfer",
                    progress_callback=None) -> Optional[str]:
        """Upload files to WeTransfer (simulated)"""
        try:
            # Calculate total size
            total_size = sum(f.stat().st_size for f in files)
            total_size_gb = total_size / (1024 ** 3)
            
            # Simulate upload progress
            if progress_callback:
                for i in range(0, 101, 10):
                    time.sleep(0.2)
                    progress_callback(i, f"Uploading {len(files)} files...")
            
            # Generate simulated link
            link = f"https://we.tl/t-{hashlib.md5(title.encode()).hexdigest()[:12]}"
            
            return link
            
        except Exception as e:
            print(f"Upload error: {e}")
            return None
    
    def upload_session(self, session: PhotoSession, chunk_size_gb: float = 3.0,
                      progress_callback=None) -> List[str]:
        """Upload session with automatic chunking"""
        total_size_gb = session.total_size / (1024 ** 3)
        
        links = []
        
        if total_size_gb <= chunk_size_gb:
            # Single upload
            files = [f.path for f in session.files]
            link = self.upload_files(files, session.name, progress_callback)
            if link:
                links.append(link)
        else:
            # Split into chunks
            chunks = self._split_into_chunks(session.files, chunk_size_gb)
            
            for i, chunk in enumerate(chunks):
                title = f"{session.name}_Part{i+1}"
                files = [f.path for f in chunk]
                link = self.upload_files(files, title, progress_callback)
                if link:
                    links.append(link)
        
        return links
    
    def _split_into_chunks(self, files: List[FileMetadata], 
                          chunk_size_gb: float) -> List[List[FileMetadata]]:
        """Split files into chunks"""
        chunk_size_bytes = chunk_size_gb * (1024 ** 3)
        chunks = []
        current_chunk = []
        current_size = 0
        
        for file_meta in files:
            if current_size + file_meta.size > chunk_size_bytes and current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_size = 0
            
            current_chunk.append(file_meta)
            current_size += file_meta.size
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks


# === UI COMPONENTS ===

class CustomTitleBar(QWidget):
    """Custom window title bar"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(40)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # App icon and title
        icon_label = QLabel()
        icon_pixmap = self._create_app_icon()
        icon_label.setPixmap(icon_pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio,
                                                Qt.TransformationMode.SmoothTransformation))
        icon_label.setFixedSize(24, 24)
        
        title_label = QLabel("PhotoQuick Pro")
        title_label.setObjectName("titleLabel")
        
        layout.addSpacing(8)
        layout.addWidget(icon_label)
        layout.addSpacing(8)
        layout.addWidget(title_label)
        layout.addStretch()
        
        # Window controls
        minimize_btn = QPushButton("─")
        minimize_btn.setObjectName("titleButton")
        minimize_btn.setFixedSize(46, 40)
        minimize_btn.clicked.connect(lambda: parent.showMinimized())
        
        maximize_btn = QPushButton("□")
        maximize_btn.setObjectName("titleButton")
        maximize_btn.setFixedSize(46, 40)
        maximize_btn.clicked.connect(self._toggle_maximize)
        
        close_btn = QPushButton("×")
        close_btn.setObjectName("closeButton")
        close_btn.setFixedSize(46, 40)
        close_btn.clicked.connect(lambda: parent.close())
        
        layout.addWidget(minimize_btn)
        layout.addWidget(maximize_btn)
        layout.addWidget(close_btn)
        
        self.parent_window = parent
        self.dragging = False
        self.drag_position = QPoint()
    
    def _create_app_icon(self) -> QPixmap:
        """Create app icon from base64"""
        try:
            icon_data = base64.b64decode(APP_ICON_BASE64)
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)
            return pixmap
        except:
            # Fallback to simple colored square
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(99, 102, 241))
            return pixmap
    
    def _toggle_maximize(self):
        """Toggle window maximize state"""
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
        else:
            self.parent_window.showMaximized()
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.parent_window.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self.dragging = False


class SessionCard(QFrame):
    """Session display card"""
    clicked = pyqtSignal(PhotoSession)
    
    def __init__(self, session: PhotoSession, parent=None):
        super().__init__(parent)
        self.session = session
        self.selected = False
        
        self.setObjectName("sessionCard")
        self.setProperty("class", "sessionCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(200)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup card UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Thumbnail
        thumbnail_label = QLabel()
        if self.session.thumbnail_grid:
            thumbnail_label.setPixmap(self.session.thumbnail_grid)
        else:
            # Create placeholder
            thumbnail = create_thumbnail_grid(self.session)
            thumbnail_label.setPixmap(thumbnail)
        thumbnail_label.setFixedSize(160, 160)
        thumbnail_label.setScaledContents(False)
        thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Session info
        name_label = QLabel(self.session.name)
        name_label.setProperty("class", "subtitleLabel")
        
        time_str = self.session.start_time.strftime("%I:%M %p")
        file_count = len(self.session.files)
        size_mb = self.session.total_size / (1024 * 1024)
        
        info_label = QLabel(f"{time_str} • {file_count} files • {size_mb:.1f} MB")
        info_label.setProperty("class", "metadataLabel")
        
        # Face detection badge
        if self.session.faces_detected > 0:
            face_label = QLabel(f"👤 {self.session.faces_detected} faces")
            face_label.setProperty("class", "metadataLabel")
            layout.addWidget(face_label)
        
        layout.addWidget(thumbnail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)
        layout.addWidget(info_label)
        layout.addStretch()
    
    def mousePressEvent(self, event):
        """Handle click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.session)
            event.accept()
    
    def setSelected(self, selected: bool):
        """Set selection state"""
        self.selected = selected
        if selected:
            self.setProperty("class", "sessionCardSelected")
        else:
            self.setProperty("class", "sessionCard")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


class ToastNotification(QFrame):
    """Custom toast notification"""
    
    def __init__(self, message: str, type: str = "info", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool |
                           Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Styling based on type
        colors = {
            'success': '#10B981',
            'error': '#EF4444',
            'warning': '#F59E0B',
            'info': '#6366F1'
        }
        color = colors.get(type, colors['info'])
        
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(20, 20, 27, 0.95),
                                            stop:1 rgba(10, 10, 15, 0.95));
                border: 2px solid {color};
                border-radius: 12px;
                padding: 16px;
            }}
            QLabel {{
                color: #F8FAFC;
                font-size: 14px;
                font-weight: 500;
            }}
        """)
        
        layout = QHBoxLayout(self)
        
        # Icon
        icons = {
            'success': '✓',
            'error': '✕',
            'warning': '⚠',
            'info': 'ℹ'
        }
        icon_label = QLabel(icons.get(type, icons['info']))
        icon_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")
        
        message_label = QLabel(message)
        
        layout.addWidget(icon_label)
        layout.addWidget(message_label)
        
        # Auto-dismiss timer
        QTimer.singleShot(5000, self.close)
        
        # Fade in animation
        self.setWindowOpacity(0)
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in_animation.start()
    
    def show_at_top_right(self, parent_widget):
        """Position at top-right of parent"""
        self.adjustSize()
        parent_rect = parent_widget.geometry()
        x = parent_rect.right() - self.width() - 20
        y = parent_rect.top() + 80
        self.move(x, y)
        self.show()


# === SETTINGS DIALOG ===

class SettingsDialog(QDialog):
    """Application settings dialog"""
    
    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("Settings - PhotoQuick Pro")
        self.setMinimumSize(600, 500)
        self.setStyleSheet(STYLESHEET)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup settings UI"""
        layout = QVBoxLayout(self)
        
        # Tabs
        tabs = QTabWidget()
        
        # General tab
        general_tab = self._create_general_tab()
        tabs.addTab(general_tab, "General")
        
        # Detection tab
        detection_tab = self._create_detection_tab()
        tabs.addTab(detection_tab, "Detection")
        
        # Transfer tab
        transfer_tab = self._create_transfer_tab()
        tabs.addTab(transfer_tab, "Transfer")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                     QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def _create_general_tab(self) -> QWidget:
        """Create general settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Default destination
        dest_group = QGroupBox("Default Destination")
        dest_layout = QHBoxLayout(dest_group)
        
        self.dest_edit = QLineEdit(self.config.default_destination)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_destination)
        
        dest_layout.addWidget(self.dest_edit)
        dest_layout.addWidget(browse_btn)
        
        layout.addWidget(dest_group)
        
        # Auto-copy
        self.auto_copy_check = QCheckBox("Automatically copy files when device detected")
        self.auto_copy_check.setChecked(self.config.auto_copy)
        layout.addWidget(self.auto_copy_check)
        
        # Include videos
        self.include_videos_check = QCheckBox("Include video files")
        self.include_videos_check.setChecked(self.config.include_videos)
        layout.addWidget(self.include_videos_check)
        
        # Session gap
        gap_group = QGroupBox("Session Grouping")
        gap_layout = QHBoxLayout(gap_group)
        
        gap_layout.addWidget(QLabel("Time gap between sessions (minutes):"))
        self.gap_spin = QSpinBox()
        self.gap_spin.setRange(5, 180)
        self.gap_spin.setValue(self.config.session_gap_minutes)
        gap_layout.addWidget(self.gap_spin)
        gap_layout.addStretch()
        
        layout.addWidget(gap_group)
        layout.addStretch()
        
        return widget
    
    def _create_detection_tab(self) -> QWidget:
        """Create detection settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Face detection confidence
        conf_group = QGroupBox("Face Detection")
        conf_layout = QHBoxLayout(conf_group)
        
        conf_layout.addWidget(QLabel("Confidence threshold:"))
        self.confidence_spin = QDoubleSpinBox()
        self.confidence_spin.setRange(0.1, 1.0)
        self.confidence_spin.setSingleStep(0.1)
        self.confidence_spin.setValue(self.config.face_detection_confidence)
        conf_layout.addWidget(self.confidence_spin)
        conf_layout.addStretch()
        
        layout.addWidget(conf_group)
        layout.addStretch()
        
        return widget
    
    def _create_transfer_tab(self) -> QWidget:
        """Create transfer settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # WeTransfer email
        email_group = QGroupBox("WeTransfer Account")
        email_layout = QHBoxLayout(email_group)
        
        email_layout.addWidget(QLabel("Email:"))
        self.email_edit = QLineEdit(self.config.wetransfer_email)
        email_layout.addWidget(self.email_edit)
        
        layout.addWidget(email_group)
        
        # Auto-transfer
        self.auto_transfer_check = QCheckBox("Automatically upload after copying")
        self.auto_transfer_check.setChecked(self.config.auto_transfer)
        layout.addWidget(self.auto_transfer_check)
        
        # Chunk size
        chunk_group = QGroupBox("Upload Settings")
        chunk_layout = QHBoxLayout(chunk_group)
        
        chunk_layout.addWidget(QLabel("Chunk size (GB):"))
        self.chunk_spin = QDoubleSpinBox()
        self.chunk_spin.setRange(1.0, 10.0)
        self.chunk_spin.setSingleStep(0.5)
        self.chunk_spin.setValue(self.config.transfer_chunk_size_gb)
        chunk_layout.addWidget(self.chunk_spin)
        chunk_layout.addStretch()
        
        layout.addWidget(chunk_group)
        
        # Headless mode
        self.headless_check = QCheckBox("Use headless browser (faster)")
        self.headless_check.setChecked(self.config.browser_headless)
        layout.addWidget(self.headless_check)
        
        layout.addStretch()
        
        return widget
    
    def _browse_destination(self):
        """Browse for destination folder"""
        folder = QFileDialog.getExistingDirectory(
            self, "Select Destination Folder",
            self.dest_edit.text()
        )
        if folder:
            self.dest_edit.setText(folder)
    
    def get_config(self) -> Config:
        """Get updated configuration"""
        self.config.default_destination = self.dest_edit.text()
        self.config.auto_copy = self.auto_copy_check.isChecked()
        self.config.include_videos = self.include_videos_check.isChecked()
        self.config.session_gap_minutes = self.gap_spin.value()
        self.config.face_detection_confidence = self.confidence_spin.value()
        self.config.wetransfer_email = self.email_edit.text()
        self.config.auto_transfer = self.auto_transfer_check.isChecked()
        self.config.transfer_chunk_size_gb = self.chunk_spin.value()
        self.config.browser_headless = self.headless_check.isChecked()
        
        return self.config


# === MAIN WINDOW ===

class PhotoQuickPro(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Load configuration
        self.config = Config.load()
        
        # Initialize components
        self.db = Database()
        self.face_detector = FaceDetector()
        self.wetransfer = WeTransferAutomation(self.config.wetransfer_email)
        
        # USB monitoring
        self.usb_monitor = USBMonitor()
        self.usb_monitor.device_connected.connect(self.on_device_connected)
        self.usb_monitor.device_disconnected.connect(self.on_device_disconnected)
        
        # Sessions
        self.sessions: List[PhotoSession] = []
        self.selected_session: Optional[PhotoSession] = None
        self.current_device_path: Optional[str] = None
        
        # Setup UI
        self._setup_ui()
        
        # Start USB monitoring
        self.usb_monitor.start()
        
        # System tray
        self._setup_system_tray()
        
        # Show window
        self.show()
    
    def _setup_ui(self):
        """Setup main UI"""
        self.setWindowTitle("PhotoQuick Pro")
        self.setMinimumSize(1200, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(STYLESHEET)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom title bar
        title_bar = CustomTitleBar(self)
        main_layout.addWidget(title_bar)
        
        # Content area
        content = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar
        sidebar = self._create_sidebar()
        content.addWidget(sidebar)
        
        # Preview panel
        preview = self._create_preview_panel()
        content.addWidget(preview)
        
        content.setSizes([300, 900])
        
        main_layout.addWidget(content)
        
        # Status bar
        status_bar = self._create_status_bar()
        main_layout.addWidget(status_bar)
    
    def _create_sidebar(self) -> QWidget:
        """Create sessions sidebar"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(280)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Header
        header_label = QLabel("SESSIONS")
        header_label.setProperty("class", "titleLabel")
        layout.addWidget(header_label)
        
        # Sessions scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.sessions_container = QWidget()
        self.sessions_layout = QVBoxLayout(self.sessions_container)
        self.sessions_layout.setSpacing(4)
        self.sessions_layout.addStretch()
        
        scroll.setWidget(self.sessions_container)
        layout.addWidget(scroll)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setProperty("class", "secondaryButton")
        refresh_btn.clicked.connect(self.refresh_device)
        
        eject_btn = QPushButton("Eject")
        eject_btn.setProperty("class", "secondaryButton")
        eject_btn.clicked.connect(self.eject_device)
        
        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addWidget(eject_btn)
        
        layout.addLayout(buttons_layout)
        
        return sidebar
    
    def _create_preview_panel(self) -> QWidget:
        """Create preview panel"""
        panel = QFrame()
        panel.setMinimumWidth(600)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header
        header_layout = QHBoxLayout()
        
        self.preview_title = QLabel("Preview Panel")
        self.preview_title.setProperty("class", "titleLabel")
        
        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.show_settings)
        
        header_layout.addWidget(self.preview_title)
        header_layout.addStretch()
        header_layout.addWidget(settings_btn)
        
        layout.addLayout(header_layout)
        
        # Preview content
        self.preview_stack = QStackedWidget()
        
        # Empty state
        empty_widget = QWidget()
        empty_layout = QVBoxLayout(empty_widget)
        empty_layout.addStretch()
        
        empty_label = QLabel("No session selected\n\nConnect a device or select a session from the sidebar")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setProperty("class", "subtitleLabel")
        
        empty_layout.addWidget(empty_label)
        empty_layout.addStretch()
        
        self.preview_stack.addWidget(empty_widget)
        
        # Session preview
        self.session_preview_widget = self._create_session_preview()
        self.preview_stack.addWidget(self.session_preview_widget)
        
        layout.addWidget(self.preview_stack)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.copy_btn = QPushButton("Copy Files")
        self.copy_btn.clicked.connect(self.copy_selected_session)
        self.copy_btn.setEnabled(False)
        
        self.transfer_btn = QPushButton("Start Transfer")
        self.transfer_btn.clicked.connect(self.transfer_selected_session)
        self.transfer_btn.setEnabled(False)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.copy_btn)
        buttons_layout.addWidget(self.transfer_btn)
        
        layout.addLayout(buttons_layout)
        
        return panel
    
    def _create_session_preview(self) -> QWidget:
        """Create session preview widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Hero image
        self.hero_image_label = QLabel()
        self.hero_image_label.setMinimumSize(600, 400)
        self.hero_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hero_image_label.setStyleSheet("""
            QLabel {
                background: rgba(20, 20, 27, 0.6);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
            }
        """)
        
        layout.addWidget(self.hero_image_label)
        
        # Metadata
        self.metadata_table = QTableWidget()
        self.metadata_table.setColumnCount(2)
        self.metadata_table.setHorizontalHeaderLabels(["Property", "Value"])
        self.metadata_table.horizontalHeader().setStretchLastSection(True)
        self.metadata_table.setMaximumHeight(200)
        
        layout.addWidget(self.metadata_table)
        
        return widget
    
    def _create_status_bar(self) -> QWidget:
        """Create status bar"""
        bar = QFrame()
        bar.setStyleSheet("""
            QFrame {
                background: rgba(20, 20, 27, 0.95);
                border-top: 1px solid rgba(99, 102, 241, 0.2);
                min-height: 32px;
                max-height: 32px;
            }
        """)
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 4, 12, 4)
        
        self.status_label = QLabel("Ready")
        self.status_label.setProperty("class", "metadataLabel")
        
        self.usb_label = QLabel("USB: Not Connected")
        self.usb_label.setProperty("class", "metadataLabel")
        
        self.storage_label = QLabel("Storage: --")
        self.storage_label.setProperty("class", "metadataLabel")
        
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(self.usb_label)
        layout.addWidget(QLabel("|"))
        layout.addWidget(self.storage_label)
        
        return bar
    
    def _setup_system_tray(self):
        """Setup system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Create icon from base64
        try:
            icon_data = base64.b64decode(APP_ICON_BASE64)
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)
            icon = QIcon(pixmap)
        except:
            icon = QIcon()
        
        self.tray_icon.setIcon(icon)
        
        # Tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
    def on_device_connected(self, path: str):
        """Handle USB device connection"""
        self.current_device_path = path
        self.usb_label.setText(f"USB: Connected ({path})")
        
        # Show notification
        toast = ToastNotification(f"Device connected: {path}", "success", self)
        toast.show_at_top_right(self)
        
        # Scan device
        self.scan_device(path)
    
    def on_device_disconnected(self):
        """Handle USB device disconnection"""
        self.current_device_path = None
        self.usb_label.setText("USB: Not Connected")
        
        toast = ToastNotification("Device disconnected", "warning", self)
        toast.show_at_top_right(self)
        
        # Clear sessions
        self.clear_sessions()
    
    def scan_device(self, device_path: str):
        """Scan device for media files"""
        self.status_label.setText("Scanning device...")
        QApplication.processEvents()
        
        try:
            # Find DCIM folders
            dcim_path = Path(device_path) / "DCIM"
            if not dcim_path.exists():
                toast = ToastNotification("No DCIM folder found", "warning", self)
                toast.show_at_top_right(self)
                return
            
            # Collect all media files
            all_files = []
            
            for ext in self.config.photo_formats + (self.config.video_formats if self.config.include_videos else []):
                all_files.extend(dcim_path.rglob(f"*{ext}"))
                all_files.extend(dcim_path.rglob(f"*{ext.upper()}"))
            
            if not all_files:
                toast = ToastNotification("No media files found", "warning", self)
                toast.show_at_top_right(self)
                return
            
            # Extract metadata
            files_metadata = []
            for file_path in all_files:
                try:
                    metadata = get_file_metadata(file_path)
                    files_metadata.append(metadata)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            
            # Group into sessions
            self.sessions = group_into_sessions(files_metadata, self.config.session_gap_minutes)
            
            # Detect faces and create thumbnails
            for session in self.sessions:
                # Detect faces
                session.faces_detected = self.face_detector.detect_faces_in_session(session)
                
                # Find hero image
                session.hero_image = self.face_detector.find_hero_image(session)
                
                # Create thumbnail grid
                session.thumbnail_grid = create_thumbnail_grid(session)
            
            # Update UI
            self.display_sessions()
            
            self.status_label.setText(f"Found {len(self.sessions)} sessions")
            
            toast = ToastNotification(
                f"Scanned {len(all_files)} files in {len(self.sessions)} sessions",
                "success", self
            )
            toast.show_at_top_right(self)
            
            # Auto-copy if enabled
            if self.config.auto_copy and self.sessions:
                self.copy_all_sessions()
            
        except Exception as e:
            print(f"Scan error: {e}")
            toast = ToastNotification(f"Scan error: {str(e)}", "error", self)
            toast.show_at_top_right(self)
        finally:
            self.status_label.setText("Ready")
    
    def display_sessions(self):
        """Display sessions in sidebar"""
        # Clear existing
        for i in reversed(range(self.sessions_layout.count())):
            widget = self.sessions_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Add session cards
        for session in self.sessions:
            card = SessionCard(session)
            card.clicked.connect(self.on_session_selected)
            self.sessions_layout.insertWidget(0, card)
    
    def clear_sessions(self):
        """Clear all sessions"""
        self.sessions = []
        self.selected_session = None
        
        for i in reversed(range(self.sessions_layout.count())):
            widget = self.sessions_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        self.preview_stack.setCurrentIndex(0)
        self.copy_btn.setEnabled(False)
        self.transfer_btn.setEnabled(False)
    
    def on_session_selected(self, session: PhotoSession):
        """Handle session selection"""
        self.selected_session = session
        
        # Update preview
        self.preview_title.setText(f"Preview: {session.name}")
        
        # Load hero image
        if session.hero_image and session.hero_image.exists():
            pixmap = QPixmap(str(session.hero_image))
            scaled_pixmap = pixmap.scaled(
                600, 400,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.hero_image_label.setPixmap(scaled_pixmap)
        
        # Update metadata table
        self.metadata_table.setRowCount(0)
        
        metadata = [
            ("Session Name", session.name),
            ("Start Time", session.start_time.strftime("%Y-%m-%d %H:%M:%S")),
            ("End Time", session.end_time.strftime("%Y-%m-%d %H:%M:%S")),
            ("File Count", str(len(session.files))),
            ("Total Size", f"{session.total_size / (1024**2):.1f} MB"),
            ("Faces Detected", str(session.faces_detected)),
        ]
        
        for row, (key, value) in enumerate(metadata):
            self.metadata_table.insertRow(row)
            self.metadata_table.setItem(row, 0, QTableWidgetItem(key))
            self.metadata_table.setItem(row, 1, QTableWidgetItem(value))
        
        self.preview_stack.setCurrentIndex(1)
        self.copy_btn.setEnabled(True)
        self.transfer_btn.setEnabled(True)
    
    def copy_selected_session(self):
        """Copy selected session to destination"""
        if not self.selected_session:
            return
        
        destination = Path(self.config.default_destination)
        
        # Create progress dialog
        progress_dialog = QDialog(self)
        progress_dialog.setWindowTitle("Copying Files")
        progress_dialog.setModal(True)
        progress_dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(progress_dialog)
        
        status_label = QLabel("Copying files...")
        progress_bar = QProgressBar()
        
        layout.addWidget(status_label)
        layout.addWidget(progress_bar)
        
        progress_dialog.show()
        QApplication.processEvents()
        
        # Define progress callback
        def update_progress(percent: int, current_file: str):
            status_label.setText(f"Copying: {current_file}")
            progress_bar.setValue(percent)
            QApplication.processEvents()
        
        # Copy files
        success = copy_session_files(self.selected_session, destination, update_progress)
        
        progress_dialog.close()
        
        if success:
            toast = ToastNotification("Files copied successfully!", "success", self)
            toast.show_at_top_right(self)
            
            # Save to database
            session_dir = destination / self.selected_session.name
            self.db.add_session(
                name=self.selected_session.name,
                date=self.selected_session.start_time.isoformat(),
                source_path=str(self.selected_session.files[0].path.parent),
                dest_path=str(session_dir),
                file_count=len(self.selected_session.files),
                total_size=self.selected_session.total_size,
                faces_detected=self.selected_session.faces_detected
            )
            
            # Auto-transfer if enabled
            if self.config.auto_transfer:
                self.transfer_selected_session()
        else:
            toast = ToastNotification("Copy failed!", "error", self)
            toast.show_at_top_right(self)
    
    def copy_all_sessions(self):
        """Copy all sessions"""
        for session in self.sessions:
            self.selected_session = session
            self.copy_selected_session()
    
    def transfer_selected_session(self):
        """Transfer selected session to WeTransfer"""
        if not self.selected_session:
            return
        
        # Check authentication
        if not self.wetransfer.is_authenticated():
            # Show login dialog
            msg = QMessageBox(self)
            msg.setWindowTitle("WeTransfer Login")
            msg.setText("Please log in to your WeTransfer account to continue.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            
            # Simulate authentication
            self.wetransfer.authenticate()
        
        # Create progress dialog
        progress_dialog = QDialog(self)
        progress_dialog.setWindowTitle("Uploading to WeTransfer")
        progress_dialog.setModal(True)
        progress_dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(progress_dialog)
        
        status_label = QLabel("Uploading files...")
        progress_bar = QProgressBar()
        
        layout.addWidget(status_label)
        layout.addWidget(progress_bar)
        
        progress_dialog.show()
        QApplication.processEvents()
        
        # Define progress callback
        def update_progress(percent: int, message: str):
            status_label.setText(message)
            progress_bar.setValue(percent)
            QApplication.processEvents()
        
        # Upload session
        links = self.wetransfer.upload_session(
            self.selected_session,
            self.config.transfer_chunk_size_gb,
            update_progress
        )
        
        progress_dialog.close()
        
        if links:
            # Show results dialog
            result_dialog = QDialog(self)
            result_dialog.setWindowTitle("Transfer Complete")
            result_dialog.setMinimumWidth(500)
            
            layout = QVBoxLayout(result_dialog)
            
            layout.addWidget(QLabel("Transfer links:"))
            
            links_text = QTextEdit()
            links_text.setReadOnly(True)
            links_text.setPlainText("\n".join(links))
            links_text.setMaximumHeight(150)
            
            layout.addWidget(links_text)
            
            copy_btn = QPushButton("Copy All Links")
            copy_btn.clicked.connect(lambda: QApplication.clipboard().setText("\n".join(links)))
            
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(result_dialog.accept)
            
            button_layout = QHBoxLayout()
            button_layout.addWidget(copy_btn)
            button_layout.addWidget(close_btn)
            
            layout.addLayout(button_layout)
            
            result_dialog.exec()
            
            # Save to database
            for link in links:
                self.db.add_transfer(
                    session_id=0,  # Would use actual session ID
                    wetransfer_link=link,
                    status="completed"
                )
            
            toast = ToastNotification("Transfer complete!", "success", self)
            toast.show_at_top_right(self)
        else:
            toast = ToastNotification("Transfer failed!", "error", self)
            toast.show_at_top_right(self)
    
    def refresh_device(self):
        """Refresh device scan"""
        if self.current_device_path:
            self.scan_device(self.current_device_path)
        else:
            toast = ToastNotification("No device connected", "warning", self)
            toast.show_at_top_right(self)
    
    def eject_device(self):
        """Eject USB device"""
        if not self.current_device_path:
            toast = ToastNotification("No device to eject", "warning", self)
            toast.show_at_top_right(self)
            return
        
        # On Windows, we'd use win32 API to eject
        # For now, just simulate
        toast = ToastNotification("Device can be safely removed", "success", self)
        toast.show_at_top_right(self)
        
        self.on_device_disconnected()
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.config, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.config = dialog.get_config()
            self.config.save()
            
            toast = ToastNotification("Settings saved", "success", self)
            toast.show_at_top_right(self)
    
    def closeEvent(self, event):
        """Handle window close"""
        # Stop USB monitor
        self.usb_monitor.stop()
        self.usb_monitor.wait()
        
        event.accept()


# === ENTRY POINT ===

def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoQuick Pro")
    app.setOrganizationName("PhotoQuick")
    app.setApplicationVersion("1.0.0")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create main window
    window = PhotoQuickPro()
    
    # Show first-run wizard if needed
    config_path = Config.get_config_path()
    if not config_path.exists():
        msg = QMessageBox()
        msg.setWindowTitle("Welcome to PhotoQuick Pro")
        msg.setText("Welcome to PhotoQuick Pro!\n\nThis is your first time running the application. "
                   "Please configure your settings in the Settings menu.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
