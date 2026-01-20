"""
Auth Controller - Authentication Controller
============================================

Controller xử lý các request liên quan đến authentication.
"""

from typing import Dict, Any, Optional

from core.models import User
from core.exceptions import InvalidCredentialsError, AuthenticationError
from services import AuthService


class AuthController:
    """
    Controller xử lý authentication requests.
    
    Example:
        >>> auth_controller = AuthController(auth_service)
        >>> result = auth_controller.handle_login("admin", "123456")
        >>> if result["success"]:
        ...     print(f"Welcome {result['user'].full_name}")
    """
    
    def __init__(self, auth_service: AuthService):
        """
        Khởi tạo AuthController.
        
        Args:
            auth_service: AuthService instance
        """
        self.auth_service = auth_service
    
    def handle_login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Xử lý login request.
        
        Args:
            username: Tên đăng nhập
            password: Mật khẩu
            
        Returns:
            Dict với keys: success, user/error, role
            
        Example:
            >>> result = controller.handle_login("admin", "123456")
            >>> result
            {"success": True, "user": User(...), "role": "ADMIN"}
        """
        # Validate input
        if not username or not username.strip():
            return {
                "success": False,
                "error": "Vui lòng nhập tên đăng nhập"
            }
        
        if not password:
            return {
                "success": False,
                "error": "Vui lòng nhập mật khẩu"
            }
        
        try:
            user = self.auth_service.login(username.strip(), password)
            return {
                "success": True,
                "user": user,
                "role": user.role.value
            }
        except InvalidCredentialsError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Lỗi hệ thống: {str(e)}"
            }
    
    def handle_logout(self) -> Dict[str, Any]:
        """
        Xử lý logout request.
        
        Returns:
            Dict với key: success
        """
        self.auth_service.logout()
        return {"success": True}
    
    def handle_reset_password(self, email: str) -> Dict[str, Any]:
        """
        Xử lý reset password request.
        
        Args:
            email: Email của user
            
        Returns:
            Dict với keys: success, message
        """
        # Validate input
        if not email or not email.strip():
            return {
                "success": False,
                "message": "Vui lòng nhập email"
            }
        
        # Basic email validation
        email = email.strip()
        if "@" not in email or "." not in email:
            return {
                "success": False,
                "message": "Email không hợp lệ"
            }
        
        success, message = self.auth_service.reset_password(email)
        return {
            "success": success,
            "message": message
        }
    
    def handle_change_password(
        self, 
        old_password: str, 
        new_password: str,
        confirm_password: str
    ) -> Dict[str, Any]:
        """
        Xử lý change password request.
        
        Args:
            old_password: Mật khẩu cũ
            new_password: Mật khẩu mới
            confirm_password: Xác nhận mật khẩu mới
            
        Returns:
            Dict với keys: success, message
        """
        # Validate input
        if not old_password:
            return {
                "success": False,
                "message": "Vui lòng nhập mật khẩu cũ"
            }
        
        if not new_password:
            return {
                "success": False,
                "message": "Vui lòng nhập mật khẩu mới"
            }
        
        if len(new_password) < 6:
            return {
                "success": False,
                "message": "Mật khẩu mới phải có ít nhất 6 ký tự"
            }
        
        if new_password != confirm_password:
            return {
                "success": False,
                "message": "Xác nhận mật khẩu không khớp"
            }
        
        # Get current user
        current_user = self.auth_service.get_current_user()
        if not current_user:
            return {
                "success": False,
                "message": "Vui lòng đăng nhập lại"
            }
        
        success, message = self.auth_service.change_password(
            current_user.user_id,
            old_password,
            new_password
        )
        
        return {
            "success": success,
            "message": message
        }
    
    def get_current_user(self) -> Optional[User]:
        """Lấy user đang đăng nhập."""
        return self.auth_service.get_current_user()
    
    def is_authenticated(self) -> bool:
        """Kiểm tra đã đăng nhập chưa."""
        return self.auth_service.is_authenticated()
