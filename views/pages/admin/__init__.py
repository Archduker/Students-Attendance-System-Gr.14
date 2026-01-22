"""
Admin Module - Admin Pages
===========================

Module chứa các trang admin:
- Login: Đăng nhập admin
- Dashboard: Tổng quan hệ thống
- User Management: Quản lý người dùng
- Class Management: Quản lý lớp học
- Reports: Báo cáo hệ thống
"""

from .login import AdminLoginPage
from .dashboard import AdminDashboard
from .user_management import UserManagementPage
from .class_management import ClassManagementPage

__all__ = [
    'AdminLoginPage',
    'AdminDashboard',
    'UserManagementPage',
    'ClassManagementPage',
]
