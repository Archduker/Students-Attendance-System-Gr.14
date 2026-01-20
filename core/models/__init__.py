"""
Models Package - Data Models
============================

Package chứa các data models (entity classes):
- user.py: User, Admin, Teacher, Student
- classroom.py: Class model
- attendance_session.py: AttendanceSession model
- attendance_record.py: AttendanceRecord model

Cách sử dụng:
    from core.models import User, Teacher, Student, AttendanceSession
"""

from .user import User, Admin, Teacher, Student
from .classroom import Classroom
from .attendance_session import AttendanceSession
from .attendance_record import AttendanceRecord

__all__ = [
    "User", "Admin", "Teacher", "Student",
    "Classroom", "AttendanceSession", "AttendanceRecord"
]
