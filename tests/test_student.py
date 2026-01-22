"""
Unit Tests for Student Module
==============================

Tests cho:
- StudentService
- StudentController
- Student models
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch

# Import modules cần test
from services.student_service import StudentService
from controllers.student_controller import StudentController
from core.models import Student, AttendanceRecord, AttendanceSession
from core.enums import UserRole, AttendanceStatus, AttendanceMethod
from core.exceptions import NotFoundError, ValidationError


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def mock_repositories():
    """Mock repositories."""
    return {
        'user_repo': Mock(),
        'attendance_record_repo': Mock(),
        'attendance_session_repo': Mock(),
        'class_repo': Mock()
    }


@pytest.fixture
def student_service(mock_repositories):
    """StudentService instance với mock repos."""
    return StudentService(
        user_repo=mock_repositories['user_repo'],
        attendance_record_repo=mock_repositories['attendance_record_repo'],
        attendance_session_repo=mock_repositories['attendance_session_repo'],
        class_repo=mock_repositories['class_repo']
    )


@pytest.fixture
def student_controller(student_service):
    """StudentController instance."""
    return StudentController(student_service)


@pytest.fixture
def sample_student():
    """Sample student object."""
    return Student(
        user_id=1,
        username="sv001",
        password_hash="hashed_password",
        full_name="Nguyễn Văn A",
        role=UserRole.STUDENT,
        email="nva@email.com",
        student_code="SV001",
        class_name="CNPM01"
    )


@pytest.fixture
def sample_attendance_records():
    """Sample attendance records."""
    return [
        AttendanceRecord(
            record_id="REC001",
            session_id="SESSION001",
            student_code="SV001",
            attendance_time=datetime.now() - timedelta(days=1),
            status=AttendanceStatus.PRESENT,
            remark=""
        ),
        AttendanceRecord(
            record_id="REC002",
            session_id="SESSION002",
            student_code="SV001",
            attendance_time=datetime.now() - timedelta(days=2),
            status=AttendanceStatus.ABSENT,
            remark=""
        ),
        AttendanceRecord(
            record_id="REC003",
            session_id="SESSION003",
            student_code="SV001",
            attendance_time=datetime.now() - timedelta(days=3),
            status=AttendanceStatus.PRESENT,
            remark=""
        )
    ]


@pytest.fixture
def sample_session():
    """Sample attendance session."""
    return AttendanceSession(
        session_id="SESSION001",
        class_id="CS101",
        start_time=datetime.now() - timedelta(minutes=30),
        end_time=datetime.now() + timedelta(minutes=30),
        method=AttendanceMethod.LINK_TOKEN,
        token="TOKEN123",
        status="OPEN"
    )


# =============================================================================
# STUDENT SERVICE TESTS
# =============================================================================

class TestStudentService:
    """Tests cho StudentService."""
    
    def test_get_dashboard_stats_success(
        self,
        student_service,
        mock_repositories,
        sample_attendance_records
    ):
        """Test lấy dashboard stats thành công."""
        # Setup mock
        mock_repositories['attendance_record_repo'].find_by_student.return_value = \
            sample_attendance_records
        
        # Execute
        stats = student_service.get_dashboard_stats("SV001")
        
        # Assert
        assert stats['total_sessions'] == 3
        assert stats['present_count'] == 2
        assert stats['absent_count'] == 1
        assert stats['attendance_rate'] == 66.67
        assert len(stats['recent_attendance']) <= 5
    
    def test_get_dashboard_stats_no_records(
        self,
        student_service,
        mock_repositories
    ):
        """Test dashboard stats khi không có records."""
        # Setup
        mock_repositories['attendance_record_repo'].find_by_student.return_value = []
        
        # Execute
        stats = student_service.get_dashboard_stats("SV001")
        
        # Assert
        assert stats['total_sessions'] == 0
        assert stats['attendance_rate'] == 0
        assert stats['recent_attendance'] == []
    
    def test_submit_attendance_success(
        self,
        student_service,
        mock_repositories,
        sample_session
    ):
        """Test submit attendance thành công."""
        # Setup
        mock_repositories['attendance_session_repo'].find_by_id.return_value = sample_session
        mock_repositories['attendance_record_repo'].find_by_session_and_student.return_value = None
        mock_repositories['attendance_record_repo'].create.return_value = True
        
        # Execute
        success, message = student_service.submit_attendance(
            "SV001",
            "SESSION001",
            "TOKEN123"
        )
        
        # Assert
        assert success is True
        assert "thành công" in message.lower()
        mock_repositories['attendance_record_repo'].create.assert_called_once()
    
    def test_submit_attendance_session_not_found(
        self,
        student_service,
        mock_repositories
    ):
        """Test submit attendance khi session không tồn tại."""
        # Setup
        mock_repositories['attendance_session_repo'].find_by_id.return_value = None
        
        # Execute & Assert
        with pytest.raises(NotFoundError):
            student_service.submit_attendance("SV001", "INVALID_SESSION", "TOKEN")
    
    def test_submit_attendance_session_closed(
        self,
        student_service,
        mock_repositories,
        sample_session
    ):
        """Test submit attendance khi session đã đóng."""
        # Setup
        sample_session.status = "CLOSED"
        mock_repositories['attendance_session_repo'].find_by_id.return_value = sample_session
        
        # Execute
        success, message = student_service.submit_attendance("SV001", "SESSION001", "TOKEN")
        
        # Assert
        assert success is False
        assert "đóng" in message.lower()
    
    def test_submit_attendance_already_submitted(
        self,
        student_service,
        mock_repositories,
        sample_session,
        sample_attendance_records
    ):
        """Test submit attendance khi đã điểm danh rồi."""
        # Setup
        mock_repositories['attendance_session_repo'].find_by_id.return_value = sample_session
        mock_repositories['attendance_record_repo'].find_by_session_and_student.return_value = \
            sample_attendance_records[0]
        
        # Execute
        success, message = student_service.submit_attendance("SV001", "SESSION001", "TOKEN")
        
        # Assert
        assert success is False
        assert "đã điểm danh" in message.lower()
    
    def test_submit_attendance_invalid_token(
        self,
        student_service,
        mock_repositories,
        sample_session
    ):
        """Test submit attendance với token không hợp lệ."""
        # Setup
        mock_repositories['attendance_session_repo'].find_by_id.return_value = sample_session
        mock_repositories['attendance_record_repo'].find_by_session_and_student.return_value = None
        
        # Execute
        success, message = student_service.submit_attendance(
            "SV001",
            "SESSION001",
            "WRONG_TOKEN"
        )
        
        # Assert
        assert success is False
        assert "token" in message.lower()
    
    def test_get_attendance_history(
        self,
        student_service,
        mock_repositories,
        sample_attendance_records
    ):
        """Test lấy attendance history."""
        # Setup
        mock_repositories['attendance_record_repo'].find_by_student.return_value = \
            sample_attendance_records
        mock_repositories['attendance_session_repo'].find_by_id.return_value = Mock(class_id="CS101")
        mock_repositories['class_repo'].find_by_id.return_value = Mock(class_name="Computer Science")
        
        # Execute
        history = student_service.get_attendance_history("SV001")
        
        # Assert
        assert len(history) == 3
        assert history[0]['student_code'] == "SV001" or 'record_id' in history[0]
    
    def test_update_profile_success(
        self,
        student_service,
        mock_repositories,
        sample_student
    ):
        """Test update profile thành công."""
        # Setup
        mock_repositories['user_repo'].find_by_student_code.return_value = sample_student
        mock_repositories['user_repo'].update_student_profile.return_value = True
        
        # Execute
        success, message = student_service.update_profile(
            "SV001",
            full_name="Nguyễn Văn B",
            email="nvb@email.com"
        )
        
        # Assert
        assert success is True
        assert "thành công" in message.lower()
    
    def test_update_profile_invalid_email(
        self,
        student_service,
        mock_repositories,
        sample_student
    ):
        """Test update profile với email không hợp lệ."""
        # Setup
        mock_repositories['user_repo'].find_by_student_code.return_value = sample_student
        
        # Execute
        success, message = student_service.update_profile(
            "SV001",
            email="invalid_email"
        )
        
        # Assert
        assert success is False
        assert "email" in message.lower()


# =============================================================================
# STUDENT CONTROLLER TESTS
# =============================================================================

class TestStudentController:
    """Tests cho StudentController."""
    
    def test_handle_get_dashboard_success(
        self,
        student_controller,
        student_service
    ):
        """Test handle get dashboard request."""
        # Setup
        student_service.get_dashboard_stats = Mock(return_value={
            'attendance_rate': 75.0,
            'total_sessions': 10
        })
        student_service.get_class_schedule = Mock(return_value=[])
        student_service.get_student_info = Mock(return_value={'student_code': 'SV001'})
        
        # Execute
        result = student_controller.handle_get_dashboard("SV001")
        
        # Assert
        assert result['success'] is True
        assert 'data' in result
        assert 'statistics' in result['data']
    
    def test_handle_get_dashboard_invalid_code(
        self,
        student_controller
    ):
        """Test handle get dashboard với mã sinh viên không hợp lệ."""
        # Execute
        result = student_controller.handle_get_dashboard("")
        
        # Assert
        assert result['success'] is False
        assert 'error' in result
    
    def test_handle_submit_attendance_success(
        self,
        student_controller,
        student_service
    ):
        """Test handle submit attendance."""
        # Setup
        student_service.submit_attendance = Mock(return_value=(True, "Thành công"))
        
        # Execute
        result = student_controller.handle_submit_attendance(
            "SV001",
            "SESSION001",
            "TOKEN123"
        )
        
        # Assert
        assert result['success'] is True
        assert result['message'] == "Thành công"
    
    def test_handle_submit_attendance_validation_error(
        self,
        student_controller
    ):
        """Test validation lỗi khi submit attendance."""
        # Execute - empty student code
        result = student_controller.handle_submit_attendance("", "SESSION001", "TOKEN")
        assert result['success'] is False
        
        # Execute - empty session ID
        result = student_controller.handle_submit_attendance("SV001", "", "TOKEN")
        assert result['success'] is False
    
    def test_handle_get_attendance_history_with_filters(
        self,
        student_controller,
        student_service
    ):
        """Test lấy history với filters."""
        # Setup
        student_service.get_attendance_history = Mock(return_value=[])
        
        # Execute
        filters = {
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'class_id': 'CS101'
        }
        result = student_controller.handle_get_attendance_history("SV001", filters)
        
        # Assert
        assert result['success'] is True
        assert 'data' in result
        student_service.get_attendance_history.assert_called_once()
    
    def test_handle_update_profile(
        self,
        student_controller,
        student_service
    ):
        """Test handle update profile."""
        # Setup
        student_service.update_profile = Mock(return_value=(True, "Success"))
        
        # Execute
        profile_data = {
            'full_name': 'New Name',
            'email': 'newemail@test.com'
        }
        result = student_controller.handle_update_profile("SV001", profile_data)
        
        # Assert
        assert result['success'] is True
    
    def test_validate_student_code(
        self,
        student_controller
    ):
        """Test validation của student code."""
        # Valid codes
        assert student_controller.validate_student_code("SV001") is True
        assert student_controller.validate_student_code("STUDENT01") is True
        
        # Invalid codes
        assert student_controller.validate_student_code("") is False
        assert student_controller.validate_student_code("   ") is False
        assert student_controller.validate_student_code("SV") is False  # Too short
        assert student_controller.validate_student_code("VERYLONGSTUDENTCODE123") is False  # Too long


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestStudentModuleIntegration:
    """Integration tests cho Student module."""
    
    def test_full_attendance_flow(
        self,
        student_service,
        mock_repositories,
        sample_session
    ):
        """Test flow đầy đủ từ submit đến view history."""
        # Setup
        mock_repositories['attendance_session_repo'].find_by_id.return_value = sample_session
        mock_repositories['attendance_record_repo'].find_by_session_and_student.return_value = None
        mock_repositories['attendance_record_repo'].create.return_value = True
        mock_repositories['attendance_record_repo'].find_by_student.return_value = []
        
        # Step 1: Submit attendance
        success, msg = student_service.submit_attendance("SV001", "SESSION001", "TOKEN123")
        assert success is True
        
        # Step 2: View history (should include new record in real scenario)
        history = student_service.get_attendance_history("SV001")
        assert isinstance(history, list)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
