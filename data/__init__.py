"""
Data Package - Data Access Layer
=================================

Package này chứa các thành phần truy cập dữ liệu:

📂 repositories/   - Repository classes (CRUD operations)
📂 migrations/     - Database schema và seed data
database.py        - Database connection manager

Sử dụng Repository Pattern để tách biệt data access logic.

Cách sử dụng:
    from data.database import Database
    from data.repositories import UserRepository
    
    db = Database()
    user_repo = UserRepository(db)
    user = user_repo.find_by_id(1)
"""

from .database import Database

__all__ = ["Database"]
