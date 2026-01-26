"""
Teacher Controller - Teacher Business Logic
===========================================

Controller xử lý logic cho Teacher module.
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

from core.enums import AttendanceMethod, AttendanceStatus
from core.models import Teacher
from services.attendance_session_service import AttendanceSessionService
from services.auth_service import AuthService
from data.repositories import ClassroomRepository, AttendanceRecordRepository


class TeacherController:
    """
    Controller xử lý business logic cho Teacher.
    
    Example:
        >>> controller = TeacherController(session_service, auth_service, classroom_repo)
        >>> stats = controller.get_dashboard_stats(teacher)
    """
    
    def __init__(
        self,
        session_service: AttendanceSessionService,
        auth_service: AuthService,
        classroom_repo: ClassroomRepository,
        record_repo: AttendanceRecordRepository
    ):
        """
        Khởi tạo TeacherController.
        
        Args:
            session_service: AttendanceSessionService instance
            auth_service: AuthService instance
            classroom_repo: ClassroomRepository instance
            record_repo: AttendanceRecordRepository instance
        """
        self.session_service = session_service
        self.auth_service = auth_service
        self.classroom_repo = classroom_repo
        self.record_repo = record_repo
    
    def get_dashboard_stats(self, teacher: Teacher) -> Dict:
        """
        Lấy thống kê cho Teacher Dashboard.
        
        Args:
            teacher: Teacher object
            
        Returns:
            Dictionary chứa thống kê
            
        Example:
            >>> stats = controller.get_dashboard_stats(teacher)
            >>> print(stats['total_classes'])
            >>> print(stats['active_sessions'])
        """
        # Get teacher's classes
        classes = self.classroom_repo.find_by_teacher(teacher.teacher_code)
        
        # Get recent sessions
        recent_sessions = self.session_service.get_sessions_by_teacher(teacher.teacher_code, limit=10)
        
        # Count active sessions
        active_sessions = sum(1 for s in recent_sessions if s.is_open())
        
        # Calculate average attendance rate
        total_rate = 0
        valid_sessions = 0
        
        for session in recent_sessions:
            report = self.session_service.get_session_report(session.session_id)
            if report and report['total_students'] > 0:
                total_rate += report['attendance_rate']
                valid_sessions += 1
        
        avg_attendance_rate = (total_rate / valid_sessions) if valid_sessions > 0 else 0
        
        # Total students across all classes
        total_students = sum(len(c.student_codes) for c in classes)
        
        return {
            "teacher_name": teacher.full_name,
            "teacher_code": teacher.teacher_code,
            "total_classes": len(classes),
            "total_students": total_students,
            "active_sessions": active_sessions,
            "recent_sessions_count": len(recent_sessions),
            "avg_attendance_rate": round(avg_attendance_rate, 2)
        }
    
    def create_new_session(
        self,
        teacher: Teacher,
        class_id: str,
        start_time: datetime,
        end_time: datetime,
        method: AttendanceMethod,
        qr_window_minutes: int = 1,
        late_window_minutes: int = 15
    ) -> Tuple[bool, str, Optional[any]]:
        """
        Tạo phiên điểm danh mới.
        
        Args:
            teacher: Teacher object
            class_id: Mã lớp học
            start_time: Thời gian bắt đầu
            end_time: Thời gian kết thúc
            method: Phương thức điểm danh
            qr_window_minutes: Thời gian hiệu lực QR
            late_window_minutes: Thời gian cho phép trễ
            
        Returns:
            Tuple (success, message, session)
        """
        # Verify teacher has access to this class
        classroom = self.classroom_repo.find_by_id(class_id)
        
        if not classroom:
            return False, "Lớp học không tồn tại", None
        
        if classroom.teacher_code != teacher.teacher_code:
            return False, "Bạn không được phân công giảng dạy lớp này", None
        
        # Create session
        success, message, session = self.session_service.create_session(
            class_id,
            start_time,
            end_time,
            method,
            qr_window_minutes,
            late_window_minutes
        )
        
        return success, message, session
    
    def get_class_list(self, teacher: Teacher) -> List:
        """
        Lấy danh sách lớp học của giáo viên.
        
        Args:
            teacher: Teacher object
            
        Returns:
            List of Classroom
        """
        return self.classroom_repo.find_by_teacher(teacher.teacher_code)
    
    def get_session_list(self, teacher: Teacher, class_id: Optional[str] = None) -> List:
        """
        Lấy danh sách session của giáo viên.
        
        Args:
            teacher: Teacher object
            class_id: Mã lớp (optional, để filter)
            
        Returns:
            List of AttendanceSession
        """
        if class_id:
            return self.session_service.get_sessions_by_class(class_id)
        else:
            return self.session_service.get_sessions_by_teacher(teacher.teacher_code)
    
    def close_session(self, teacher: Teacher, session_id: str) -> Tuple[bool, str]:
        """
        Đóng phiên điểm danh.
        
        Args:
            teacher: Teacher object
            session_id: Mã phiên
            
        Returns:
            Tuple (success, message)
        """
        # Verify teacher owns this session
        session = self.session_service.get_session_details(session_id)
        
        if not session:
            return False, "Phiên không tồn tại"
        
        classroom = self.classroom_repo.find_by_id(session.class_id)
        
        if not classroom or classroom.teacher_code != teacher.teacher_code:
            return False, "Bạn không có quyền đóng phiên này"
        
        return self.session_service.close_session(session_id)
    
    def get_session_report(self, teacher: Teacher, session_id: str) -> Optional[Dict]:
        """
        Lấy báo cáo điểm danh của session.
        
        Args:
            teacher: Teacher object
            session_id: Mã phiên
            
        Returns:
            Báo cáo hoặc None
        """
        # Verify access
        session = self.session_service.get_session_details(session_id)
        
        if not session:
            return None
        
        classroom = self.classroom_repo.find_by_id(session.class_id)
        
        if not classroom or classroom.teacher_code != teacher.teacher_code:
            return None
        
        return self.session_service.get_session_report(session_id)
    
    def mark_manual_attendance(
        self,
        teacher: Teacher,
        session_id: str,
        student_code: str,
        status: AttendanceStatus
    ) -> Tuple[bool, str]:
        """
        Điểm danh thủ công.
        
        Args:
            teacher: Teacher object
            session_id: Mã phiên
            student_code: Mã sinh viên
            status: Trạng thái điểm danh
            
        Returns:
            Tuple (success, message)
        """
        # Verify session
        session = self.session_service.get_session_details(session_id)
        
        if not session:
            return False, "Phiên không tồn tại"
        
        # Verify teacher access
        classroom = self.classroom_repo.find_by_id(session.class_id)
        
        if not classroom or classroom.teacher_code != teacher.teacher_code:
            return False, "Bạn không có quyền điểm danh phiên này"
        
        # Verify student in class
        if student_code not in classroom.student_codes:
            return False, "Sinh viên không thuộc lớp này"
        
        # Mark attendance
        success = self.record_repo.mark_attendance(session_id, student_code, status)
        
        if success:
            return True, "Điểm danh thành công"
        else:
            return False, "Không thể điểm danh"
    
    def export_class_report(
        self,
        teacher: Teacher,
        class_id: str,
        format: str = "csv"
    ) -> Tuple[bool, str, Optional[bytes]]:
        """
        Export báo cáo điểm danh của lớp.
        
        Args:
            teacher: Teacher object
            class_id: Mã lớp
            format: Định dạng (csv, xlsx)
            
        Returns:
            Tuple (success, message, file_data)
        """
        # TODO: Implement export functionality
        # For now, return placeholder
        return False, "Chức năng export đang được phát triển", None
    
    def handle_generate_qr_code(
        self,
        teacher: Teacher,
        class_id: str,
        session_id: Optional[str] = None
    ) -> Dict:
        """
        Generate QR code cho attendance session.
        
        Args:
            teacher: Teacher object
            class_id: Mã lớp học
            session_id: Session ID (optional, nếu muốn dùng session cụ thể)
            
        Returns:
            Dict với keys:
                - success: bool
                - qr_image: PIL Image (nếu success)
                - session_data: Dict (session info)
                - message: str (nếu error)
        """
        # Verify teacher has access to this class
        classroom = self.classroom_repo.find_by_id(class_id)
        
        if not classroom:
            return {
                "success": False,
                "message": "Lớp học không tồn tại"
            }
        
        if classroom.teacher_code != teacher.teacher_code:
            return {
                "success": False,
                "message": "Bạn không được phân công giảng dạy lớp này"
            }
        
        # Get or create active session
        session = None
        
        if session_id:
            # Use existing session
            session = self.session_service.get_session_details(session_id)
            if not session or session.class_id != class_id:
                return {
                    "success": False,
                    "message": "Session không hợp lệ"
                }
        else:
            # Try to find active session for this class
            sessions = self.session_service.get_sessions_by_class(class_id)
            active_sessions = [s for s in sessions if s.is_open()]
            
            if active_sessions:
                # Use first active session
                session = active_sessions[0]
            else:
                # Create new session with default settings
                from datetime import datetime, timedelta
                start_time = datetime.now()
                end_time = start_time + timedelta(hours=2)
                
                success, message, new_session = self.session_service.create_session(
                    class_id,
                    start_time,
                    end_time,
                    AttendanceMethod.QR,
                    qr_window_minutes=1,
                    late_window_minutes=15
                )
                
                if not success:
                    return {
                        "success": False,
                        "message": f"Không thể tạo session: {message}"
                    }
                
                session = new_session
        
        # Generate QR code
        try:
            from services.qr_service import QRService
            from services.security_service import SecurityService
            
            qr_service = QRService(SecurityService())
            
            # Generate QR with session data
            qr_image, token = qr_service.generate_attendance_qr(
                session.session_id,
                validity_seconds=60
            )
            
            # Prepare session data for UI
            session_data = {
                "session_id": session.session_id,
                "secret_code": token,  # Use the token from QR generation
                "status": session.status.value if hasattr(session.status, 'value') else str(session.status),
                "start_time": session.start_time,
                "end_time": session.end_time,
                "class_name": classroom.class_name
            }
            
            print(f"✅ Generated secret code: {token}")  # Debug
            
            return {
                "success": True,
                "qr_image": qr_image,
                "session_data": session_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi tạo QR code: {str(e)}"
            }

