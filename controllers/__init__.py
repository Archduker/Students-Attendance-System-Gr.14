"""
Controllers Package - Application Logic
========================================

Package chứa các controller classes:
- auth_controller.py: Login, logout, password reset
- dashboard_controller.py: Dashboard data
- attendance_controller.py: Attendance operations
- user_controller.py: User management (Admin)
- profile_controller.py: Profile editing

Controllers xử lý request từ UI, gọi services, trả về response.

Cách sử dụng:
    from controllers import AuthController
    
    auth_controller = AuthController(auth_service)
    result = auth_controller.handle_login("username", "password")
"""

from .auth_controller import AuthController

__all__ = ["AuthController"]
