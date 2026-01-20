"""
Classroom Model - Model lớp học
===============================

Định nghĩa model cho lớp học trong hệ thống.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Classroom:
    """
    Model đại diện cho một lớp học.
    
    Attributes:
        class_id: Mã lớp (VD: "CS101-2024")
        class_name: Tên lớp học
        subject_code: Mã môn học
        teacher_code: Mã giáo viên phụ trách
        student_codes: Danh sách mã sinh viên trong lớp
        
    Example:
        >>> classroom = Classroom(
        ...     class_id="CS101-2024",
        ...     class_name="Lập trình Python",
        ...     subject_code="CS101",
        ...     teacher_code="GV001"
        ... )
    """
    
    class_id: str
    class_name: str
    subject_code: str
    teacher_code: Optional[str] = None
    student_codes: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate data sau khi khởi tạo."""
        if not self.class_id:
            raise ValueError("Class ID không được để trống")
        if not self.class_name:
            raise ValueError("Class name không được để trống")
    
    def add_student(self, student_code: str) -> None:
        """
        Thêm sinh viên vào lớp.
        
        Args:
            student_code: Mã sinh viên cần thêm
        """
        if student_code not in self.student_codes:
            self.student_codes.append(student_code)
    
    def remove_student(self, student_code: str) -> bool:
        """
        Xóa sinh viên khỏi lớp.
        
        Args:
            student_code: Mã sinh viên cần xóa
            
        Returns:
            True nếu xóa thành công, False nếu không tìm thấy
        """
        if student_code in self.student_codes:
            self.student_codes.remove(student_code)
            return True
        return False
    
    @property
    def student_count(self) -> int:
        """Số lượng sinh viên trong lớp."""
        return len(self.student_codes)
    
    def to_dict(self) -> dict:
        """Chuyển đổi thành dictionary."""
        return {
            "class_id": self.class_id,
            "class_name": self.class_name,
            "subject_code": self.subject_code,
            "teacher_code": self.teacher_code,
            "student_codes": self.student_codes,
            "student_count": self.student_count,
        }
