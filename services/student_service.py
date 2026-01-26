"""
Student Service - Student Business Logic
=========================================

Service xử lý các nghiệp vụ liên quan đến sinh viên:
- View dashboard statistics
- Submit attendance
- View attendance history
- Edit profile
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

from core.models import Student, AttendanceRecord, AttendanceSession
from core.enums import AttendanceStatus, AttendanceMethod
from core.exceptions import ValidationError, NotFoundError
from data.repositories import (
    UserRepository, 
    AttendanceRecordRepository,
    AttendanceSessionRepository,
    ClassRepository
)


class StudentService:
    """
    Service xử lý business logic cho Student.
    
    Example:
        >>> student_service = StudentService(user_repo, attendance_repo, ...)
        >>> stats = student_service.get_dashboard_stats("SV001")
        >>> student_service.submit_attendance("SV001", "SESSION123", "TOKEN456")
    """
    
    def __init__(
        self,
        user_repo: UserRepository,
        attendance_record_repo: AttendanceRecordRepository,
        attendance_session_repo: AttendanceSessionRepository,
        class_repo: ClassRepository
    ):
        """
        Khởi tạo StudentService.
        
        Args:
            user_repo: UserRepository instance
            attendance_record_repo: AttendanceRecordRepository instance
            attendance_session_repo: AttendanceSessionRepository instance
            class_repo: ClassRepository instance
        """
        self.user_repo = user_repo
        self.attendance_record_repo = attendance_record_repo
        self.attendance_session_repo = attendance_session_repo
        self.class_repo = class_repo
    
    def get_dashboard_stats(self, student_code: str) -> Dict[str, Any]:
        """
        Lấy thống kê cho dashboard của sinh viên.
        
        Args:
            student_code: Mã sinh viên
            
        Returns:
            Dict chứa các thống kê:
            - attendance_rate: Tỷ lệ điểm danh (%)
            - total_sessions: Tổng số buổi học
            - present_count: Số buổi có mặt
            - absent_count: Số buổi vắng
            - recent_attendance: 5 bản ghi điểm danh gần nhất
            
        Example:
            >>> stats = service.get_dashboard_stats("SV001")
            >>> print(f"Tỷ lệ điểm danh: {stats['attendance_rate']}%")
        """
        # Lấy tất cả attendance records của sinh viên
        records = self.attendance_record_repo.find_by_student(student_code)
        
        total_sessions = len(records)
        present_count = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)
        absent_count = total_sessions - present_count
        
        # Tính tỷ lệ điểm danh
        attendance_rate = (present_count / total_sessions * 100) if total_sessions > 0 else 0
        
        # Lấy 5 bản ghi gần nhất
        recent_records = sorted(
            records, 
            key=lambda r: r.attendance_time, 
            reverse=True
        )[:5]
        
        return {
            "attendance_rate": round(attendance_rate, 2),
            "total_sessions": total_sessions,
            "present_count": present_count,
            "absent_count": absent_count,
            "recent_attendance": [self._format_attendance_record(r) for r in recent_records]
        }
    
    def get_class_schedule(self, student_code: str) -> List[Dict[str, Any]]:
        """
        Lấy lịch học của sinh viên.
        
        Args:
            student_code: Mã sinh viên
            
        Returns:
            List các lớp học đang tham gia
        """
        classes = self.class_repo.get_classes_for_student(student_code)
        return [
            {
                "class_id": cls.class_id,
                "class_name": cls.class_name,
                "subject_code": cls.subject_code,
                "teacher_name": cls.teacher_name if hasattr(cls, 'teacher_name') else None
            }
            for cls in classes
        ]

    def get_todays_sessions(self, student_code: str) -> List[Dict[str, Any]]:
        """
        Lấy danh sách các session học trong ngày hôm nay.
        
        Args:
            student_code: Mã sinh viên
            
        Returns:
            List các session trong ngày
        """
        # Get classes for student
        classes = self.class_repo.get_classes_for_student(student_code)
        
        today = datetime.now().date()
        sessions_today = []
        
        for cls in classes:
            # Find active sessions for this class
            # Note: This finds all sessions, we filter for today
            all_sessions = self.attendance_session_repo.find_by_class(cls.class_id)
            
            for session in all_sessions:
                if session.start_time.date() == today:
                    sessions_today.append({
                        "session_id": session.session_id,
                        "class_id": cls.class_id,
                        "class_name": cls.class_name,
                        "subject_code": cls.subject_code,
                        "start_time": session.start_time.strftime("%H:%M"),
                        "end_time": session.end_time.strftime("%H:%M"),
                        "raw_start_time": session.start_time, # For sorting
                        "room": "Online" if session.method == AttendanceMethod.LINK_TOKEN else "TBA",
                        "status": session.status.value,
                        "method": session.method.value,
                        "is_active": session.status.value == "OPEN"
                    })
        
        # Sort by start time
        sessions_today.sort(key=lambda x: x["raw_start_time"])
        return sessions_today
    
    def submit_attendance(
        self, 
        student_code: str, 
        session_id: str,
        verification_data: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Submit điểm danh cho một phiên.
        
        Args:
            student_code: Mã sinh viên
            session_id: ID của session điểm danh
            verification_data: Token hoặc QR code data (tùy phương thức)
            
        Returns:
            Tuple (success, message)
            
        Raises:
            NotFoundError: Nếu session không tồn tại
            ValidationError: Nếu không trong thời gian cho phép
            
        Example:
            >>> success, msg = service.submit_attendance("SV001", "SESSION123", "TOKEN456")
            >>> if success:
            ...     print("Điểm danh thành công!")
        """
        # Kiểm tra session có tồn tại không
        session = self.attendance_session_repo.find_by_id(session_id)
        if not session:
            raise NotFoundError(f"Phiên điểm danh {session_id} không tồn tại")
        
        # Kiểm tra session có đang mở không
        if not (hasattr(session, 'status') and 
                (session.status == "OPEN" or 
                 (hasattr(session.status, 'value') and session.status.value == "OPEN"))):
            return False, "Phiên điểm danh đã đóng"
        
        # Kiểm tra thời gian
        current_time = datetime.now()
        if current_time < session.start_time:
            return False, "Phiên điểm danh chưa bắt đầu"
        
        if current_time > session.end_time:
            return False, "Phiên điểm danh đã kết thúc"
        
        # Kiểm tra đã điểm danh chưa
        existing_record = self.attendance_record_repo.find_by_session_and_student(
            session_id, student_code
        )
        if existing_record:
            return False, "Bạn đã điểm danh cho phiên này rồi"
        
        # Verify theo phương thức
        session_method = session.method if hasattr(session, 'method') else session.attendance_method
        if session_method == AttendanceMethod.LINK_TOKEN:
            if not verification_data or verification_data != session.token:
                return False, "Token không hợp lệ"
        elif session_method == AttendanceMethod.QR:
            # QR code verification (sẽ được xử lý bởi QR service)
            if not verification_data:
                return False, "Vui lòng quét mã QR"
        
        # Tạo attendance record
        record = AttendanceRecord(
            record_id=self._generate_record_id(),
            session_id=session_id,
            student_code=student_code,
            attendance_time=current_time,
            status=AttendanceStatus.PRESENT,
            remark=""
        )
        
        # Lưu vào database
        success = self.attendance_record_repo.create(record)
        
        if success:
            return True, "Điểm danh thành công!"
        else:
            return False, "Không thể lưu điểm danh, vui lòng thử lại"
    
    def get_attendance_history(
        self,
        student_code: str,
        search_query: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        class_id: Optional[str] = None,
        status: Optional[str] = None,
        sort_by: str = 'date',
        sort_order: str = 'desc'
    ) -> List[Dict[str, Any]]:
        """
        Lấy lịch sử điểm danh của sinh viên.
        
        Args:
            student_code: Mã sinh viên
            search_query: Từ khóa tìm kiếm (tên lớp hoặc ngày)
            start_date: Ngày bắt đầu (optional)
            end_date: Ngày kết thúc (optional)
            class_id: Lọc theo lớp học (optional)
            status: Lọc theo trạng thái (optional)
            sort_by: Sắp xếp theo 'date' hoặc 'class_name' (default: 'date')
            sort_order: 'asc' hoặc 'desc' (default: 'desc')
            
        Returns:
            List các bản ghi điểm danh
            
        Example:
            >>> history = service.get_attendance_history("SV001")
            >>> for record in history:
            ...     print(f"{record['date']}: {record['status']}")
        """
        # Lấy tất cả records
        records = self.attendance_record_repo.find_by_student(student_code)
        
        # Filter theo date range
        if start_date:
            records = [r for r in records if r.attendance_time >= start_date]
        if end_date:
            records = [r for r in records if r.attendance_time <= end_date]
        
        # Filter theo class_id
        if class_id:
            # Lấy sessions của class đó
            class_sessions = self.attendance_session_repo.find_by_class(class_id)
            session_ids = {s.session_id for s in class_sessions}
            records = [r for r in records if r.session_id in session_ids]
        
        # Filter theo status
        if status:
            records = [r for r in records if r.status.value == status]
        
        # Helper function to get class name safely for filtering
        def get_class_name_safe(record):
            session = self.attendance_session_repo.find_by_id(record.session_id)
            if not session: return ""
            cls = self.class_repo.find_by_id(session.class_id)
            return cls.class_name if cls else ""

        # Filter theo search query (Class Name or Date)
        if search_query:
            query = search_query.lower()
            filtered_records = []
            for r in records:
                class_name = get_class_name_safe(r).lower()
                date_str = r.attendance_time.strftime("%d %b %Y").lower()
                date_str_iso = r.attendance_time.strftime("%Y-%m-%d").lower()
                
                if query in class_name or query in date_str or query in date_str_iso:
                    filtered_records.append(r)
            records = filtered_records

        # Format và sort
        formatted_records = [self._format_attendance_record(r) for r in records]
        
        # Sort
        reverse = (sort_order.lower() == 'desc')
        if sort_by == 'class_name':
            formatted_records.sort(key=lambda x: (x['class_name'] or "").lower(), reverse=reverse)
        else: # date
            formatted_records.sort(key=lambda x: x['date'] + x['time'], reverse=reverse)
        
        return formatted_records
    
    def update_profile(
        self,
        student_code: str,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        class_name: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Cập nhật thông tin profile của sinh viên.
        
        Args:
            student_code: Mã sinh viên
            full_name: Họ tên mới (optional)
            email: Email mới (optional)
            class_name: Lớp mới (optional)
            
        Returns:
            Tuple (success, message)
        """
        # Tìm student
        student = self.user_repo.find_by_student_code(student_code)
        if not student:
            return False, "Không tìm thấy sinh viên"
        
        # Update fields
        update_data = {}
        if full_name:
            update_data['full_name'] = full_name
        if email:
            # Validate email
            if '@' not in email or '.' not in email:
                return False, "Email không hợp lệ"
            update_data['email'] = email
        if class_name:
            update_data['class_name'] = class_name
        
        # Update trong database
        success = self.user_repo.update_student_profile(student_code, update_data)
        
        if success:
            return True, "Cập nhật thông tin thành công"
        else:
            return False, "Không thể cập nhật thông tin"
    
    def get_student_info(self, student_code: str) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin chi tiết của sinh viên.
        
        Args:
            student_code: Mã sinh viên
            
        Returns:
            Dict chứa thông tin sinh viên hoặc None
        """
        student = self.user_repo.find_by_student_code(student_code)
        if not student:
            return None
        
        return {
            "student_code": student.student_code,
            "full_name": student.full_name,
            "email": student.email,
            "class_name": student.class_name if hasattr(student, 'class_name') else None,
            "username": student.username,
            "created_at": student.created_at.isoformat() if hasattr(student, 'created_at') else None
        }
    
    # Helper methods
    
    def _format_attendance_record(self, record: AttendanceRecord) -> Dict[str, Any]:
        """Format attendance record thành dictionary."""
        # Lấy session info
        session = self.attendance_session_repo.find_by_id(record.session_id)
        
        return {
            "record_id": record.record_id,
            "session_id": record.session_id,
            "class_id": session.class_id if session else None,
            "class_name": self._get_class_name(session.class_id) if session else None,
            "date": record.attendance_time.strftime("%Y-%m-%d"),
            "time": record.attendance_time.strftime("%H:%M:%S"),
            "status": record.status.value,
            "remark": record.remark or ""
        }
    
    def _get_class_name(self, class_id: str) -> Optional[str]:
        """Lấy tên lớp từ class_id."""
        cls = self.class_repo.find_by_id(class_id)
        return cls.class_name if cls else None
    
    def _generate_record_id(self) -> str:
        """Generate record ID."""
        # Simple implementation: timestamp-based
        return f"REC{datetime.now().strftime('%Y%m%d%H%M%S')}"
