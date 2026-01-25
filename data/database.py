"""
Database Connection Manager
===========================

Quản lý kết nối SQLite database với connection pooling.

Cách sử dụng:
    from data.database import Database
    
    # Singleton instance
    db = Database()
    
    # Execute query
    db.execute("SELECT * FROM users WHERE id = ?", (1,))
    
    # Transaction
    with db.transaction():
        db.execute("INSERT INTO users ...")
        db.execute("UPDATE stats ...")
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, List, Optional, Tuple

from config.database import get_db_path, ensure_database_dir, CONNECTION_TIMEOUT, CHECK_SAME_THREAD


class Database:
    """
    Singleton class quản lý kết nối SQLite database.
    
    Features:
    - Singleton pattern: chỉ có 1 instance
    - Connection management
    - Transaction support
    - Query execution helpers
    
    Example:
        >>> db = Database()
        >>> users = db.fetch_all("SELECT * FROM users")
        >>> user = db.fetch_one("SELECT * FROM users WHERE id = ?", (1,))
    """
    
    _instance: Optional["Database"] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls) -> "Database":
        """Singleton pattern - chỉ tạo 1 instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Khởi tạo database connection."""
        if self._connection is None:
            self._connect()
    
    def _connect(self) -> None:
        """Tạo kết nối đến database."""
        ensure_database_dir()
        db_path = get_db_path()
        
        self._connection = sqlite3.connect(
            str(db_path),
            timeout=CONNECTION_TIMEOUT,
            check_same_thread=CHECK_SAME_THREAD,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        
        # Register datetime adapter for Python 3.12+
        # This fixes the deprecation warning
        from datetime import datetime
        
        def adapt_datetime(dt):
            """Convert datetime to ISO format string."""
            return dt.isoformat()
        
        def convert_datetime(val):
            """Convert ISO format string to datetime."""
            return datetime.fromisoformat(val.decode())
        
        sqlite3.register_adapter(datetime, adapt_datetime)
        sqlite3.register_converter("DATETIME", convert_datetime)
        
        # Enable foreign keys
        self._connection.execute("PRAGMA foreign_keys = ON")
        
        # Return rows as dictionaries
        self._connection.row_factory = sqlite3.Row
    
    @property
    def connection(self) -> sqlite3.Connection:
        """Lấy connection hiện tại."""
        if self._connection is None:
            self._connect()
        return self._connection
    
    def execute(
        self, 
        query: str, 
        params: Tuple = ()
    ) -> sqlite3.Cursor:
        """
        Thực thi một query.
        
        Args:
            query: SQL query string
            params: Parameters cho query (tuple)
            
        Returns:
            Cursor object
            
        Example:
            >>> db.execute("INSERT INTO users (name) VALUES (?)", ("John",))
        """
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor
    
    def execute_many(
        self,
        query: str,
        params_list: List[Tuple]
    ) -> sqlite3.Cursor:
        """
        Thực thi query với nhiều bộ params.
        
        Args:
            query: SQL query string
            params_list: List các tuple params
            
        Returns:
            Cursor object
        """
        cursor = self.connection.cursor()
        cursor.executemany(query, params_list)
        self.connection.commit()
        return cursor
    
    def fetch_one(
        self, 
        query: str, 
        params: Tuple = ()
    ) -> Optional[sqlite3.Row]:
        """
        Lấy một bản ghi.
        
        Args:
            query: SQL query string
            params: Parameters cho query
            
        Returns:
            Row object hoặc None
            
        Example:
            >>> user = db.fetch_one("SELECT * FROM users WHERE id = ?", (1,))
            >>> print(user["name"])
        """
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
    
    def fetch_all(
        self, 
        query: str, 
        params: Tuple = ()
    ) -> List[sqlite3.Row]:
        """
        Lấy tất cả bản ghi.
        
        Args:
            query: SQL query string
            params: Parameters cho query
            
        Returns:
            List các Row objects
            
        Example:
            >>> users = db.fetch_all("SELECT * FROM users")
            >>> for user in users:
            ...     print(user["name"])
        """
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    @contextmanager
    def transaction(self):
        """
        Context manager cho transaction.
        
        Tự động commit nếu thành công, rollback nếu có lỗi.
        
        Example:
            >>> with db.transaction():
            ...     db.execute("INSERT INTO users ...")
            ...     db.execute("UPDATE stats ...")
        """
        try:
            yield
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
    
    def close(self) -> None:
        """Đóng connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def __del__(self):
        """Cleanup khi object bị destroy."""
        self.close()
