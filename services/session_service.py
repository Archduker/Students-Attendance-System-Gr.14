"""
Session Service - Quản lý phiên đăng nhập
=========================================

Service xử lý session management:
- Tạo session token khi login
- Validate session
- Lưu remember me
- Session expiration
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json
from pathlib import Path

from services.security_service import SecurityService


class SessionService:
    """
    Service quản lý phiên đăng nhập.
    
    Example:
        >>> session_service = SessionService()
        >>> token = session_service.create_session(user_id=1, remember_me=True)
        >>> session_service.validate_session(token)
    """
    
    # Session expiration times
    DEFAULT_EXPIRY_HOURS = 24
    REMEMBER_ME_EXPIRY_DAYS = 30
    
    def __init__(self, security_service: Optional[SecurityService] = None):
        """
        Khởi tạo SessionService.
        
        Args:
            security_service: SecurityService instance (optional)
        """
        self.security = security_service or SecurityService()
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._session_file = Path(__file__).parent.parent / "data" / "sessions.json"
        
        # Load existing sessions
        self._load_sessions()
    
    def _load_sessions(self):
        """Load sessions từ file."""
        try:
            if self._session_file.exists():
                with open(self._session_file, "r", encoding="utf-8") as f:
                    self._sessions = json.load(f)
                # Clean expired sessions
                self._cleanup_expired()
        except Exception as e:
            print(f"Warning: Could not load sessions: {e}")
            self._sessions = {}
    
    def _save_sessions(self):
        """Lưu sessions vào file."""
        try:
            self._session_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self._session_file, "w", encoding="utf-8") as f:
                json.dump(self._sessions, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save sessions: {e}")
    
    def _cleanup_expired(self):
        """Xóa các session đã hết hạn."""
        now = datetime.now()
        expired_tokens = []
        
        for token, session in self._sessions.items():
            expires_at = datetime.fromisoformat(session["expires_at"])
            if now > expires_at:
                expired_tokens.append(token)
        
        for token in expired_tokens:
            del self._sessions[token]
        
        if expired_tokens:
            self._save_sessions()
    
    def create_session(
        self, 
        user_id: int, 
        username: str,
        role: str,
        remember_me: bool = False
    ) -> str:
        """
        Tạo session mới.
        
        Args:
            user_id: ID của user
            username: Tên đăng nhập
            role: Role của user
            remember_me: Có ghi nhớ đăng nhập không
            
        Returns:
            Session token
            
        Example:
            >>> token = session_service.create_session(1, "admin", "ADMIN", remember_me=True)
        """
        # Generate token
        token = self.security.generate_token(48)
        
        # Calculate expiry
        if remember_me:
            expires_at = datetime.now() + timedelta(days=self.REMEMBER_ME_EXPIRY_DAYS)
        else:
            expires_at = datetime.now() + timedelta(hours=self.DEFAULT_EXPIRY_HOURS)
        
        # Create session data
        session_data = {
            "user_id": user_id,
            "username": username,
            "role": role,
            "remember_me": remember_me,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        
        # Store session
        self._sessions[token] = session_data
        self._save_sessions()
        
        return token
    
    def validate_session(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate session token.
        
        Args:
            token: Session token
            
        Returns:
            Session data nếu valid, None nếu invalid/expired
            
        Example:
            >>> session = session_service.validate_session(token)
            >>> if session:
            ...     print(f"User: {session['username']}")
        """
        if not token or token not in self._sessions:
            return None
        
        session = self._sessions[token]
        
        # Check expiration
        expires_at = datetime.fromisoformat(session["expires_at"])
        if datetime.now() > expires_at:
            self.destroy_session(token)
            return None
        
        # Update last activity
        session["last_activity"] = datetime.now().isoformat()
        self._save_sessions()
        
        return session
    
    def get_session_user_id(self, token: str) -> Optional[int]:
        """
        Lấy user ID từ session token.
        
        Args:
            token: Session token
            
        Returns:
            User ID hoặc None
        """
        session = self.validate_session(token)
        return session["user_id"] if session else None
    
    def destroy_session(self, token: str) -> bool:
        """
        Hủy session (logout).
        
        Args:
            token: Session token
            
        Returns:
            True nếu thành công
            
        Example:
            >>> session_service.destroy_session(token)
        """
        if token in self._sessions:
            del self._sessions[token]
            self._save_sessions()
            return True
        return False
    
    def destroy_user_sessions(self, user_id: int) -> int:
        """
        Hủy tất cả sessions của một user.
        
        Args:
            user_id: ID của user
            
        Returns:
            Số sessions đã hủy
        """
        tokens_to_remove = [
            token for token, session in self._sessions.items()
            if session["user_id"] == user_id
        ]
        
        for token in tokens_to_remove:
            del self._sessions[token]
        
        if tokens_to_remove:
            self._save_sessions()
        
        return len(tokens_to_remove)
    
    def get_active_sessions_count(self, user_id: int) -> int:
        """
        Đếm số sessions đang active của user.
        
        Args:
            user_id: ID của user
            
        Returns:
            Số sessions active
        """
        count = 0
        now = datetime.now()
        
        for session in self._sessions.values():
            if session["user_id"] == user_id:
                expires_at = datetime.fromisoformat(session["expires_at"])
                if now <= expires_at:
                    count += 1
        
        return count
    
    def refresh_session(self, token: str) -> bool:
        """
        Gia hạn session.
        
        Args:
            token: Session token
            
        Returns:
            True nếu thành công
        """
        session = self.validate_session(token)
        if not session:
            return False
        
        # Extend expiry
        if session["remember_me"]:
            new_expiry = datetime.now() + timedelta(days=self.REMEMBER_ME_EXPIRY_DAYS)
        else:
            new_expiry = datetime.now() + timedelta(hours=self.DEFAULT_EXPIRY_HOURS)
        
        session["expires_at"] = new_expiry.isoformat()
        self._save_sessions()
        
        return True
