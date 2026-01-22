"""
User Repository - User Data Access
===================================

Repository cho các thao tác CRUD với User, Admin, Teacher, Student.
"""

from typing import Any, Dict, List, Optional

from core.enums import UserRole
from core.models import User, Admin, Teacher, Student
from data.database import Database
from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository cho User entity.
    
    Handles:
    - User CRUD operations
    - Authentication queries
    - Role-based queries
    
    Example:
        >>> user_repo = UserRepository(db)
        >>> user = user_repo.find_by_username("admin")
        >>> teachers = user_repo.find_by_role(UserRole.TEACHER)
    """
    
    @property
    def table_name(self) -> str:
        return "users"
    
    def _row_to_entity(self, row) -> User:
        """Chuyển đổi row thành User/Admin/Teacher/Student."""
        role = UserRole.from_string(row["role"])
        
        base_data = {
            "user_id": row["user_id"],
            "username": row["username"],
            "password_hash": row["password_hash"],
            "full_name": row["full_name"],
            "role": role,
            "email": row["email"] if row["email"] else None,
        }
        
        # Tạo subclass phù hợp
        if role == UserRole.ADMIN:
            return Admin(**base_data, admin_id=row["admin_id"] if row["admin_id"] else "")
        elif role == UserRole.TEACHER:
            return Teacher(**base_data, teacher_code=row["teacher_code"] if row["teacher_code"] else "")
        elif role == UserRole.STUDENT:
            return Student(**base_data, student_code=row["student_code"] if row["student_code"] else "")
        else:
            return User(**base_data)
    
    def _entity_to_dict(self, entity: User) -> Dict[str, Any]:
        """Chuyển đổi User thành dictionary."""
        data = {
            "user_id": entity.user_id,
            "username": entity.username,
            "password_hash": entity.password_hash,
            "full_name": entity.full_name,
            "role": entity.role.value,
            "email": entity.email,
        }
        
        # Thêm fields theo role
        if isinstance(entity, Admin):
            data["admin_id"] = entity.admin_id
        elif isinstance(entity, Teacher):
            data["teacher_code"] = entity.teacher_code
        elif isinstance(entity, Student):
            data["student_code"] = entity.student_code
        
        return data
    
    def find_by_username(self, username: str) -> Optional[User]:
        """
        Tìm user theo username.
        
        Args:
            username: Tên đăng nhập
            
        Returns:
            User object hoặc None
        """
        query = f"SELECT * FROM {self.table_name} WHERE username = ?"
        row = self.db.fetch_one(query, (username,))
        return self._row_to_entity(row) if row else None
    
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Tìm user theo email.
        
        Args:
            email: Email address
            
        Returns:
            User object hoặc None
        """
        query = f"SELECT * FROM {self.table_name} WHERE email = ?"
        row = self.db.fetch_one(query, (email,))
        return self._row_to_entity(row) if row else None
    
    def find_by_role(self, role: UserRole) -> List[User]:
        """
        Lấy tất cả users theo role.
        
        Args:
            role: UserRole enum
            
        Returns:
            List các users
        """
        query = f"SELECT * FROM {self.table_name} WHERE role = ?"
        rows = self.db.fetch_all(query, (role.value,))
        return [self._row_to_entity(row) for row in rows]
    
    def find_by_teacher_code(self, teacher_code: str) -> Optional[Teacher]:
        """
        Tìm teacher theo mã giáo viên.
        
        Args:
            teacher_code: Mã giáo viên
            
        Returns:
            Teacher object hoặc None
        """
        query = f"SELECT * FROM {self.table_name} WHERE teacher_code = ?"
        row = self.db.fetch_one(query, (teacher_code,))
        return self._row_to_entity(row) if row else None
    
    def find_by_student_code(self, student_code: str) -> Optional[Student]:
        """
        Tìm student theo mã sinh viên.
        
        Args:
            student_code: Mã sinh viên
            
        Returns:
            Student object hoặc None
        """
        query = f"SELECT * FROM {self.table_name} WHERE student_code = ?"
        row = self.db.fetch_one(query, (student_code,))
        return self._row_to_entity(row) if row else None
    
    def username_exists(self, username: str) -> bool:
        """Kiểm tra username đã tồn tại chưa."""
        query = f"SELECT 1 FROM {self.table_name} WHERE username = ? LIMIT 1"
        row = self.db.fetch_one(query, (username,))
        return row is not None
    
    def email_exists(self, email: str) -> bool:
        """Kiểm tra email đã tồn tại chưa."""
        query = f"SELECT 1 FROM {self.table_name} WHERE email = ? LIMIT 1"
        row = self.db.fetch_one(query, (email,))
        return row is not None
    
    def update_password(self, user_id: int, new_password_hash: str) -> bool:
        """
        Cập nhật mật khẩu user.
        
        Args:
            user_id: ID của user
            new_password_hash: Mật khẩu mới đã hash
            
        Returns:
            True nếu cập nhật thành công
        """
        query = f"UPDATE {self.table_name} SET password_hash = ? WHERE user_id = ?"
        cursor = self.db.execute(query, (new_password_hash, user_id))
        return cursor.rowcount > 0
