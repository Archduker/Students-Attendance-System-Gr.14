"""
Attendance Repository - Attendance Data Access
===============================================

Repository cho AttendanceSession và AttendanceRecord.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from core.enums import AttendanceMethod, AttendanceStatus
from core.models import AttendanceSession, AttendanceRecord
from core.models.attendance_session import SessionStatus
from data.database import Database
from .base_repository import BaseRepository


class AttendanceSessionRepository(BaseRepository[AttendanceSession]):
    """
    Repository cho AttendanceSession entity.
    
    Example:
        >>> session_repo = AttendanceSessionRepository(db)
        >>> active_sessions = session_repo.find_active_by_class("CS101")
    """
    
    @property
    def table_name(self) -> str:
        return "attendance_sessions"
    
    def _row_to_entity(self, row) -> AttendanceSession:
        """Chuyển đổi row thành AttendanceSession."""
        return AttendanceSession(
            session_id=row["session_id"],
            class_id=row["class_id"],
            start_time=datetime.fromisoformat(row["start_time"]),
            end_time=datetime.fromisoformat(row["end_time"]),
            method=AttendanceMethod.from_string(row["attendance_method"]),
            status=SessionStatus(row["status"]),
            attendance_link=row["attendance_link"],
            token=row["token"],
            qr_window_minutes=row["qr_window_minutes"] if row["qr_window_minutes"] else 1,
            late_window_minutes=row["late_window_minutes"] if row["late_window_minutes"] else 15,
        )

    def _entity_to_dict(self, entity: AttendanceSession) -> Dict[str, Any]:
        """Chuyển đổi AttendanceSession thành dictionary."""
        return {
            "session_id": entity.session_id,
            "class_id": entity.class_id,
            "start_time": entity.start_time.isoformat(),
            "end_time": entity.end_time.isoformat(),
            "attendance_method": entity.method.value,
            "status": entity.status.value,
            "attendance_link": entity.attendance_link,
            "token": entity.token,
            "qr_window_minutes": entity.qr_window_minutes,
            "late_window_minutes": entity.late_window_minutes,
        }
    
    def find_by_class(self, class_id: str) -> List[AttendanceSession]:
        """Lấy tất cả sessions của một lớp."""
        query = f"SELECT * FROM {self.table_name} WHERE class_id = ? ORDER BY start_time DESC"
        rows = self.db.fetch_all(query, (class_id,))
        return [self._row_to_entity(row) for row in rows]
    
    def find_active_by_class(self, class_id: str) -> List[AttendanceSession]:
        """Lấy các session đang mở của một lớp."""
        query = f"SELECT * FROM {self.table_name} WHERE class_id = ? AND status = 'OPEN'"
        rows = self.db.fetch_all(query, (class_id,))
        return [self._row_to_entity(row) for row in rows]
    
    def find_by_token(self, token: str) -> Optional[AttendanceSession]:
        """Tìm session theo token."""
        query = f"SELECT * FROM {self.table_name} WHERE token = ?"
        row = self.db.fetch_one(query, (token,))
        return self._row_to_entity(row) if row else None
    
    def close_session(self, session_id: str) -> bool:
        """Đóng một session."""
        query = f"UPDATE {self.table_name} SET status = 'CLOSED' WHERE session_id = ?"
        cursor = self.db.execute(query, (session_id,))
        return cursor.rowcount > 0


class AttendanceRecordRepository(BaseRepository[AttendanceRecord]):
    """
    Repository cho AttendanceRecord entity.
    
    Example:
        >>> record_repo = AttendanceRecordRepository(db)
        >>> records = record_repo.find_by_session("SS001")
    """
    
    @property
    def table_name(self) -> str:
        return "attendance_records"
    
    def _row_to_entity(self, row) -> AttendanceRecord:
        """Chuyển đổi row thành AttendanceRecord."""
        attendance_time = None
        if row["attendance_time"]:
            attendance_time = datetime.fromisoformat(row["attendance_time"])
        
        return AttendanceRecord(
            record_id=row["record_id"],
            session_id=row["session_id"],
            student_code=row["student_code"],
            status=AttendanceStatus.from_string(row["status"]),
            attendance_time=attendance_time,
            remark=row["remark"],
        )
    
    def _entity_to_dict(self, entity: AttendanceRecord) -> Dict[str, Any]:
        """Chuyển đổi AttendanceRecord thành dictionary."""
        return {
            "record_id": entity.record_id,
            "session_id": entity.session_id,
            "student_code": entity.student_code,
            "status": entity.status.value,
            "attendance_time": entity.attendance_time.isoformat() if entity.attendance_time else None,
            "remark": entity.remark,
        }
    
    def find_by_session(self, session_id: str) -> List[AttendanceRecord]:
        """Lấy tất cả records của một session."""
        query = f"SELECT * FROM {self.table_name} WHERE session_id = ?"
        rows = self.db.fetch_all(query, (session_id,))
        return [self._row_to_entity(row) for row in rows]
    
    def find_by_student(self, student_code: str) -> List[AttendanceRecord]:
        """Lấy lịch sử điểm danh của sinh viên."""
        query = f"SELECT * FROM {self.table_name} WHERE student_code = ? ORDER BY attendance_time DESC"
        rows = self.db.fetch_all(query, (student_code,))
        return [self._row_to_entity(row) for row in rows]
    
    def find_by_session_and_student(
        self, 
        session_id: str, 
        student_code: str
    ) -> Optional[AttendanceRecord]:
        """Tìm record của sinh viên trong một session."""
        query = f"SELECT * FROM {self.table_name} WHERE session_id = ? AND student_code = ?"
        row = self.db.fetch_one(query, (session_id, student_code))
        return self._row_to_entity(row) if row else None
    
    def mark_attendance(
        self, 
        session_id: str, 
        student_code: str, 
        status: AttendanceStatus
    ) -> bool:
        """Đánh dấu điểm danh cho sinh viên."""
        existing = self.find_by_session_and_student(session_id, student_code)
        
        if existing:
            # Update existing record
            query = f"""
                UPDATE {self.table_name} 
                SET status = ?, attendance_time = ?
                WHERE session_id = ? AND student_code = ?
            """
            cursor = self.db.execute(
                query, 
                (status.value, datetime.now().isoformat(), session_id, student_code)
            )
            return cursor.rowcount > 0
        else:
            # Insert new record
            record = AttendanceRecord(
                record_id=f"REC{datetime.now().strftime('%Y%m%d%H%M%S')}",
                session_id=session_id,
                student_code=student_code,
                status=status,
                attendance_time=datetime.now() if status == AttendanceStatus.PRESENT else None,
            )
            self.create(record)
            return True
    
    def get_attendance_stats(self, session_id: str) -> Dict[str, int]:
        """Lấy thống kê điểm danh của một session."""
        query = f"""
            SELECT status, COUNT(*) as count
            FROM {self.table_name}
            WHERE session_id = ?
            GROUP BY status
        """
        rows = self.db.fetch_all(query, (session_id,))
        
        stats = {"PRESENT": 0, "ABSENT": 0}
        for row in rows:
            stats[row["status"]] = row["count"]
        
        return stats
