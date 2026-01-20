"""
Database Configuration - Cấu hình Database
==========================================

File này chứa cấu hình kết nối và quản lý SQLite database.

Hướng dẫn sử dụng:
    from config.database import get_db_path, get_connection
    
    # Lấy đường dẫn database
    db_path = get_db_path()
    
    # Lấy connection
    conn = get_connection()
"""

import os
from pathlib import Path

# =============================================================================
# DATABASE SETTINGS
# =============================================================================
# Tên file database
DATABASE_NAME = "attendance.db"

# Đường dẫn đến thư mục database
DATABASE_DIR = Path(__file__).resolve().parent.parent / "database"


def get_db_path() -> Path:
    """
    Lấy đường dẫn đầy đủ đến file database.
    
    Returns:
        Path: Đường dẫn đến file attendance.db
        
    Example:
        >>> db_path = get_db_path()
        >>> print(db_path)
        /path/to/project/database/attendance.db
    """
    return DATABASE_DIR / DATABASE_NAME


def ensure_database_dir():
    """
    Đảm bảo thư mục database tồn tại.
    Tạo thư mục nếu chưa có.
    """
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# CONNECTION SETTINGS
# =============================================================================
# Timeout khi kết nối (giây)
CONNECTION_TIMEOUT = 30

# Cho phép multi-threading
CHECK_SAME_THREAD = False
