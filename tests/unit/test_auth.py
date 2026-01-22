"""
Unit Tests for Auth Module
==========================

Test cases cho:
- AuthService: login, logout, password reset
- SecurityService: password hashing, token generation
- SessionService: session management
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta

from services.security_service import SecurityService
from services.auth_service import AuthService
from services.session_service import SessionService
from core.exceptions import InvalidCredentialsError
from core.enums import UserRole


class TestSecurityService:
    """Test cases cho SecurityService."""
    
    @pytest.fixture
    def security(self):
        """SecurityService instance."""
        return SecurityService()
    
    def test_hash_password_returns_string(self, security):
        """Hash password phải trả về string."""
        password = "test123456"
        hashed = security.hash_password(password)
        
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password
    
    def test_hash_password_different_each_time(self, security):
        """Hash cùng password nhiều lần phải khác nhau (do salt)."""
        password = "test123456"
        hash1 = security.hash_password(password)
        hash2 = security.hash_password(password)
        
        assert hash1 != hash2
    
    def test_verify_password_correct(self, security):
        """Verify password đúng phải trả về True."""
        password = "test123456"
        hashed = security.hash_password(password)
        
        assert security.verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self, security):
        """Verify password sai phải trả về False."""
        password = "test123456"
        wrong_password = "wrong_password"
        hashed = security.hash_password(password)
        
        assert security.verify_password(wrong_password, hashed) is False
    
    def test_verify_password_empty(self, security):
        """Verify password rỗng phải trả về False."""
        password = "test123456"
        hashed = security.hash_password(password)
        
        assert security.verify_password("", hashed) is False
    
    def test_generate_token_default_length(self, security):
        """Generate token với default length."""
        token = security.generate_token()
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_generate_token_custom_length(self, security):
        """Generate token với custom length."""
        token = security.generate_token(64)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_generate_token_unique(self, security):
        """Mỗi token phải unique."""
        token1 = security.generate_token()
        token2 = security.generate_token()
        
        assert token1 != token2
    
    def test_generate_code_default_length(self, security):
        """Generate code với default length (6 digits)."""
        code = security.generate_code()
        
        assert isinstance(code, str)
        assert len(code) == 6
        assert code.isdigit()
    
    def test_generate_code_custom_length(self, security):
        """Generate code với custom length."""
        code = security.generate_code(8)
        
        assert len(code) == 8
        assert code.isdigit()
    
    def test_generate_session_id(self, security):
        """Generate session ID format."""
        session_id = security.generate_session_id()
        
        assert isinstance(session_id, str)
        assert session_id.startswith("SS")


class TestAuthService:
    """Test cases cho AuthService."""
    
    @pytest.fixture
    def mock_user_repo(self):
        """Mock UserRepository."""
        return Mock()
    
    @pytest.fixture
    def mock_security(self):
        """Mock SecurityService."""
        return Mock()
    
    @pytest.fixture
    def mock_email(self):
        """Mock EmailService."""
        return Mock()
    
    @pytest.fixture
    def session_service(self):
        """Mock SessionService."""
        return Mock()
    
    @pytest.fixture
    def auth_service(self, mock_user_repo, mock_security, session_service, mock_email):
        """AuthService với mocked dependencies."""
        return AuthService(mock_user_repo, mock_security, session_service, mock_email)
    
    def test_login_success(self, auth_service, mock_user_repo, mock_security, session_service):
        """Login thành công với credentials đúng."""
        # Setup
        mock_user = Mock()
        mock_user.user_id = 1
        mock_user.username = "testuser"
        mock_user.password_hash = "hashed_password"
        mock_user.role = UserRole.STUDENT
        
        mock_user_repo.find_by_username.return_value = mock_user
        mock_security.verify_password.return_value = True
        session_service.create_session.return_value = "mock_token"
        
        # Execute
        user, token = auth_service.login("testuser", "password123")
        
        # Verify
        assert user == mock_user
        assert token == "mock_token"
        assert auth_service.get_current_user() == mock_user
        mock_user_repo.find_by_username.assert_called_once_with("testuser")
        mock_security.verify_password.assert_called_once_with("password123", "hashed_password")
        session_service.create_session.assert_called_once()
    
    def test_login_user_not_found(self, auth_service, mock_user_repo):
        """Login thất bại khi user không tồn tại."""
        mock_user_repo.find_by_username.return_value = None
        
        with pytest.raises(InvalidCredentialsError):
            auth_service.login("nonexistent", "password")
    
    def test_login_wrong_password(self, auth_service, mock_user_repo, mock_security):
        """Login thất bại khi password sai."""
        mock_user = Mock()
        mock_user.password_hash = "hashed_password"
        
        mock_user_repo.find_by_username.return_value = mock_user
        mock_security.verify_password.return_value = False
        
        with pytest.raises(InvalidCredentialsError):
            auth_service.login("testuser", "wrong_password")
    
    def test_logout(self, auth_service, mock_user_repo, mock_security, session_service):
        """Logout phải clear current user."""
        # Login first
        mock_user = Mock()
        mock_user.password_hash = "hash"
        mock_user_repo.find_by_username.return_value = mock_user
        mock_security.verify_password.return_value = True
        session_service.create_session.return_value = "token"
        
        auth_service.login("user", "pass")
        assert auth_service.is_authenticated() is True
        
        # Logout
        auth_service.logout()
        
        assert auth_service.is_authenticated() is False
        assert auth_service.get_current_user() is None
    
    def test_is_authenticated_true(self, auth_service, mock_user_repo, mock_security, session_service):
        """is_authenticated trả về True khi đã login."""
        mock_user = Mock()
        mock_user.password_hash = "hash"
        mock_user_repo.find_by_username.return_value = mock_user
        mock_security.verify_password.return_value = True
        session_service.create_session.return_value = "token"
        
        auth_service.login("user", "pass")
        
        assert auth_service.is_authenticated() is True
    
    def test_is_authenticated_false(self, auth_service):
        """is_authenticated trả về False khi chưa login."""
        assert auth_service.is_authenticated() is False
    
    def test_reset_password_success(self, auth_service, mock_user_repo, mock_security, mock_email):
        """Reset password thành công."""
        mock_user = Mock()
        mock_user.user_id = 1
        mock_user.email = "test@example.com"
        
        mock_user_repo.find_by_email.return_value = mock_user
        mock_security.generate_code.return_value = "newpass1"
        mock_security.hash_password.return_value = "hashed_new"
        mock_user_repo.update_password.return_value = True
        
        success, message = auth_service.reset_password("test@example.com")
        
        assert success is True
        mock_user_repo.update_password.assert_called_once_with(1, "hashed_new")
    
    def test_reset_password_email_not_found(self, auth_service, mock_user_repo):
        """Reset password thất bại khi email không tồn tại."""
        mock_user_repo.find_by_email.return_value = None
        
        success, message = auth_service.reset_password("notfound@example.com")
        
        assert success is False
        assert "không tồn tại" in message


class TestSessionService:
    """Test cases cho SessionService."""
    
    @pytest.fixture
    def session_service(self, tmp_path):
        """SessionService với temp directory."""
        service = SessionService()
        # Override session file path
        service._session_file = tmp_path / "sessions.json"
        service._sessions = {}
        return service
    
    def test_create_session(self, session_service):
        """Tạo session mới."""
        token = session_service.create_session(
            user_id=1,
            username="testuser",
            role="STUDENT",
            remember_me=False
        )
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_validate_session_valid(self, session_service):
        """Validate session hợp lệ."""
        token = session_service.create_session(
            user_id=1,
            username="testuser",
            role="STUDENT"
        )
        
        session = session_service.validate_session(token)
        
        assert session is not None
        assert session["user_id"] == 1
        assert session["username"] == "testuser"
        assert session["role"] == "STUDENT"
    
    def test_validate_session_invalid_token(self, session_service):
        """Validate session với token không tồn tại."""
        session = session_service.validate_session("invalid_token")
        
        assert session is None
    
    def test_validate_session_empty_token(self, session_service):
        """Validate session với token rỗng."""
        session = session_service.validate_session("")
        
        assert session is None
    
    def test_destroy_session(self, session_service):
        """Hủy session."""
        token = session_service.create_session(
            user_id=1,
            username="testuser",
            role="STUDENT"
        )
        
        result = session_service.destroy_session(token)
        
        assert result is True
        assert session_service.validate_session(token) is None
    
    def test_destroy_session_not_found(self, session_service):
        """Hủy session không tồn tại."""
        result = session_service.destroy_session("not_exists")
        
        assert result is False
    
    def test_get_session_user_id(self, session_service):
        """Lấy user ID từ session."""
        token = session_service.create_session(
            user_id=42,
            username="testuser",
            role="STUDENT"
        )
        
        user_id = session_service.get_session_user_id(token)
        
        assert user_id == 42
    
    def test_get_session_user_id_invalid(self, session_service):
        """Lấy user ID với token invalid."""
        user_id = session_service.get_session_user_id("invalid")
        
        assert user_id is None
    
    def test_remember_me_session(self, session_service):
        """Session với remember_me có thời gian dài hơn."""
        token_normal = session_service.create_session(
            user_id=1,
            username="user1",
            role="STUDENT",
            remember_me=False
        )
        
        token_remember = session_service.create_session(
            user_id=2,
            username="user2",
            role="STUDENT",
            remember_me=True
        )
        
        session_normal = session_service._sessions[token_normal]
        session_remember = session_service._sessions[token_remember]
        
        expires_normal = datetime.fromisoformat(session_normal["expires_at"])
        expires_remember = datetime.fromisoformat(session_remember["expires_at"])
        
        # Remember me session phải có expiry xa hơn
        assert expires_remember > expires_normal
    
    def test_destroy_user_sessions(self, session_service):
        """Hủy tất cả sessions của một user."""
        # Create multiple sessions for same user
        session_service.create_session(1, "user1", "STUDENT")
        session_service.create_session(1, "user1", "STUDENT")
        session_service.create_session(2, "user2", "STUDENT")
        
        count = session_service.destroy_user_sessions(1)
        
        assert count == 2
        assert session_service.get_active_sessions_count(1) == 0
        assert session_service.get_active_sessions_count(2) == 1
