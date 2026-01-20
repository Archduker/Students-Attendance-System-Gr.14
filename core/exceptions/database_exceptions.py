"""
Database Exceptions - Lỗi database
==================================

Các exception liên quan đến thao tác database.
"""

from typing import Optional


class DatabaseError(Exception):
    """
    Base exception cho các lỗi database.
    
    Attributes:
        message: Thông báo lỗi
        query: Query gây lỗi (nếu có)
        original_error: Exception gốc từ database driver
        
    Example:
        >>> raise DatabaseError("Không thể kết nối database")
        >>> raise DatabaseError(
        ...     "Lỗi khi thực thi query",
        ...     query="SELECT * FROM users",
        ...     original_error=sqlite3_error
        ... )
    """
    
    def __init__(
        self,
        message: str = "Lỗi database",
        query: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        self.message = message
        self.query = query
        self.original_error = original_error
        
        # Tạo message chi tiết
        full_message = message
        if query:
            full_message += f" | Query: {query[:100]}..."
        if original_error:
            full_message += f" | Original: {str(original_error)}"
            
        super().__init__(full_message)


class RecordNotFoundError(DatabaseError):
    """
    Exception khi không tìm thấy bản ghi.
    
    Example:
        >>> raise RecordNotFoundError("User", user_id=123)
    """
    
    def __init__(self, entity_name: str, **identifiers):
        id_str = ", ".join([f"{k}={v}" for k, v in identifiers.items()])
        message = f"Không tìm thấy {entity_name} với {id_str}"
        super().__init__(message)


class DuplicateRecordError(DatabaseError):
    """
    Exception khi bản ghi đã tồn tại.
    
    Example:
        >>> raise DuplicateRecordError("User", username="admin")
    """
    
    def __init__(self, entity_name: str, **identifiers):
        id_str = ", ".join([f"{k}={v}" for k, v in identifiers.items()])
        message = f"{entity_name} với {id_str} đã tồn tại"
        super().__init__(message)
