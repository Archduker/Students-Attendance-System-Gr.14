"""
User Role Enum - Vai trò người dùng
===================================

Định nghĩa các vai trò trong hệ thống:
- ADMIN: Quản trị viên hệ thống
- TEACHER: Giáo viên
- STUDENT: Sinh viên
"""

from enum import Enum


class UserRole(Enum):
    """
    Enum định nghĩa các vai trò người dùng trong hệ thống.
    
    Attributes:
        ADMIN: Quản trị viên - quản lý users, classes, system
        TEACHER: Giáo viên - tạo phiên điểm danh, xem báo cáo
        STUDENT: Sinh viên - điểm danh, xem lịch sử
        
    Example:
        >>> from core.enums import UserRole
        >>> role = UserRole.TEACHER
        >>> print(role.value)
        TEACHER
    """
    
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"
    
    @classmethod
    def from_string(cls, role_str: str) -> "UserRole":
        """
        Chuyển đổi string thành UserRole enum.
        
        Args:
            role_str: Chuỗi vai trò (case-insensitive)
            
        Returns:
            UserRole enum tương ứng
            
        Raises:
            ValueError: Nếu role_str không hợp lệ
            
        Example:
            >>> UserRole.from_string("admin")
            UserRole.ADMIN
        """
        try:
            return cls(role_str.upper())
        except ValueError:
            valid_roles = [r.value for r in cls]
            raise ValueError(
                f"Invalid role: '{role_str}'. "
                f"Valid roles: {valid_roles}"
            )
    
    def __str__(self) -> str:
        return self.value
