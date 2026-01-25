"""
Auth Controller - Authentication Controller
============================================

Controller handles authentication-related requests.
"""

from typing import Dict, Any, Optional

from core.models import User
from core.exceptions import InvalidCredentialsError, AuthenticationError
from services import AuthService


class AuthController:
    """
    Controller handling authentication requests.
    
    Example:
        >>> auth_controller = AuthController(auth_service)
        >>> result = auth_controller.handle_login("admin", "123456")
        >>> if result["success"]:
        ...     print(f"Welcome {result['user'].full_name}")
    """
    
    def __init__(self, auth_service: AuthService):
        """
        Initialize AuthController.
        
        Args:
            auth_service: AuthService instance
        """
        self.auth_service = auth_service
    
    def handle_login(self, username: str, password: str, remember_me: bool = False) -> Dict[str, Any]:
        """
        Handle login request.
        
        Args:
            username: Username or email
            password: Password
            remember_me: Remember login session
            
        Returns:
            Dict with keys: success, user/error, role, token
            
        Example:
            >>> result = controller.handle_login("admin", "123456")
            >>> result
            {"success": True, "token": "...", "role": "ADMIN"}
        """
        # Validate input
        if not username or not username.strip():
            return {
                "success": False,
                "error": "Please enter username"
            }
        
        if not password:
            return {
                "success": False,
                "error": "Please enter password"
            }
        
        try:
            # Login and get token
            user, token = self.auth_service.login(
                username.strip(), 
                password,
                remember_me
            )
            
            return {
                "success": True,
                "user": user,
                "role": user.role.value,
                "token": token
            }
        except InvalidCredentialsError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def handle_logout(self) -> Dict[str, Any]:
        """
        Handle logout request.
        
        Returns:
            Dict with key: success
        """
        self.auth_service.logout()
        return {"success": True}
    
    def handle_reset_password(self, email: str) -> Dict[str, Any]:
        """
        Handle password reset request.
        
        Args:
            email: User's email address
            
        Returns:
            Dict with keys: success, message
        """
        # Validate input
        if not email or not email.strip():
            return {
                "success": False,
                "message": "Please enter email address"
            }
        
        # Basic email validation
        email = email.strip()
        if "@" not in email or "." not in email:
            return {
                "success": False,
                "message": "Invalid email address"
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
        Handle password change request.
        
        Args:
            old_password: Current password
            new_password: New password
            confirm_password: Confirm new password
            
        Returns:
            Dict with keys: success, message
        """
        # Validate input
        if not old_password:
            return {
                "success": False,
                "message": "Please enter current password"
            }
        
        if not new_password:
            return {
                "success": False,
                "message": "Please enter new password"
            }
        
        if len(new_password) < 6:
            return {
                "success": False,
                "message": "New password must be at least 6 characters"
            }
        
        if new_password != confirm_password:
            return {
                "success": False,
                "message": "Password confirmation does not match"
            }
        
        # Get current user
        current_user = self.auth_service.get_current_user()
        if not current_user:
            return {
                "success": False,
                "message": "Please login again"
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
        """Get currently logged in user."""
        return self.auth_service.get_current_user()
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.auth_service.is_authenticated()
