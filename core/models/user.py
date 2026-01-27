"""
User Models - Các model người dùng
==================================

Định nghĩa các class cho người dùng:
- User: Base class cho tất cả users
- Admin: Quản trị viên hệ thống
- Teacher: Giáo viên
- Student: Sinh viên

Inheritance hierarchy:
    User (base)
    ├── Admin
    ├── Teacher
    └── Student
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from core.enums import UserRole


@dataclass
class User:
    """
    Base class cho tất cả người dùng trong hệ thống.
    
    Attributes:
        user_id: ID duy nhất của user
        username: Tên đăng nhập
        password_hash: Mật khẩu đã hash (không lưu plaintext!)
        full_name: Họ tên đầy đủ
        role: Vai trò (ADMIN, TEACHER, STUDENT)
        email: Email của user
        created_at: Thời gian tạo tài khoản
        
    Example:
        >>> user = User(
        ...     user_id=1,
        ...     username="admin",
        ...     password_hash="hashed_password",
        ...     full_name="Admin User",
        ...     role=UserRole.ADMIN
        ... )
    """
    
    user_id: int
    username: str
    password_hash: str
    full_name: str
    role: UserRole
    email: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate data sau khi khởi tạo."""
        if not self.username:
            raise ValueError("Username không được để trống")
        if not self.full_name:
            raise ValueError("Full name không được để trống")
    
    def to_dict(self) -> dict:
        """Chuyển đổi thành dictionary."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "full_name": self.full_name,
            "role": self.role.value,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "admin_id": getattr(self, 'admin_id', None),
            "teacher_code": getattr(self, 'teacher_code', None),
            "student_code": getattr(self, 'student_code', None),
        }


@dataclass
class Admin(User):
    """
    Model cho Admin - Quản trị viên hệ thống.
    
    Attributes:
        admin_id: Mã admin (VD: "AD001")
        
    Chức năng:
        - Quản lý users (CRUD)
        - Quản lý classes
        - Xem system status
        - Quản lý cấu hình hệ thống
    """
    
    admin_id: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.role = UserRole.ADMIN


@dataclass
class Teacher(User):
    """
    Model cho Teacher - Giáo viên.
    
    Attributes:
        teacher_code: Mã giáo viên (VD: "GV001")
        department: Khoa/Bộ môn
        
    Chức năng:
        - Tạo phiên điểm danh
        - Xem attendance history của lớp
        - Generate QR code / token
        - Điểm danh thủ công
    """
    
    teacher_code: str = ""
    department: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.role = UserRole.TEACHER


@dataclass
class Student(User):
    """
    Model cho Student - Sinh viên.
    
    Attributes:
        student_code: Mã sinh viên (VD: "SV001")
        class_name: Lớp sinh hoạt
        
    Chức năng:
        - Submit attendance (QR/Token)
        - Xem attendance history cá nhân
        - Xem dashboard thống kê
    """
    
    student_code: str = ""
    class_name: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.role = UserRole.STUDENT
