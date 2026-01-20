"""
Formatters - Format Helpers
===========================

Các hàm format data để hiển thị.
"""

from datetime import datetime, date, time
from typing import Optional


def format_datetime(
    dt: Optional[datetime], 
    format_str: str = "%d/%m/%Y %H:%M"
) -> str:
    """
    Format datetime thành string.
    
    Args:
        dt: Datetime object
        format_str: Format string (default: "dd/mm/yyyy HH:MM")
        
    Returns:
        Formatted string hoặc "-" nếu None
        
    Example:
        >>> format_datetime(datetime.now())
        "20/01/2024 14:30"
    """
    if dt is None:
        return "-"
    return dt.strftime(format_str)


def format_date(
    d: Optional[date], 
    format_str: str = "%d/%m/%Y"
) -> str:
    """
    Format date thành string.
    
    Args:
        d: Date object
        format_str: Format string
        
    Returns:
        Formatted string
    """
    if d is None:
        return "-"
    return d.strftime(format_str)


def format_time(
    t: Optional[time], 
    format_str: str = "%H:%M"
) -> str:
    """
    Format time thành string.
    
    Args:
        t: Time object
        format_str: Format string
        
    Returns:
        Formatted string
    """
    if t is None:
        return "-"
    return t.strftime(format_str)


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format số thành phần trăm.
    
    Args:
        value: Giá trị (0-1 hoặc 0-100)
        decimals: Số chữ số thập phân
        
    Returns:
        Formatted string (e.g., "85.5%")
    """
    if value > 1:
        # Already percentage
        return f"{value:.{decimals}f}%"
    else:
        # Convert to percentage
        return f"{value * 100:.{decimals}f}%"


def format_status(status: str) -> str:
    """
    Format attendance status thành tiếng Việt.
    
    Args:
        status: Status string (PRESENT, ABSENT, LATE)
        
    Returns:
        Vietnamese status
    """
    status_map = {
        "PRESENT": "Có mặt",
        "ABSENT": "Vắng mặt",
        "LATE": "Đi trễ",
    }
    return status_map.get(status.upper(), status)


def format_role(role: str) -> str:
    """
    Format role thành tiếng Việt.
    
    Args:
        role: Role string (ADMIN, TEACHER, STUDENT)
        
    Returns:
        Vietnamese role
    """
    role_map = {
        "ADMIN": "Quản trị viên",
        "TEACHER": "Giáo viên",
        "STUDENT": "Sinh viên",
    }
    return role_map.get(role.upper(), role)


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Cắt ngắn text nếu quá dài.
    
    Args:
        text: Text cần cắt
        max_length: Độ dài tối đa
        suffix: Suffix thêm vào cuối
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
