"""
Attendance Status Enum - Trạng thái điểm danh
==============================================

Định nghĩa các trạng thái điểm danh:
- PRESENT: Có mặt
- ABSENT: Vắng mặt
"""

from enum import Enum


class AttendanceStatus(Enum):
    """
    Enum định nghĩa trạng thái điểm danh của sinh viên.
    
    Attributes:
        PRESENT: Có mặt - sinh viên đã điểm danh thành công
        ABSENT: Vắng mặt - sinh viên không điểm danh
        
    Example:
        >>> from core.enums import AttendanceStatus
        >>> status = AttendanceStatus.PRESENT
        >>> print(status.value)
        PRESENT
    """
    
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    
    @classmethod
    def from_string(cls, status_str: str) -> "AttendanceStatus":
        """
        Chuyển đổi string thành AttendanceStatus enum.
        
        Args:
            status_str: Chuỗi trạng thái (case-insensitive)
            
        Returns:
            AttendanceStatus enum tương ứng
            
        Raises:
            ValueError: Nếu status_str không hợp lệ
        """
        try:
            return cls(status_str.upper())
        except ValueError:
            valid_statuses = [s.value for s in cls]
            raise ValueError(
                f"Invalid status: '{status_str}'. "
                f"Valid statuses: {valid_statuses}"
            )
    
    def is_present(self) -> bool:
        """Kiểm tra trạng thái có mặt."""
        return self == AttendanceStatus.PRESENT
    
    def __str__(self) -> str:
        return self.value
