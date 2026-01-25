"""
Repositories Package - Data Access Objects
============================================

Package contains repository classes:
- base_repository.py: Abstract base class
- user_repository.py: User CRUD operations
- classroom_repository.py: Classroom CRUD
- attendance_repository.py: Attendance operations
- password_reset_token_repository.py: Password reset token operations

Repository Pattern: Separates business logic from data access.

Usage:
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
from .password_reset_token_repository import PasswordResetTokenRepository

# Alias for compatibility
ClassRepository = ClassroomRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "ClassroomRepository",
    "ClassRepository",  # Alias
    "AttendanceSessionRepository",
    "AttendanceRecordRepository",
    "PasswordResetTokenRepository",
]
