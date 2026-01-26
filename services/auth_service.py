"""
Auth Service - Authentication & Authorization
=============================================

Service handles authentication and authorization:
- Login / Logout
- Password reset
- Session management
"""

from typing import Optional, Tuple

from core.enums import UserRole
from core.models import User
from core.exceptions import InvalidCredentialsError, UnauthorizedError
from data.repositories import UserRepository, PasswordResetTokenRepository
from .security_service import SecurityService
from .session_service import SessionService

class AuthService:
    """
    Service handling authentication and authorization.
    """
    
    def __init__(
        self,
        user_repo: UserRepository,
        security_service: SecurityService,
        session_service: SessionService,
        email_service: Optional[object] = None
    ):
        """
        Initialize AuthService.
        
        Args:
            user_repo: UserRepository instance
            security_service: SecurityService instance
            session_service: SessionService instance
            email_service: EmailService instance (optional)
        """
        self.user_repo = user_repo
        self.security = security_service
        self.session = session_service
        self.email = email_service
        self._current_user: Optional[User] = None
    
    def login(self, username: str, password: str, remember_me: bool = False) -> Tuple[User, str]:
        """
        Login to the system.
        
        Args:
            username: Username or email
            password: Password
            remember_me: Remember login session
            
        Returns:
            Tuple (User object, session_token)
            
        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        # Find user (Login by Username OR Email)
        user = self.user_repo.find_by_username(username)
        
        # If not found by username, try email
        if not user and "@" in username:
            user = self.user_repo.find_by_email(username)
        
        if not user:
            raise InvalidCredentialsError("Invalid username or password")
        
        # Verify password
        if not self.security.verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid username or password")
        
        # Store current user
        self._current_user = user
        
        # Create session
        token = self.session.create_session(
            user_id=user.user_id,
            username=user.username,
            role=user.role.value,
            remember_me=remember_me
        )
        
        return user, token
    
    def logout(self) -> None:
        """Logout from the system."""
        self._current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """Get currently logged in user."""
        return self._current_user
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self._current_user is not None
    
    def reset_password(self, email: str, role: str = None) -> Tuple[bool, str]:
        """
        Reset password and send via email.
        
        Args:
            email: User's email address
            role: Optional role to verify against user
            
        Returns:
            Tuple (success, message)
            
        Example:
            >>> success, msg = auth.reset_password("user@email.com", "Student")
        """
        # Find user by email
        user = self.user_repo.find_by_email(email)
        
        if not user:
            return False, "Email does not exist in the system"
            
        # Verify role if provided
        if role:
            # Check if user role matches the requested role (case-insensitive)
            if str(user.role.value).upper() != str(role).upper():
                return False, f"Email exists but does not belong to role '{role}'"
        
        # Generate new password
        new_password = self.security.generate_code(8)
        new_hash = self.security.hash_password(new_password)
        
        # Update password in database
        success = self.user_repo.update_password(user.user_id, new_hash)
        
        if not success:
            return False, "Unable to update password"
        
        # DEMO ONLY: Print password to terminal
        print("\n" + "="*50)
        print(f"🔐 RESET PASSWORD REQUEST FOR: {email}")
        print(f"🔑 NEW PASSWORD: {new_password}")
        print("="*50 + "\n")
        
        # Send email (if email service available)
        if self.email:
            try:
                self.email.send_password_reset_email(email, new_password)
            except Exception as e:
                # Log error but still return success
                print(f"Warning: Could not send email: {e}")
        
        return True, f"New password has been generated (See Terminal)"
    
    def confirm_password_reset(self, reset_token: str, new_password: str) -> Tuple[bool, str]:
        """
        Confirm password reset using token.
        
        Args:
            reset_token: Password reset token
            new_password: New password to set
            
        Returns:
            Tuple (success, message)
            
        Example:
            >>> success, msg = auth.confirm_password_reset("token123", "newpass")
        """
        
        # Get token repository
        token_repo = PasswordResetTokenRepository(self.user_repo.db)
        
        # Validate token
        token_data = token_repo.get_valid_token(reset_token)
        
        if not token_data:
            return False, "Invalid or expired reset token"
        
        user_id = token_data["user_id"]
        
        # Hash new password
        new_hash = self.security.hash_password(new_password)
        
        # Update password
        success = self.user_repo.update_password(user_id, new_hash)
        
        if not success:
            return False, "Unable to update password"
        
        # Mark token as used
        token_repo.mark_token_as_used(reset_token)
        
        # Invalidate all other tokens for this user
        token_repo.invalidate_all_user_tokens(user_id)
        
        return True, "Password reset successfully"
    
    def change_password(
        self, 
        user_id: int, 
        old_password: str, 
        new_password: str
    ) -> Tuple[bool, str]:
        """
        Change password.
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            Tuple (success, message)
        """
        user = self.user_repo.find_by_id(user_id)
        
        if not user:
            return False, "User does not exist"
        
        # Verify old password
        if not self.security.verify_password(old_password, user.password_hash):
            return False, "Current password is incorrect"
        
        # Update password
        new_hash = self.security.hash_password(new_password)
        success = self.user_repo.update_password(user_id, new_hash)
        
        if success:
            return True, "Password changed successfully"
        else:
            return False, "Unable to update password"
    
    def check_permission(self, required_role: UserRole) -> bool:
        """
        Check if user has required permission.
        
        Args:
            required_role: Required role
            
        Returns:
            True if user has permission
        """
        if not self._current_user:
            return False
        
        # Admin has all permissions
        if self._current_user.role == UserRole.ADMIN:
            return True
        
        return self._current_user.role == required_role
    
    def require_permission(self, required_role: UserRole) -> None:
        """
        Require permission, raise error if not authorized.
        
        Args:
            required_role: Required role
            
        Raises:
            UnauthorizedError: If user doesn't have permission
        """
        if not self.check_permission(required_role):
            raise UnauthorizedError(
                f"You need {required_role.value} permission to perform this action"
            )
