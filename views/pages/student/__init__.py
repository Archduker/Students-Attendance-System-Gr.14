"""Student Pages - Dashboard, Attendance, Profile"""

from .dashboard import StudentDashboard
from .submit_attendance import SubmitAttendancePage
from .attendance_history import AttendanceHistoryPage
from .profile import ProfilePage
from views.layouts.student_layout import StudentLayout

__all__ = [
    "StudentDashboard",
    "SubmitAttendancePage",
    "AttendanceHistoryPage",
    "ProfilePage",
    "StudentLayout"
]
