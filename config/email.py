"""
Email Configuration - Cấu hình Email
=====================================

File này chứa cấu hình cho việc gửi email (password reset, notifications).

⚠️ LƯU Ý BẢO MẬT:
- KHÔNG commit email password vào Git
- Sử dụng biến môi trường hoặc file .env

Hướng dẫn sử dụng:
    from config.email import SMTP_CONFIG, get_email_config
    
    # Lấy cấu hình email
    config = get_email_config()
"""

import os

# =============================================================================
# SMTP CONFIGURATION
# =============================================================================
# Cấu hình mặc định cho Gmail
SMTP_CONFIG = {
    "server": "smtp.gmail.com",
    "port": 587,
    "use_tls": True,
}

# Email gửi đi (sender)
# ⚠️ Không hardcode giá trị thật, dùng biến môi trường
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")  # App password từ Google

# =============================================================================
# EMAIL TEMPLATES
# =============================================================================
# Subject mặc định cho các loại email
EMAIL_SUBJECTS = {
    "password_reset": "[Student Attendance] Khôi phục mật khẩu",
    "welcome": "[Student Attendance] Chào mừng bạn đến với hệ thống",
    "attendance_reminder": "[Student Attendance] Nhắc nhở điểm danh",
}


def get_email_config() -> dict:
    """
    Lấy cấu hình email đầy đủ.
    
    Returns:
        dict: Cấu hình SMTP và thông tin sender
        
    Example:
        >>> config = get_email_config()
        >>> print(config['server'])
        smtp.gmail.com
    """
    return {
        **SMTP_CONFIG,
        "sender_email": SENDER_EMAIL,
        "sender_password": SENDER_PASSWORD,
    }


def is_email_configured() -> bool:
    """
    Kiểm tra email đã được cấu hình chưa.
    
    Returns:
        bool: True nếu đã cấu hình đầy đủ
    """
    return bool(SENDER_EMAIL and SENDER_PASSWORD)
