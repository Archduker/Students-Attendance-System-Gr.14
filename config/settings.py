"""
Application Settings - Cấu hình chung
=====================================

File này chứa các hằng số và cấu hình chung cho toàn bộ ứng dụng.

Hướng dẫn:
- Không commit các giá trị nhạy cảm (API keys, passwords) vào Git
- Sử dụng biến môi trường hoặc file .env cho các giá trị nhạy cảm
"""

import os
from pathlib import Path

# =============================================================================
# APPLICATION INFO
# =============================================================================
APP_NAME = "Student Attendance System"
APP_VERSION = "1.0.0"
DEBUG = True  # Set False in production

# =============================================================================
# PATHS
# =============================================================================
# Base directory của project
BASE_DIR = Path(__file__).resolve().parent.parent

# Database directory
DATABASE_DIR = BASE_DIR / "database"

# Assets directory
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
ICONS_DIR = ASSETS_DIR / "icons"
FONTS_DIR = ASSETS_DIR / "fonts"

# =============================================================================
# ATTENDANCE SETTINGS
# =============================================================================
# Thời gian QR code có hiệu lực (giây)
QR_CODE_VALIDITY_SECONDS = 30

# Thời gian token có hiệu lực (phút)
TOKEN_VALIDITY_MINUTES = 5

# Thời gian cho phép điểm danh trễ (phút)
LATE_WINDOW_MINUTES = 15

# =============================================================================
# UI SETTINGS
# =============================================================================
# Window size mặc định
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800

# Theme
APPEARANCE_MODE = "dark"  # "light", "dark", "system"
COLOR_THEME = "blue"  # "blue", "green", "dark-blue"

# =============================================================================
# LOGGING
# =============================================================================
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
