"""
Pytest Configuration - Fixtures
================================

Shared fixtures cho tất cả tests.
"""

import pytest
import sqlite3
from pathlib import Path
import tempfile

from data.database import Database
from services import SecurityService


@pytest.fixture
def temp_db():
    """
    Tạo temporary database cho testing.
    
    Yields:
        Database instance với temp file
    """
    # Create temp file
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_path = f.name
    
    # Override database path
    import config.database as db_config
    original_path = db_config.DATABASE_NAME
    db_config.DATABASE_NAME = temp_path
    
    # Initialize database
    from data.migrations.init_db import init_database
    init_database(reset=True)
    
    db = Database()
    
    yield db
    
    # Cleanup
    db.close()
    db_config.DATABASE_NAME = original_path
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def security_service():
    """SecurityService instance."""
    return SecurityService()


@pytest.fixture
def sample_password():
    """Sample password for testing."""
    return "test_password_123"


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "password": "test123456",
        "full_name": "Test User",
        "email": "test@example.com",
        "role": "STUDENT",
        "student_code": "SV999",
    }
