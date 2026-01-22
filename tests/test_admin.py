"""
Admin Module Tests
==================

Unit tests cho Admin module:
- AdminService tests
- AdminController tests
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from services.admin_service import AdminService
from controllers.admin_controller import AdminController
from core.enums import UserRole
from core.models import User, Admin, Teacher, Student, Classroom


class TestAdminService(unittest.TestCase):
    """Test cases cho AdminService."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.user_repo = Mock()
        self.classroom_repo = Mock()
        self.attendance_repo = Mock()
        self.security = Mock()
        
        self.service = AdminService(
            self.user_repo,
            self.classroom_repo,
            self.attendance_repo,
            self.security
        )
    
    def test_get_dashboard_stats(self):
        """Test get dashboard statistics."""
        # Setup mock data
        admin_user = Admin(1, "admin", "hash", "Admin User", UserRole.ADMIN)
        teacher_user = Teacher(2, "teacher", "hash", "Teacher User", UserRole.TEACHER, teacher_code="GV001")
        student_user = Student(3, "student", "hash", "Student User", UserRole.STUDENT, student_code="SV001")
        
        self.user_repo.find_all.return_value = [admin_user, teacher_user, student_user]
        
        classroom = Classroom("CS101", "Intro to CS", "CS101", "GV001")
        self.classroom_repo.find_all.return_value = [classroom]
        
        # Execute
        stats = self.service.get_dashboard_stats()
        
        # Assert
        self.assertEqual(stats["total_users"], 3)
        self.assertEqual(stats["total_admins"], 1)
        self.assertEqual(stats["total_teachers"], 1)
        self.assertEqual(stats["total_students"], 1)
        self.assertEqual(stats["total_classes"], 1)
    
    def test_get_all_users(self):
        """Test get all users."""
        # Setup mock data
        users = [
            Admin(1, "admin", "hash", "Admin", UserRole.ADMIN),
            Teacher(2, "teacher", "hash", "Teacher", UserRole.TEACHER, teacher_code="GV001")
        ]
        self.user_repo.find_all.return_value = users
        
        # Execute
        result = self.service.get_all_users()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["username"], "admin")
        self.assertEqual(result[1]["username"], "teacher")
    
    def test_create_user_success(self):
        """Test create user successfully."""
        # Setup
        self.user_repo.username_exists.return_value = False
        self.user_repo.find_all.return_value = []
        self.security.generate_code.return_value = "testpass"
        self.security.hash_password.return_value = "hashed"
        
        # Create a properly initialized Student object
        created_user = Student(
            user_id=1,
            username="student1",
            password_hash="hashed",
            full_name="Test Student",
            role=UserRole.STUDENT,
            student_code="SV001"
        )
        self.user_repo.create.return_value = created_user
        
        user_data = {
            "username": "student1",
            "full_name": "Test Student",
            "role": "STUDENT",
            "email": "student@test.com"
        }
        
        # Execute
        success, message, password = self.service.create_user(user_data)
        
        # Assert
        self.assertTrue(success, f"Expected success=True, but got: {message}")
        self.assertEqual(password, "testpass")
        self.user_repo.create.assert_called_once()
    
    def test_create_user_duplicate_username(self):
        """Test create user with duplicate username."""
        # Setup
        self.user_repo.username_exists.return_value = True
        
        user_data = {
            "username": "existing",
            "full_name": "Test",
            "role": "STUDENT"
        }
        
        # Execute
        success, message, password = self.service.create_user(user_data)
        
        # Assert
        self.assertFalse(success)
        self.assertIn("already exists", message)
        self.assertIsNone(password)
    
    def test_update_user(self):
        """Test update user."""
        # Setup
        existing_user = Student(1, "student1", "hash", "Old Name", UserRole.STUDENT, student_code="SV001")
        self.user_repo.find_by_id.return_value = existing_user
        self.user_repo.update.return_value = existing_user
        
        user_data = {
            "user_id": 1,
            "full_name": "New Name",
            "email": "new@test.com"
        }
        
        # Execute
        success, message = self.service.update_user(user_data)
        
        # Assert
        self.assertTrue(success)
        self.assertEqual(existing_user.full_name, "New Name")
        self.assertEqual(existing_user.email, "new@test.com")
    
    def test_delete_user(self):
        """Test delete user."""
        # Setup
        user = Student(1, "student1", "hash", "Test", UserRole.STUDENT, student_code="SV001")
        self.user_repo.find_by_id.return_value = user
        self.user_repo.delete.return_value = True
        
        # Execute
        success, message = self.service.delete_user(1)
        
        # Assert
        self.assertTrue(success)
        self.user_repo.delete.assert_called_once_with(1)
    
    def test_delete_last_admin_fails(self):
        """Test that deleting the last admin fails."""
        # Setup
        admin = Admin(1, "admin", "hash", "Admin", UserRole.ADMIN)
        self.user_repo.find_by_id.return_value = admin
        self.user_repo.find_by_role.return_value = [admin]  # Only one admin
        
        # Execute
        success, message = self.service.delete_user(1)
        
        # Assert
        self.assertFalse(success)
        self.assertIn("last admin", message)
    
    def test_create_class(self):
        """Test create class."""
        # Setup
        self.classroom_repo.find_by_id.return_value = None
        created_class = Classroom("CS101", "Intro", "CS101", "GV001")
        self.classroom_repo.create.return_value = created_class
        
        teacher = Teacher(1, "teacher", "hash", "Teacher", UserRole.TEACHER, teacher_code="GV001")
        self.user_repo.find_by_teacher_code.return_value = teacher
        
        class_data = {
            "class_id": "CS101",
            "class_name": "Intro",
            "subject_code": "CS101",
            "teacher_code": "GV001"
        }
        
        # Execute
        success, message = self.service.create_class(class_data)
        
        # Assert
        self.assertTrue(success)
        self.classroom_repo.create.assert_called_once()
    
    def test_add_student_to_class(self):
        """Test add student to class."""
        # Setup
        classroom = Classroom("CS101", "Intro", "CS101", "GV001")
        student = Student(1, "student", "hash", "Student", UserRole.STUDENT, student_code="SV001")
        
        self.classroom_repo.find_by_id.return_value = classroom
        self.user_repo.find_by_student_code.return_value = student
        self.classroom_repo.add_student_to_class.return_value = True
        
        # Execute
        success, message = self.service.add_student_to_class("CS101", "SV001")
        
        # Assert
        self.assertTrue(success)
        self.classroom_repo.add_student_to_class.assert_called_once_with("CS101", "SV001")


class TestAdminController(unittest.TestCase):
    """Test cases cho AdminController."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.admin_service = Mock()
        self.controller = AdminController(self.admin_service)
    
    def test_get_dashboard_stats_success(self):
        """Test get dashboard stats successfully."""
        # Setup
        stats = {
            "total_users": 10,
            "total_classes": 5
        }
        self.admin_service.get_dashboard_stats.return_value = stats
        
        # Execute
        result = self.controller.get_dashboard_stats()
        
        # Assert
        self.assertTrue(result["success"])
        self.assertEqual(result["data"], stats)
    
    def test_get_all_users_success(self):
        """Test get all users successfully."""
        # Setup
        users = [
            {"user_id": 1, "username": "admin"},
            {"user_id": 2, "username": "teacher"}
        ]
        self.admin_service.get_all_users.return_value = users
        
        # Execute
        result = self.controller.get_all_users()
        
        # Assert
        self.assertTrue(result["success"])
        self.assertEqual(result["users"], users)
    
    def test_create_user_success(self):
        """Test create user successfully."""
        # Setup
        self.admin_service.create_user.return_value = (True, "Created", "password123")
        
        user_data = {"username": "new_user", "full_name": "New User", "role": "STUDENT"}
        
        # Execute
        result = self.controller.create_user(user_data)
        
        # Assert
        self.assertTrue(result["success"])
        self.assertEqual(result["password"], "password123")
    
    def test_delete_user_success(self):
        """Test delete user successfully."""
        # Setup
        self.admin_service.delete_user.return_value = (True, "Deleted")
        
        # Execute
        result = self.controller.delete_user(1)
        
        # Assert
        self.assertTrue(result["success"])
        self.assertIsNone(result["error"])


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    run_tests()
