"""
Authentication Exceptions - Lỗi xác thực
========================================

Các exception liên quan đến authentication và authorization.
"""


class AuthenticationError(Exception):
    """
    Base exception cho các lỗi xác thực.
    
    Example:
        >>> raise AuthenticationError("Đăng nhập thất bại")
    """
    
    def __init__(self, message: str = "Lỗi xác thực"):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsError(AuthenticationError):
    """
    Exception khi thông tin đăng nhập không hợp lệ.
    
    Example:
        >>> raise InvalidCredentialsError()
    """
    
    def __init__(self, message: str = "Tên đăng nhập hoặc mật khẩu không đúng"):
        super().__init__(message)


class UnauthorizedError(AuthenticationError):
    """
    Exception khi người dùng không có quyền truy cập.
    
    Example:
        >>> raise UnauthorizedError("Bạn không có quyền truy cập tính năng này")
    """
    
    def __init__(self, message: str = "Bạn không có quyền thực hiện thao tác này"):
        super().__init__(message)


class SessionExpiredError(AuthenticationError):
    """
    Exception khi phiên đăng nhập hết hạn.
    
    Example:
        >>> raise SessionExpiredError()
    """
    
    def __init__(self, message: str = "Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại"):
        super().__init__(message)
