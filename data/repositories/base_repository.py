"""
Base Repository - Abstract Base Class
======================================

Base class cho tất cả repositories với các CRUD operations cơ bản.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

from data.database import Database

# Generic type cho entity
T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base class cho repositories.
    
    Provides:
    - Common CRUD operations interface
    - Database connection management
    - Query building helpers
    
    Subclasses cần implement:
    - table_name: Tên bảng trong database
    - _row_to_entity: Chuyển đổi row thành entity
    - _entity_to_dict: Chuyển đổi entity thành dict
    
    Example:
        >>> class UserRepository(BaseRepository[User]):
        ...     table_name = "users"
        ...     
        ...     def _row_to_entity(self, row):
        ...         return User(**dict(row))
    """
    
    def __init__(self, db: Database):
        """
        Khởi tạo repository với database connection.
        
        Args:
            db: Database instance
        """
        self.db = db
    
    @property
    @abstractmethod
    def table_name(self) -> str:
        """Tên bảng trong database."""
        pass
    
    @abstractmethod
    def _row_to_entity(self, row) -> T:
        """
        Chuyển đổi database row thành entity object.
        
        Args:
            row: sqlite3.Row object
            
        Returns:
            Entity object (User, Classroom, etc.)
        """
        pass
    
    @abstractmethod
    def _entity_to_dict(self, entity: T) -> Dict[str, Any]:
        """
        Chuyển đổi entity object thành dictionary cho database.
        
        Args:
            entity: Entity object
            
        Returns:
            Dictionary với các field và values
        """
        pass
    
    def find_by_id(self, id: Any) -> Optional[T]:
        """
        Tìm entity theo ID.
        
        Args:
            id: Primary key value
            
        Returns:
            Entity object hoặc None nếu không tìm thấy
        """
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        row = self.db.fetch_one(query, (id,))
        return self._row_to_entity(row) if row else None
    
    def find_all(self) -> List[T]:
        """
        Lấy tất cả entities.
        
        Returns:
            List các entity objects
        """
        query = f"SELECT * FROM {self.table_name}"
        rows = self.db.fetch_all(query)
        return [self._row_to_entity(row) for row in rows]
    
    def find_by(self, **conditions) -> List[T]:
        """
        Tìm entities theo điều kiện.
        
        Args:
            **conditions: Các điều kiện (field=value)
            
        Returns:
            List các entity objects thỏa mãn điều kiện
            
        Example:
            >>> users = user_repo.find_by(role="TEACHER", active=True)
        """
        where_clauses = " AND ".join([f"{k} = ?" for k in conditions.keys()])
        query = f"SELECT * FROM {self.table_name} WHERE {where_clauses}"
        rows = self.db.fetch_all(query, tuple(conditions.values()))
        return [self._row_to_entity(row) for row in rows]
    
    def create(self, entity: T) -> T:
        """
        Tạo entity mới trong database.
        
        Args:
            entity: Entity object cần tạo
            
        Returns:
            Entity object với ID được gán
        """
        data = self._entity_to_dict(entity)
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        cursor = self.db.execute(query, tuple(data.values()))
        
        # Update entity với ID mới
        return entity
    
    def update(self, entity: T) -> T:
        """
        Cập nhật entity trong database.
        
        Args:
            entity: Entity object cần cập nhật
            
        Returns:
            Entity object đã cập nhật
        """
        data = self._entity_to_dict(entity)
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
        self.db.execute(query, (*data.values(), data.get("id")))
        
        return entity
    
    def delete(self, id: Any) -> bool:
        """
        Xóa entity theo ID.
        
        Args:
            id: Primary key value
            
        Returns:
            True nếu xóa thành công
        """
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        cursor = self.db.execute(query, (id,))
        return cursor.rowcount > 0
    
    def count(self) -> int:
        """
        Đếm số lượng entities.
        
        Returns:
            Số lượng records
        """
        query = f"SELECT COUNT(*) as count FROM {self.table_name}"
        row = self.db.fetch_one(query)
        return row["count"] if row else 0
    
    def exists(self, id: Any) -> bool:
        """
        Kiểm tra entity có tồn tại không.
        
        Args:
            id: Primary key value
            
        Returns:
            True nếu tồn tại
        """
        query = f"SELECT 1 FROM {self.table_name} WHERE id = ? LIMIT 1"
        row = self.db.fetch_one(query, (id,))
        return row is not None
