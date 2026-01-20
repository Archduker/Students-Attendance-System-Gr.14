"""
Enums Package - Các kiểu liệt kê
================================

Package chứa các enum types:
- user_role.py: UserRole (ADMIN, TEACHER, STUDENT)
- attendance_status.py: AttendanceStatus (PRESENT, ABSENT)
- attendance_method.py: AttendanceMethod (QR, LINK_TOKEN, MANUAL, AUTO)

Cách sử dụng:
    from core.enums import UserRole, AttendanceStatus, AttendanceMethod
    
    role = UserRole.TEACHER
    status = AttendanceStatus.PRESENT
"""

from .user_role import UserRole
from .attendance_status import AttendanceStatus
from .attendance_method import AttendanceMethod

__all__ = ["UserRole", "AttendanceStatus", "AttendanceMethod"]
