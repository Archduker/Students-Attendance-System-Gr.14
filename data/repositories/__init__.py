"""
Repositories Package - Data Access Objects
============================================

Package chứa các repository classes:
- base_repository.py: Abstract base class
- user_repository.py: User CRUD operations
- classroom_repository.py: Classroom CRUD
- attendance_repository.py: Attendance operations

Repository Pattern: Tách biệt business logic và data access.

Cách sử dụng:
    from data.repositories import UserRepository
    from data.database import Database
    
    db = Database()
    user_repo = UserRepository(db)
    
    user = user_repo.find_by_id(1)
    users = user_repo.find_all()
"""

from .base_repository import BaseRepository
from .user_repository import UserRepository
from .classroom_repository import ClassroomRepository
from .attendance_repository import AttendanceSessionRepository, AttendanceRecordRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "ClassroomRepository",
    "AttendanceSessionRepository",
    "AttendanceRecordRepository",
]
