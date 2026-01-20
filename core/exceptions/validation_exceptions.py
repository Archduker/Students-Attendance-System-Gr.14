"""
Validation Exceptions - Lỗi validation
======================================

Các exception liên quan đến validation dữ liệu.
"""

from typing import Dict, List, Optional


class ValidationError(Exception):
    """
    Exception khi dữ liệu không hợp lệ.
    
    Attributes:
        message: Thông báo lỗi chung
        field: Tên trường bị lỗi (nếu có)
        errors: Dictionary chứa các lỗi theo field
        
    Example:
        >>> raise ValidationError("Email không hợp lệ", field="email")
        >>> raise ValidationError(
        ...     "Dữ liệu không hợp lệ",
        ...     errors={"email": "Email không hợp lệ", "password": "Mật khẩu quá ngắn"}
        ... )
    """
    
    def __init__(
        self, 
        message: str = "Dữ liệu không hợp lệ",
        field: Optional[str] = None,
        errors: Optional[Dict[str, str]] = None
    ):
        self.message = message
        self.field = field
        self.errors = errors or {}
        
        # Tạo message chi tiết
        if field:
            full_message = f"{field}: {message}"
        elif errors:
            error_details = "; ".join([f"{k}: {v}" for k, v in errors.items()])
            full_message = f"{message} ({error_details})"
        else:
            full_message = message
            
        super().__init__(full_message)
    
    def get_error_for_field(self, field_name: str) -> Optional[str]:
        """
        Lấy thông báo lỗi cho một field cụ thể.
        
        Args:
            field_name: Tên field cần lấy lỗi
            
        Returns:
            Thông báo lỗi hoặc None
        """
        return self.errors.get(field_name)
    
    def has_errors(self) -> bool:
        """Kiểm tra có lỗi không."""
        return bool(self.errors) or bool(self.message)
