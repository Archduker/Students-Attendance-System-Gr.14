"""
Password Reset Token Repository
=================================

Repository for managing password reset tokens in the database.
Handles CRUD operations for secure password recovery flow.
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from data.repositories.base_repository import BaseRepository


class PasswordResetTokenRepository(BaseRepository):
    """
    Repository for password reset tokens.
    
    Manages secure, time-limited, single-use tokens for password recovery.
    """
    
    @property
    def table_name(self) -> str:
        """Return table name."""
        return "password_reset_tokens"
    
    def _row_to_entity(self, row) -> Dict[str, Any]:
        """Convert database row to dictionary."""
        if not row:
            return None
        return dict(row)
    
    def _entity_to_dict(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Convert entity to dictionary (pass-through for this case)."""
        return entity

    
    def create_token(
        self, 
        user_id: int, 
        reset_token: str, 
        expires_in_minutes: int = 30
    ) -> bool:
        """
        Create a new password reset token.
        
        Args:
            user_id: User ID requesting password reset
            reset_token: Secure random token string
            expires_in_minutes: Token validity duration (default: 30 min)
            
        Returns:
            True if token created successfully
            
        Example:
            >>> token = secrets.token_urlsafe(32)
            >>> repo.create_token(user_id=123, reset_token=token)
            True
        """
        expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)
        
        query = """
            INSERT INTO password_reset_tokens 
            (user_id, reset_token, expires_at, is_used, created_at)
            VALUES (?, ?, ?, 0, ?)
        """
        
        try:
            self.db.execute(
                query, 
                (user_id, reset_token, expires_at, datetime.now())
            )
            return True
        except sqlite3.IntegrityError:
            # Token already exists (collision, very rare)
            return False
    
    def get_valid_token(self, reset_token: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a valid (unused, non-expired) token.
        
        Args:
            reset_token: Token string to validate
            
        Returns:
            Dict with token info if valid, None otherwise
            
        Example:
            >>> token_data = repo.get_valid_token("abc123...")
            >>> if token_data:
            ...     print(f"Valid for user {token_data['user_id']}")
        """
        query = """
            SELECT id, user_id, reset_token, expires_at, is_used, created_at
            FROM password_reset_tokens
            WHERE reset_token = ?
              AND is_used = 0
              AND expires_at > ?
        """
        
        result = self.db.fetch_one(query, (reset_token, datetime.now()))
        
        if not result:
            return None
        
        return {
            "id": result[0],
            "user_id": result[1],
            "reset_token": result[2],
            "expires_at": result[3],
            "is_used": result[4],
            "created_at": result[5]
        }
    
    def mark_token_as_used(self, reset_token: str) -> bool:
        """
        Mark a token as used to prevent reuse.
        
        Args:
            reset_token: Token to mark as used
            
        Returns:
            True if successfully marked
        """
        query = """
            UPDATE password_reset_tokens
            SET is_used = 1
            WHERE reset_token = ?
        """
        
        self.db.execute(query, (reset_token,))
        return True
    
    def cleanup_expired_tokens(self, days_old: int = 7) -> int:
        """
        Delete old expired tokens (housekeeping).
        
        Args:
            days_old: Remove tokens older than this many days
            
        Returns:
            Number of tokens deleted
        """
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        query = """
            DELETE FROM password_reset_tokens
            WHERE created_at < ?
        """
        
        cursor = self.db.execute(query, (cutoff_date,))
        return cursor.rowcount if cursor else 0
    
    def invalidate_all_user_tokens(self, user_id: int) -> bool:
        """
        Invalidate all tokens for a specific user.
        
        Useful when user successfully resets password or account is locked.
        
        Args:
            user_id: User whose tokens should be invalidated
            
        Returns:
            True if successfully invalidated
        """
        query = """
            UPDATE password_reset_tokens
            SET is_used = 1
            WHERE user_id = ? AND is_used = 0
        """
        
        self.db.execute(query, (user_id,))
        return True
