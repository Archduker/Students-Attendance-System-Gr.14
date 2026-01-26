"""
Classroom Repository - Class Data Access
=========================================

Repository cho các thao tác CRUD với Classroom.
"""

from typing import Any, Dict, List, Optional

from core.models import Classroom
from data.database import Database
from .base_repository import BaseRepository


class ClassroomRepository(BaseRepository[Classroom]):
    """
    Repository cho Classroom entity.
    
    Example:
        >>> class_repo = ClassroomRepository(db)
        >>> classes = class_repo.find_by_teacher("GV001")
    """
    
    @property
    def table_name(self) -> str:
        return "classes"
    
    def _row_to_entity(self, row) -> Classroom:
        """Chuyển đổi row thành Classroom."""
        # sqlite3.Row supports dict-style access but not .get()
        return Classroom(
            class_id=row["class_id"],
            class_name=row["class_name"],
            subject_code=row["subject_code"],
            teacher_code=row["teacher_code"] if "teacher_code" in row.keys() else None
        )
    
    def _entity_to_dict(self, entity: Classroom) -> Dict[str, Any]:
        """Chuyển đổi Classroom thành dictionary."""
        return {
            "class_id": entity.class_id,
            "class_name": entity.class_name,
            "subject_code": entity.subject_code,
            "teacher_code": entity.teacher_code,
        }
    
    def find_by_id(self, class_id: str) -> Optional[Classroom]:
        """
        Override find_by_id to use class_id instead of id.
        
        Args:
            class_id: Class ID
            
        Returns:
            Classroom object or None
        """
        query = f"SELECT * FROM {self.table_name} WHERE class_id = ?"
        row = self.db.fetch_one(query, (class_id,))
        return self._row_to_entity(row) if row else None
    
    def find_by_teacher(self, teacher_code: str) -> List[Classroom]:
        """
        Lấy các lớp của một giáo viên.
        
        Args:
            teacher_code: Mã giáo viên
            
        Returns:
            List các Classroom
        """
        query = f"SELECT * FROM {self.table_name} WHERE teacher_code = ?"
        rows = self.db.fetch_all(query, (teacher_code,))
        return [self._row_to_entity(row) for row in rows]
    
    def find_by_subject(self, subject_code: str) -> List[Classroom]:
        """
        Lấy các lớp của một môn học.
        
        Args:
            subject_code: Mã môn học
            
        Returns:
            List các Classroom
        """
        query = f"SELECT * FROM {self.table_name} WHERE subject_code = ?"
        rows = self.db.fetch_all(query, (subject_code,))
        return [self._row_to_entity(row) for row in rows]
    
    def get_students_in_class(self, class_id: str) -> List[str]:
        """
        Lấy danh sách mã sinh viên trong lớp.
        
        Args:
            class_id: Mã lớp
            
        Returns:
            List các student_code
        """
        query = "SELECT student_code FROM classes_student WHERE class_id = ?"
        rows = self.db.fetch_all(query, (class_id,))
        return [row["student_code"] for row in rows]
    
    def add_student_to_class(self, class_id: str, student_code: str) -> bool:
        """
        Thêm sinh viên vào lớp.
        
        Args:
            class_id: Mã lớp
            student_code: Mã sinh viên
            
        Returns:
            True nếu thêm thành công
        """
        query = "INSERT INTO classes_student (class_id, student_code) VALUES (?, ?)"
        try:
            self.db.execute(query, (class_id, student_code))
            return True
        except Exception:
            return False
    
    def remove_student_from_class(self, class_id: str, student_code: str) -> bool:
        """
        Xóa sinh viên khỏi lớp.
        
        Args:
            class_id: Mã lớp
            student_code: Mã sinh viên
            
        Returns:
            True nếu xóa thành công
        """
        query = "DELETE FROM classes_student WHERE class_id = ? AND student_code = ?"
        cursor = self.db.execute(query, (class_id, student_code))
        return cursor.rowcount > 0
    
    def get_classes_for_student(self, student_code: str) -> List[Classroom]:
        """
        Lấy các lớp mà sinh viên đang học.
        
        Args:
            student_code: Mã sinh viên
            
        Returns:
            List các Classroom
        """
        query = """
            SELECT c.* FROM classes c
            JOIN classes_student cs ON c.class_id = cs.class_id
            WHERE cs.student_code = ?
        """
        rows = self.db.fetch_all(query, (student_code,))
        return [self._row_to_entity(row) for row in rows]
