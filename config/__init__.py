"""
Config Package - Cấu hình ứng dụng
==================================

Package này chứa các file cấu hình cho ứng dụng:
- settings.py: Cấu hình chung của ứng dụng
- database.py: Cấu hình kết nối database
- email.py: Cấu hình gửi email

Cách sử dụng:
    from config.settings import APP_NAME, DEBUG
    from config.database import get_db_path
    from config.email import SMTP_CONFIG
"""

from .settings import *
from .database import *
from .email import *
