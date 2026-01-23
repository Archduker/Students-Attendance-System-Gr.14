"""
Exceptions Package - Custom Exceptions
======================================

Package chứa các custom exceptions:
- auth_exceptions.py: Lỗi xác thực
- validation_exceptions.py: Lỗi validation
- database_exceptions.py: Lỗi database

Cách sử dụng:
    from core.exceptions import AuthenticationError, ValidationError
    
    raise AuthenticationError("Invalid credentials")
"""

from .auth_exceptions import (
    AuthenticationError,
    InvalidCredentialsError,
    UnauthorizedError,
    SessionExpiredError,
)
from .validation_exceptions import ValidationError, NotFoundError
from .database_exceptions import DatabaseError

__all__ = [
    "AuthenticationError",
    "InvalidCredentialsError", 
    "UnauthorizedError",
    "SessionExpiredError",
    "ValidationError",
    "NotFoundError",
    "DatabaseError",
]
