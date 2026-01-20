"""
Auth Service - Authentication & Authorization
=============================================

Service xử lý xác thực và phân quyền:
- Login / Logout
- Password reset
- Session management
"""

from typing import Optional, Tuple

from core.enums import UserRole
from core.models import User
from core.exceptions import InvalidCredentialsError, UnauthorizedError
from data.repositories import UserRepository
from .security_service import SecurityService
from .email_service import EmailService


class AuthService:
    """
    Service xử lý authentication và authorization.
    
    Example:
        >>> auth = AuthService(user_repo, security, email)
        >>> user = auth.login("admin", "123456")
        >>> auth.reset_password("user@email.com")
    """
    
    def __init__(
        self,
        user_repo: UserRepository,
        security_service: SecurityService,
        email_service: Optional[EmailService] = None
    ):
        """
        Khởi tạo AuthService.
        
        Args:
            user_repo: UserRepository instance
            security_service: SecurityService instance
            email_service: EmailService instance (optional)
        """
        self.user_repo = user_repo
        self.security = security_service
        self.email = email_service
        self._current_user: Optional[User] = None
    
    def login(self, username: str, password: str) -> User:
        """
        Đăng nhập vào hệ thống.
        
        Args:
            username: Tên đăng nhập
            password: Mật khẩu
            
        Returns:
            User object nếu đăng nhập thành công
            
        Raises:
            InvalidCredentialsError: Nếu thông tin không đúng
            
        Example:
            >>> user = auth.login("admin", "123456")
            >>> print(user.role)
            UserRole.ADMIN
        """
        # Tìm user
        user = self.user_repo.find_by_username(username)
        
        if not user:
            raise InvalidCredentialsError("Tên đăng nhập hoặc mật khẩu không đúng")
        
        # Verify password
        if not self.security.verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Tên đăng nhập hoặc mật khẩu không đúng")
        
        # Lưu current user
        self._current_user = user
        
        return user
    
    def logout(self) -> None:
        """Đăng xuất khỏi hệ thống."""
        self._current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """Lấy user đang đăng nhập."""
        return self._current_user
    
    def is_authenticated(self) -> bool:
        """Kiểm tra đã đăng nhập chưa."""
        return self._current_user is not None
    
    def reset_password(self, email: str) -> Tuple[bool, str]:
        """
        Reset password và gửi qua email.
        
        Args:
            email: Email của user
            
        Returns:
            Tuple (success, message)
            
        Example:
            >>> success, msg = auth.reset_password("user@email.com")
        """
        # Tìm user theo email
        user = self.user_repo.find_by_email(email)
        
        if not user:
            return False, "Email không tồn tại trong hệ thống"
        
        # Generate new password
        new_password = self.security.generate_code(8)
        new_hash = self.security.hash_password(new_password)
        
        # Update password trong database
        success = self.user_repo.update_password(user.user_id, new_hash)
        
        if not success:
            return False, "Không thể cập nhật mật khẩu"
        
        # Gửi email (nếu có email service)
        if self.email:
            try:
                self.email.send_password_reset_email(email, new_password)
            except Exception as e:
                # Log error nhưng vẫn trả về success
                print(f"Warning: Could not send email: {e}")
        
        return True, f"Mật khẩu mới đã được gửi đến {email}"
    
    def change_password(
        self, 
        user_id: int, 
        old_password: str, 
        new_password: str
    ) -> Tuple[bool, str]:
        """
        Đổi mật khẩu.
        
        Args:
            user_id: ID của user
            old_password: Mật khẩu cũ
            new_password: Mật khẩu mới
            
        Returns:
            Tuple (success, message)
        """
        user = self.user_repo.find_by_id(user_id)
        
        if not user:
            return False, "User không tồn tại"
        
        # Verify old password
        if not self.security.verify_password(old_password, user.password_hash):
            return False, "Mật khẩu cũ không đúng"
        
        # Update password
        new_hash = self.security.hash_password(new_password)
        success = self.user_repo.update_password(user_id, new_hash)
        
        if success:
            return True, "Đổi mật khẩu thành công"
        else:
            return False, "Không thể cập nhật mật khẩu"
    
    def check_permission(self, required_role: UserRole) -> bool:
        """
        Kiểm tra user có quyền không.
        
        Args:
            required_role: Role cần có
            
        Returns:
            True nếu có quyền
        """
        if not self._current_user:
            return False
        
        # Admin có tất cả quyền
        if self._current_user.role == UserRole.ADMIN:
            return True
        
        return self._current_user.role == required_role
    
    def require_permission(self, required_role: UserRole) -> None:
        """
        Yêu cầu quyền, raise error nếu không có.
        
        Args:
            required_role: Role cần có
            
        Raises:
            UnauthorizedError: Nếu không có quyền
        """
        if not self.check_permission(required_role):
            raise UnauthorizedError(
                f"Bạn cần quyền {required_role.value} để thực hiện thao tác này"
            )
