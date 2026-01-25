"""
Security Service - Security Operations
==========================

Service handles security tasks:
- Hash and verify passwords
- Generate secure tokens
- Generate session IDs
"""

import secrets
import string
from typing import Optional

import bcrypt


class SecurityService:
    """
    Service handling security operations.
    
    Example:
        >>> security = SecurityService()
        >>> hashed = security.hash_password("mypassword")
        >>> security.verify_password("mypassword", hashed)
        True
    """
    
    def hash_password(self, password: str) -> str:
        """
        Hash password with bcrypt.
        
        Args:
            password: Plaintext password
            
        Returns:
            Hashed password string
            
        Example:
            >>> hashed = security.hash_password("123456")
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password: Plaintext password to verify
            hashed: Hashed password from database
            
        Returns:
            True if password matches
            
        Example:
            >>> security.verify_password("123456", hashed_password)
            True
        """
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"), 
                hashed.encode("utf-8")
            )
        except Exception:
            return False
    
    def generate_token(self, length: int = 32) -> str:
        """
        Generate secure random token.
        
        Args:
            length: Token length (default: 32)
            
        Returns:
            Random token string
            
        Example:
            >>> token = security.generate_token()
            >>> len(token)
            32
        """
        return secrets.token_urlsafe(length)
    
    def generate_code(self, length: int = 6) -> str:
        """
        Generate numeric code (for attendance).
        
        Args:
            length: Code length (default: 6)
            
        Returns:
            Numeric code string
            
        Example:
            >>> code = security.generate_code()
            >>> code
            '482951'
        """
        return "".join(secrets.choice(string.digits) for _ in range(length))
    
    def generate_session_id(self) -> str:
        """
        Generate unique session ID.
        
        Returns:
            Session ID string (format: SS + timestamp + random)
            
        Example:
            >>> session_id = security.generate_session_id()
            >>> session_id
            'SS20240120143052ABC'
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = "".join(secrets.choice(string.ascii_uppercase) for _ in range(3))
        return f"SS{timestamp}{random_part}"
    
    def generate_record_id(self) -> str:
        """
        Generate unique record ID.
        
        Returns:
            Record ID string
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = "".join(secrets.choice(string.ascii_uppercase) for _ in range(3))
        return f"REC{timestamp}{random_part}"
