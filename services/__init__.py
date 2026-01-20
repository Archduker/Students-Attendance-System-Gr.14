"""
Services Package - Business Logic Layer
========================================

Package chứa các service classes:
- auth_service.py: Authentication & authorization
- user_service.py: User management
- classroom_service.py: Class management
- attendance_service.py: Attendance operations
- dashboard_service.py: Dashboard data
- qr_service.py: QR code generation
- email_service.py: Email sending
- security_service.py: Password hashing, tokens

Services chứa business logic, gọi repositories để truy cập data.

Cách sử dụng:
    from services import AuthService, AttendanceService
    
    auth_service = AuthService(user_repo, security_service)
    user = auth_service.login("username", "password")
"""

from .auth_service import AuthService
from .security_service import SecurityService
from .qr_service import QRService
from .email_service import EmailService

__all__ = [
    "AuthService",
    "SecurityService", 
    "QRService",
    "EmailService",
]
