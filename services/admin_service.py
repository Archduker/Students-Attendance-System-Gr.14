"""
Admin Service - Admin Business Logic
====================================

Service xử lý logic nghiệp vụ cho admin:
- Quản lý users
- Quản lý classes
- Thống kê hệ thống
- Báo cáo
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta

from core.enums import UserRole
from core.models import User, Admin, Teacher, Student, Classroom
from data.repositories import UserRepository, ClassroomRepository, AttendanceSessionRepository
from services.security_service import SecurityService


class AdminService:
    """
    Service xử lý admin operations.
    
    Features:
        - User management (CRUD)
        - Class management (CRUD)
        - System statistics
        - Reports generation
        
    Example:
        >>> admin_service = AdminService(user_repo, class_repo, security)
        >>> stats = admin_service.get_dashboard_stats()
        >>> users = admin_service.get_all_users()
    """
    
    def __init__(
        self,
        user_repo: UserRepository,
        classroom_repo: ClassroomRepository,
        attendance_repo: AttendanceSessionRepository,
        security_service: SecurityService
    ):
        """
        Khởi tạo AdminService.
        
        Args:
            user_repo: UserRepository instance
            classroom_repo: ClassroomRepository instance
            attendance_repo: AttendanceSessionRepository instance
            security_service: SecurityService instance
        """
        self.user_repo = user_repo
        self.classroom_repo = classroom_repo
        self.attendance_repo = attendance_repo
        self.security = security_service
    
    # ==================== Dashboard ====================
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Lấy thống kê cho admin dashboard.
        
        Returns:
            Dict chứa các thống kê:
            - total_users
            - total_classes
            - total_sessions
            - recent_activity
        """
        # Count users
        all_users = self.user_repo.find_all()
        total_users = len(all_users)
        
        # Count by role
        admins = len([u for u in all_users if u.role == UserRole.ADMIN])
        teachers = len([u for u in all_users if u.role == UserRole.TEACHER])
        students = len([u for u in all_users if u.role == UserRole.STUDENT])
        
        # Count classes
        all_classes = self.classroom_repo.find_all()
        total_classes = len(all_classes)
        
        # Count sessions (this month)
        # TODO: Implement once AttendanceSessionRepository is available
        total_sessions = 0
        
        return {
            "total_users": total_users,
            "total_admins": admins,
            "total_teachers": teachers,
            "total_students": students,
            "total_classes": total_classes,
            "total_sessions": total_sessions,
            "recent_activity": []  # TODO: Implement activity log
        }
    
    # ==================== User Management ====================
    
    def get_all_users(self, role_filter: Optional[UserRole] = None) -> List[Dict[str, Any]]:
        """
        Lấy danh sách tất cả users.
        
        Args:
            role_filter: Filter theo role (optional)
            
        Returns:
            List các user dicts
        """
        if role_filter:
            users = self.user_repo.find_by_role(role_filter)
        else:
            users = self.user_repo.find_all()
        
        return [user.to_dict() for user in users]
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin một user.
        
        Args:
            user_id: ID của user
            
        Returns:
            User dict hoặc None
        """
        user = self.user_repo.find_by_id(user_id)
        return user.to_dict() if user else None
    
    def create_user(self, user_data: Dict[str, Any]) -> Tuple[bool, str, Optional[str]]:
        """
        Tạo user mới.
        
        Args:
            user_data: Dict chứa thông tin user:
                - username (required)
                - full_name (required)
                - role (required)
                - email (optional)
                - teacher_code (optional, for teachers)
                - student_code (optional, for students)
                
        Returns:
            Tuple (success, message, generated_password)
        """
        try:
            # Validate required fields
            username = user_data.get("username", "").strip()
            full_name = user_data.get("full_name", "").strip()
            role_str = user_data.get("role", "").upper()
            
            if not username or not full_name or not role_str:
                return False, "Username, full name, and role are required", None
            
            # Check if username exists
            if self.user_repo.username_exists(username):
                return False, f"Username '{username}' already exists", None
            
            # Parse role
            try:
                role = UserRole.from_string(role_str)
            except ValueError:
                return False, f"Invalid role: {role_str}", None
            
            # Generate password
            password = self.security.generate_code(8)
            password_hash = self.security.hash_password(password)
            
            # Create user object based on role
            user_id = self._get_next_user_id()
            
            if role == UserRole.ADMIN:
                user = Admin(
                    user_id=user_id,
                    username=username,
                    password_hash=password_hash,
                    full_name=full_name,
                    role=role,
                    email=user_data.get("email"),
                    admin_id=user_data.get("admin_id", f"AD{user_id:03d}")
                )
            elif role == UserRole.TEACHER:
                user = Teacher(
                    user_id=user_id,
                    username=username,
                    password_hash=password_hash,
                    full_name=full_name,
                    role=role,
                    email=user_data.get("email"),
                    teacher_code=user_data.get("teacher_code", f"GV{user_id:03d}")
                )
            elif role == UserRole.STUDENT:
                user = Student(
                    user_id=user_id,
                    username=username,
                    password_hash=password_hash,
                    full_name=full_name,
                    role=role,
                    email=user_data.get("email"),
                    student_code=user_data.get("student_code", f"SV{user_id:03d}")
                )
            else:
                user = User(
                    user_id=user_id,
                    username=username,
                    password_hash=password_hash,
                    full_name=full_name,
                    role=role,
                    email=user_data.get("email")
                )
            
            # Save to database
            created_user = self.user_repo.create(user)
            
            if created_user:
                return True, "User created successfully", password
            else:
                return False, "Failed to create user", None
                
        except Exception as e:
            return False, f"Error creating user: {str(e)}", None
    
    def update_user(self, user_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Cập nhật thông tin user.
        
        Args:
            user_data: Dict chứa thông tin cần update (phải có user_id)
            
        Returns:
            Tuple (success, message)
        """
        try:
            user_id = user_data.get("user_id")
            if not user_id:
                return False, "User ID is required"
            
            # Find existing user
            user = self.user_repo.find_by_id(user_id)
            if not user:
                return False, "User not found"
            
            # Update fields
            if "full_name" in user_data:
                user.full_name = user_data["full_name"]
            
            if "email" in user_data:
                user.email = user_data["email"]
            
            # Update role-specific fields
            if isinstance(user, Teacher) and "teacher_code" in user_data:
                user.teacher_code = user_data["teacher_code"]
            
            if isinstance(user, Student) and "student_code" in user_data:
                user.student_code = user_data["student_code"]
            
            # Save changes
            updated = self.user_repo.update(user)
            
            if updated:
                return True, "User updated successfully"
            else:
                return False, "Failed to update user"
                
        except Exception as e:
            return False, f"Error updating user: {str(e)}"
    
    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """
        Xóa user.
        
        Args:
            user_id: ID của user cần xóa
            
        Returns:
            Tuple (success, message)
        """
        try:
            user = self.user_repo.find_by_id(user_id)
            if not user:
                return False, "User not found"
            
            # Prevent deleting the last admin
            if user.role == UserRole.ADMIN:
                all_admins = self.user_repo.find_by_role(UserRole.ADMIN)
                if len(all_admins) <= 1:
                    return False, "Cannot delete the last admin user"
            
            success = self.user_repo.delete(user_id)
            
            if success:
                return True, "User deleted successfully"
            else:
                return False, "Failed to delete user"
                
        except Exception as e:
            return False, f"Error deleting user: {str(e)}"
    
    def get_teachers(self) -> List[Dict[str, Any]]:
        """
        Lấy danh sách tất cả teachers.
        
        Returns:
            List các teacher dicts
        """
        teachers = self.user_repo.find_by_role(UserRole.TEACHER)
        return [t.to_dict() for t in teachers]
    
    # ==================== Class Management ====================
    
    def get_all_classes(self) -> List[Dict[str, Any]]:
        """
        Lấy danh sách tất cả classes.
        
        Returns:
            List các class dicts
        """
        classes = self.classroom_repo.find_all()
        result = []
        
        for classroom in classes:
            class_dict = classroom.to_dict()
            # Add student codes
            students = self.classroom_repo.get_students_in_class(classroom.class_id)
            class_dict["student_codes"] = students
            result.append(class_dict)
        
        return result
    
    def get_class(self, class_id: str) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin một class.
        
        Args:
            class_id: ID của class
            
        Returns:
            Class dict hoặc None
        """
        classroom = self.classroom_repo.find_by_id(class_id)
        if not classroom:
            return None
        
        class_dict = classroom.to_dict()
        students = self.classroom_repo.get_students_in_class(class_id)
        class_dict["student_codes"] = students
        
        return class_dict
    
    def create_class(self, class_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Tạo class mới.
        
        Args:
            class_data: Dict chứa thông tin class:
                - class_id (required)
                - class_name (required)
                - subject_code (required)
                - teacher_code (optional)
                
        Returns:
            Tuple (success, message)
        """
        try:
            # Validate required fields
            class_id = class_data.get("class_id", "").strip()
            class_name = class_data.get("class_name", "").strip()
            subject_code = class_data.get("subject_code", "").strip()
            
            if not class_id or not class_name or not subject_code:
                return False, "Class ID, name, and subject code are required"
            
            # Check if class ID exists
            existing = self.classroom_repo.find_by_id(class_id)
            if existing:
                return False, f"Class ID '{class_id}' already exists"
            
            # Validate teacher if provided
            teacher_code = class_data.get("teacher_code")
            if teacher_code:
                teacher = self.user_repo.find_by_teacher_code(teacher_code)
                if not teacher:
                    return False, f"Teacher '{teacher_code}' not found"
            
            # Create classroom
            classroom = Classroom(
                class_id=class_id,
                class_name=class_name,
                subject_code=subject_code,
                teacher_code=teacher_code
            )
            
            created = self.classroom_repo.create(classroom)
            
            if created:
                return True, "Class created successfully"
            else:
                return False, "Failed to create class"
                
        except Exception as e:
            return False, f"Error creating class: {str(e)}"
    
    def update_class(self, class_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Cập nhật thông tin class.
        
        Args:
            class_data: Dict chứa thông tin cần update (phải có class_id)
            
        Returns:
            Tuple (success, message)
        """
        try:
            class_id = class_data.get("class_id")
            if not class_id:
                return False, "Class ID is required"
            
            # Find existing class
            classroom = self.classroom_repo.find_by_id(class_id)
            if not classroom:
                return False, "Class not found"
            
            # Update fields
            if "class_name" in class_data:
                classroom.class_name = class_data["class_name"]
            
            if "subject_code" in class_data:
                classroom.subject_code = class_data["subject_code"]
            
            if "teacher_code" in class_data:
                teacher_code = class_data["teacher_code"]
                if teacher_code:
                    teacher = self.user_repo.find_by_teacher_code(teacher_code)
                    if not teacher:
                        return False, f"Teacher '{teacher_code}' not found"
                classroom.teacher_code = teacher_code
            
            # Save changes
            updated = self.classroom_repo.update(classroom)
            
            if updated:
                return True, "Class updated successfully"
            else:
                return False, "Failed to update class"
                
        except Exception as e:
            return False, f"Error updating class: {str(e)}"
    
    def delete_class(self, class_id: str) -> Tuple[bool, str]:
        """
        Xóa class.
        
        Args:
            class_id: ID của class cần xóa
            
        Returns:
            Tuple (success, message)
        """
        try:
            classroom = self.classroom_repo.find_by_id(class_id)
            if not classroom:
                return False, "Class not found"
            
            success = self.classroom_repo.delete(class_id)
            
            if success:
                return True, "Class deleted successfully"
            else:
                return False, "Failed to delete class"
                
        except Exception as e:
            return False, f"Error deleting class: {str(e)}"
    
    def add_student_to_class(self, class_id: str, student_code: str) -> Tuple[bool, str]:
        """
        Thêm student vào class.
        
        Args:
            class_id: ID của class
            student_code: Mã sinh viên
            
        Returns:
            Tuple (success, message)
        """
        try:
            # Verify class exists
            classroom = self.classroom_repo.find_by_id(class_id)
            if not classroom:
                return False, "Class not found"
            
            # Verify student exists
            student = self.user_repo.find_by_student_code(student_code)
            if not student:
                return False, f"Student '{student_code}' not found"
            
            success = self.classroom_repo.add_student_to_class(class_id, student_code)
            
            if success:
                return True, "Student added to class successfully"
            else:
                return False, "Failed to add student to class (may already be enrolled)"
                
        except Exception as e:
            return False, f"Error adding student to class: {str(e)}"
    
    def remove_student_from_class(self, class_id: str, student_code: str) -> Tuple[bool, str]:
        """
        Xóa student khỏi class.
        
        Args:
            class_id: ID của class
            student_code: Mã sinh viên
            
        Returns:
            Tuple (success, message)
        """
        try:
            success = self.classroom_repo.remove_student_from_class(class_id, student_code)
            
            if success:
                return True, "Student removed from class successfully"
            else:
                return False, "Failed to remove student from class"
                
        except Exception as e:
            return False, f"Error removing student from class: {str(e)}"
    
    # ==================== Helper Methods ====================
    
    def _get_next_user_id(self) -> int:
        """Generate next user ID."""
        all_users = self.user_repo.find_all()
        if not all_users:
            return 1
        return max(user.user_id for user in all_users) + 1
