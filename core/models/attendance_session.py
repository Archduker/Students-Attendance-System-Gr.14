"""
Attendance Session Model - Model phiên điểm danh
=================================================

Định nghĩa model cho phiên điểm danh do giáo viên tạo.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

from core.enums import AttendanceMethod


class SessionStatus(Enum):
    """Trạng thái của phiên điểm danh."""
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass
class AttendanceSession:
    """
    Model đại diện cho một phiên điểm danh.
    
    Attributes:
        session_id: Mã phiên điểm danh
        class_id: Mã lớp học
        start_time: Thời gian bắt đầu
        end_time: Thời gian kết thúc
        method: Phương thức điểm danh (QR, LINK_TOKEN, MANUAL, AUTO)
        status: Trạng thái (OPEN, CLOSED)
        attendance_link: Link điểm danh (nếu có)
        token: Token điểm danh (nếu có)
        qr_window_minutes: Thời gian hiệu lực QR (phút)
        late_window_minutes: Thời gian cho phép trễ (phút)
        
    Example:
        >>> session = AttendanceSession(
        ...     session_id="SS001",
        ...     class_id="CS101-2024",
        ...     start_time=datetime.now(),
        ...     end_time=datetime.now() + timedelta(hours=2),
        ...     method=AttendanceMethod.QR
        ... )
    """
    
    session_id: str
    class_id: str
    start_time: datetime
    end_time: datetime
    method: AttendanceMethod = AttendanceMethod.QR
    status: SessionStatus = SessionStatus.OPEN
    attendance_link: Optional[str] = None
    token: Optional[str] = None
    qr_window_minutes: int = 1  # QR đổi mỗi 1 phút
    late_window_minutes: int = 15  # Cho phép trễ 15 phút
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate data sau khi khởi tạo."""
        if not self.session_id:
            raise ValueError("Session ID không được để trống")
        if self.end_time <= self.start_time:
            raise ValueError("End time phải sau start time")
    
    def is_open(self) -> bool:
        """Kiểm tra phiên còn mở không."""
        return self.status == SessionStatus.OPEN
    
    def is_active(self) -> bool:
        """Kiểm tra phiên đang trong thời gian hoạt động."""
        now = datetime.now()
        return self.is_open() and self.start_time <= now <= self.end_time
    
    def is_late_window(self) -> bool:
        """Kiểm tra đang trong thời gian trễ cho phép."""
        now = datetime.now()
        if not self.is_open():
            return False
        # Sau end_time nhưng trong late_window
        from datetime import timedelta
        late_deadline = self.end_time + timedelta(minutes=self.late_window_minutes)
        return self.end_time < now <= late_deadline
    
    def open_session(self) -> None:
        """Mở phiên điểm danh."""
        self.status = SessionStatus.OPEN
    
    def close_session(self) -> None:
        """Đóng phiên điểm danh."""
        self.status = SessionStatus.CLOSED
    
    def auto_close_if_expired(self) -> bool:
        """
        Tự động đóng phiên nếu đã hết thời gian.
        
        Returns:
            True nếu đã đóng, False nếu không cần đóng
        """
        if self.is_open() and datetime.now() > self.end_time:
            self.close_session()
            return True
        return False
    
    def to_dict(self) -> dict:
        """Chuyển đổi thành dictionary."""
        return {
            "session_id": self.session_id,
            "class_id": self.class_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "method": self.method.value,
            "status": self.status.value,
            "attendance_link": self.attendance_link,
            "qr_window_minutes": self.qr_window_minutes,
            "late_window_minutes": self.late_window_minutes,
        }
