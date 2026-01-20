"""
Validators - Input Validation Helpers
=====================================

Các hàm validate input data.
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format.
    
    Args:
        email: Email cần validate
        
    Returns:
        Tuple (is_valid, error_message)
        
    Example:
        >>> validate_email("test@email.com")
        (True, "")
        >>> validate_email("invalid")
        (False, "Email không hợp lệ")
    """
    if not email:
        return False, "Email không được để trống"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Email không hợp lệ"
    
    return True, ""


def validate_password(password: str, min_length: int = 6) -> Tuple[bool, str]:
    """
    Validate password.
    
    Args:
        password: Password cần validate
        min_length: Độ dài tối thiểu (default: 6)
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not password:
        return False, "Mật khẩu không được để trống"
    
    if len(password) < min_length:
        return False, f"Mật khẩu phải có ít nhất {min_length} ký tự"
    
    return True, ""


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Validate username.
    
    Args:
        username: Username cần validate
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not username:
        return False, "Tên đăng nhập không được để trống"
    
    if len(username) < 3:
        return False, "Tên đăng nhập phải có ít nhất 3 ký tự"
    
    if len(username) > 50:
        return False, "Tên đăng nhập không được quá 50 ký tự"
    
    # Only alphanumeric and underscore
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Tên đăng nhập chỉ được chứa chữ cái, số và dấu gạch dưới"
    
    return True, ""


def validate_required(value: str, field_name: str) -> Tuple[bool, str]:
    """
    Validate required field.
    
    Args:
        value: Giá trị cần validate
        field_name: Tên field (để hiển thị lỗi)
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not value or not value.strip():
        return False, f"{field_name} không được để trống"
    
    return True, ""


def validate_student_code(code: str) -> Tuple[bool, str]:
    """
    Validate mã sinh viên.
    
    Args:
        code: Mã sinh viên (format: SVxxx)
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not code:
        return False, "Mã sinh viên không được để trống"
    
    if not re.match(r'^SV\d{3,}$', code.upper()):
        return False, "Mã sinh viên không hợp lệ (format: SVxxx)"
    
    return True, ""


def validate_teacher_code(code: str) -> Tuple[bool, str]:
    """
    Validate mã giáo viên.
    
    Args:
        code: Mã giáo viên (format: GVxxx)
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not code:
        return False, "Mã giáo viên không được để trống"
    
    if not re.match(r'^GV\d{3,}$', code.upper()):
        return False, "Mã giáo viên không hợp lệ (format: GVxxx)"
    
    return True, ""
