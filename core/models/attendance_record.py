"""
Attendance Record Model - Model bản ghi điểm danh
==================================================

Định nghĩa model cho bản ghi điểm danh của từng sinh viên.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from core.enums import AttendanceStatus


@dataclass
class AttendanceRecord:
    """
    Model đại diện cho một bản ghi điểm danh.
    
    Attributes:
        record_id: Mã bản ghi
        session_id: Mã phiên điểm danh
        student_code: Mã sinh viên
        attendance_time: Thời gian điểm danh
        status: Trạng thái (PRESENT, ABSENT)
        remark: Ghi chú (nếu có)
        
    Example:
        >>> record = AttendanceRecord(
        ...     record_id="REC001",
        ...     session_id="SS001",
        ...     student_code="SV001",
        ...     status=AttendanceStatus.PRESENT
        ... )
    """
    
    record_id: str
    session_id: str
    student_code: str
    status: AttendanceStatus = AttendanceStatus.ABSENT
    attendance_time: Optional[datetime] = None
    remark: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate data sau khi khởi tạo."""
        if not self.record_id:
            raise ValueError("Record ID không được để trống")
        if not self.session_id:
            raise ValueError("Session ID không được để trống")
        if not self.student_code:
            raise ValueError("Student code không được để trống")
    
    def mark_present(self, time: Optional[datetime] = None) -> None:
        """
        Đánh dấu có mặt.
        
        Args:
            time: Thời gian điểm danh (mặc định là thời gian hiện tại)
        """
        self.status = AttendanceStatus.PRESENT
        self.attendance_time = time or datetime.now()
    
    def mark_absent(self, remark: Optional[str] = None) -> None:
        """
        Đánh dấu vắng mặt.
        
        Args:
            remark: Ghi chú lý do vắng (nếu có)
        """
        self.status = AttendanceStatus.ABSENT
        self.attendance_time = None
        if remark:
            self.remark = remark
    
    def update_status(self, new_status: AttendanceStatus) -> None:
        """
        Cập nhật trạng thái điểm danh.
        
        Args:
            new_status: Trạng thái mới
        """
        self.status = new_status
        if new_status == AttendanceStatus.PRESENT and not self.attendance_time:
            self.attendance_time = datetime.now()
    
    def is_present(self) -> bool:
        """Kiểm tra sinh viên có mặt không."""
        return self.status == AttendanceStatus.PRESENT
    
    def to_dict(self) -> dict:
        """Chuyển đổi thành dictionary."""
        return {
            "record_id": self.record_id,
            "session_id": self.session_id,
            "student_code": self.student_code,
            "status": self.status.value,
            "attendance_time": self.attendance_time.isoformat() if self.attendance_time else None,
            "remark": self.remark,
            "created_at": self.created_at.isoformat(),
        }
