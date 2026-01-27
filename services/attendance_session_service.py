"""
Attendance Session Service - Session Management
===============================================

Service quản lý phiên điểm danh cho giáo viên.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict

from core.enums import AttendanceMethod, AttendanceStatus
from core.models import AttendanceSession
from core.models.attendance_session import SessionStatus
from data.repositories import AttendanceSessionRepository, AttendanceRecordRepository, ClassroomRepository
from .security_service import SecurityService
from .qr_service import QRService


class AttendanceSessionService:
    """
    Service quản lý phiên điểm danh.
    
    Example:
        >>> session_service = AttendanceSessionService(session_repo, record_repo, security, qr_service)
        >>> session = session_service.create_session("GV001", "CS101", ...)
    """
    
    def __init__(
        self,
        session_repo: AttendanceSessionRepository,
        record_repo: AttendanceRecordRepository,
        classroom_repo: ClassroomRepository,
        security_service: SecurityService,
        qr_service: QRService
    ):
        """
        Khởi tạo AttendanceSessionService.
        
        Args:
            session_repo: AttendanceSessionRepository instance
            record_repo: AttendanceRecordRepository instance
            classroom_repo: ClassroomRepository instance
            security_service: SecurityService instance
            qr_service: QRService instance
        """
        self.session_repo = session_repo
        self.record_repo = record_repo
        self.classroom_repo = classroom_repo
        self.security = security_service
        self.qr_service = qr_service
    
    def create_session(
        self,
        class_id: str,
        start_time: datetime,
        end_time: datetime,
        method: AttendanceMethod,
        qr_window_minutes: int = 1,
        late_window_minutes: int = 15
    ) -> Tuple[bool, str, Optional[AttendanceSession]]:
        """
        Tạo phiên điểm danh mới.
        
        Args:
            class_id: Mã lớp học
            start_time: Thời gian bắt đầu
            end_time: Thời gian kết thúc
            method: Phương thức điểm danh
            qr_window_minutes: Thời gian hiệu lực QR (phút)
            late_window_minutes: Thời gian cho phép trễ (phút)
            
        Returns:
            Tuple (success, message, session)
            
        Example:
            >>> success, msg, session = service.create_session(
            ...     "CS101",
            ...     datetime.now(),
            ...     datetime.now() + timedelta(hours=2),
            ...     AttendanceMethod.QR
            ... )
        """
        # Validate class exists
        classroom = self.classroom_repo.find_by_id(class_id)
        if not classroom:
            return False, "Lớp học không tồn tại", None
        
        # Validate time
        if end_time <= start_time:
            return False, "Thời gian kết thúc phải sau thời gian bắt đầu", None
        
        # Generate session ID
        session_id = f"SS{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Generate token/link if needed
        token = None
        attendance_link = None
        
        if method == AttendanceMethod.LINK_TOKEN:
            token = self.security.generate_token(16)
            attendance_link = f"/attendance/submit/{session_id}?token={token}"
        
        # Create session
        session = AttendanceSession(
            session_id=session_id,
            class_id=class_id,
            start_time=start_time,
            end_time=end_time,
            method=method,
            status=SessionStatus.OPEN,
            attendance_link=attendance_link,
            token=token,
            qr_window_minutes=qr_window_minutes,
            late_window_minutes=late_window_minutes
        )
        
        # Save to database
        created_session = self.session_repo.create(session)
        
        if created_session:
            return True, "Tạo phiên điểm danh thành công", created_session
        else:
            return False, "Không thể tạo phiên điểm danh", None
    
    def get_sessions_by_teacher(self, teacher_code: str, limit: int = 50) -> List[AttendanceSession]:
        """
        Lấy danh sách phiên điểm danh của giáo viên.
        
        Args:
            teacher_code: Mã giáo viên
            limit: Số lượng session tối đa
            
        Returns:
            List of AttendanceSession
        """
        # Get teacher's classes
        classes = self.classroom_repo.find_by_teacher(teacher_code)
        class_ids = [c.class_id for c in classes]
        
        # Get all sessions for these classes
        all_sessions = []
        for class_id in class_ids:
            sessions = self.session_repo.find_by_class(class_id)
            all_sessions.extend(sessions)
        
        # Sort by start_time descending and limit
        all_sessions.sort(key=lambda x: x.start_time, reverse=True)
        return all_sessions[:limit]
    
    def get_sessions_by_class(self, class_id: str) -> List[AttendanceSession]:
        """
        Lấy tất cả sessions của một lớp.
        
        Args:
            class_id: Mã lớp học
            
        Returns:
            List of AttendanceSession
        """
        return self.session_repo.find_by_class(class_id)
    
    def get_active_sessions(self, class_id: str) -> List[AttendanceSession]:
        """
        Lấy các session đang mở của một lớp.
        
        Args:
            class_id: Mã lớp học
            
        Returns:
            List of active AttendanceSession
        """
        return self.session_repo.find_active_by_class(class_id)
    
    def get_session_details(self, session_id: str) -> Optional[AttendanceSession]:
        """
        Lấy chi tiết một session.
        
        Args:
            session_id: Mã phiên điểm danh
            
        Returns:
            AttendanceSession or None
        """
        return self.session_repo.find_by_id(session_id)
    
    def close_session(self, session_id: str) -> Tuple[bool, str]:
        """
        Đóng phiên điểm danh.
        
        Args:
            session_id: Mã phiên điểm danh
            
        Returns:
            Tuple (success, message)
        """
        session = self.session_repo.find_by_id(session_id)
        
        if not session:
            return False, "Phiên điểm danh không tồn tại"
        
        if session.status == SessionStatus.CLOSED:
            return False, "Phiên đã được đóng từ trước"
        
        success = self.session_repo.close_session(session_id)
        
        if success:
            return True, "Đóng phiên thành công"
        else:
            return False, "Không thể đóng phiên"
    
    def auto_close_expired_sessions(self) -> int:
        """
        Tự động đóng các session đã hết hạn.
        
        Returns:
            Số lượng session đã đóng
        """
        # Get all open sessions
        all_sessions = self.session_repo.find_all()
        closed_count = 0
        
        for session in all_sessions:
            if session.auto_close_if_expired():
                self.session_repo.close_session(session.session_id)
                closed_count += 1
        
        return closed_count
    
    def get_session_report(self, session_id: str) -> Optional[Dict]:
        """
        Lấy báo cáo điểm danh của một session.
        
        Args:
            session_id: Mã phiên điểm danh
            
        Returns:
            Dictionary chứa thống kê hoặc None
            
        Example:
            >>> report = service.get_session_report("SS001")
            >>> print(report['total_students'])
            >>> print(report['present_count'])
        """
        session = self.session_repo.find_by_id(session_id)
        
        if not session:
            return None
        
        # Get attendance stats
        stats = self.record_repo.get_attendance_stats(session_id)
        
        # Get all students in class
        classroom = self.classroom_repo.find_by_id(session.class_id)
        total_students = len(classroom.student_codes) if classroom else 0
        
        return {
            "session_id": session_id,
            "class_id": session.class_id,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat(),
            "method": session.method.value,
            "status": session.status.value,
            "total_students": total_students,
            "present_count": stats.get("PRESENT", 0),
            "absent_count": stats.get("ABSENT", 0),
            "attendance_rate": (stats.get("PRESENT", 0) / total_students * 100) if total_students > 0 else 0
        }
    
    def generate_qr_for_session(self, session_id: str) -> Tuple[Optional[any], str]:
        """
        Tạo QR code cho phiên điểm danh.
        
        Args:
            session_id: Mã phiên điểm danh
            
        Returns:
            Tuple (QR image, token)
        """
        session = self.session_repo.find_by_id(session_id)
        
        if not session:
            return None, ""
        
        if session.method != AttendanceMethod.QR:
            return None, ""
        
        # Generate QR code
        qr_image, token = self.qr_service.generate_attendance_qr(
            session_id, 
            validity_seconds=session.qr_window_minutes * 60
        )
        
        return qr_image, token
