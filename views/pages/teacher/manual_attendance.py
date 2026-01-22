"""
Manual Attendance Page - Điểm danh thủ công
===========================================

Page cho phép giáo viên điểm danh thủ công cho sinh viên.
"""

import customtkinter as ctk
from typing import Optional, Dict
from datetime import datetime

from core.models import Teacher, AttendanceSession
from core.enums import AttendanceStatus
from controllers.teacher_controller import TeacherController


class ManualAttendancePage(ctk.CTkFrame):
    """
    Page điểm danh thủ công.
    
    Chức năng:
    - Hiển thị danh sách sinh viên trong lớp
    - Cho phép đánh dấu Present/Absent
    - Lưu kết quả điểm danh
    """
    
    def __init__(
        self,
        parent,
        teacher: Teacher,
        session: AttendanceSession,
        controller: TeacherController
    ):
        """
        Khởi tạo Manual Attendance Page.
        
        Args:
            parent: Parent widget
            teacher: Teacher object
            session: AttendanceSession object
            controller: TeacherController instance
        """
        super().__init__(parent)
        
        self.teacher = teacher
        self.session = session
        self.controller = controller
        self.attendance_status: Dict[str, AttendanceStatus] = {}
        
        self._setup_ui()
        self._load_students()
    
    def _setup_ui(self):
        """Setup giao diện."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header
        header_text = f"Điểm danh thủ công - {self.session.class_id}"
        header = ctk.CTkLabel(
            self,
            text=header_text,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Session Info
        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        info_text = f"📝 Session: {self.session.session_id} | "
        info_text += f"⏰ {self.session.start_time.strftime('%Y-%m-%d %H:%M')}"
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12)
        )
        info_label.pack(padx=15, pady=10)
        
        # Students List Frame
        self.students_frame = ctk.CTkScrollableFrame(self, height=400)
        self.students_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.students_frame.grid_columnconfigure(0, weight=1)
        
        # Action Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        
        mark_all_present_btn = ctk.CTkButton(
            button_frame,
            text="✓ Đánh dấu tất cả có mặt",
            command=self.on_mark_all_present,
            width=180
        )
        mark_all_present_btn.pack(side="left", padx=10)
        
        mark_all_absent_btn = ctk.CTkButton(
            button_frame,
            text="✗ Đánh dấu tất cả vắng",
            command=self.on_mark_all_absent,
            width=180,
            fg_color="#FF5722"
        )
        mark_all_absent_btn.pack(side="left", padx=10)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Lưu điểm danh",
            command=self.on_save,
            width=150,
            fg_color="#4CAF50"
        )
        save_btn.pack(side="right", padx=10)
    
    def _load_students(self):
        """Load danh sách sinh viên."""
        try:
            # Get classroom
            from data.repositories import ClassroomRepository
            from data.database import Database
            
            # TODO: Get classroom from controller
            # For now, create a placeholder
            # classroom = self.controller.get_classroom(self.session.class_id)
            
            # Placeholder: Assume we have student codes
            student_codes = ["SV001", "SV002", "SV003"]  # Placeholder
            
            # Load existing attendance records
            from data.repositories import AttendanceRecordRepository
            record_repo = AttendanceRecordRepository(Database())
            
            existing_records = record_repo.find_by_session(self.session.session_id)
            existing_map = {r.student_code: r.status for r in existing_records}
            
            # Create student cards
            for student_code in student_codes:
                # Get existing status or default to ABSENT
                current_status = existing_map.get(student_code, AttendanceStatus.ABSENT)
                self.attendance_status[student_code] = current_status
                
                card = self._create_student_card(self.students_frame, student_code, current_status)
                card.pack(fill="x", padx=10, pady=5)
        
        except Exception as e:
            print(f"Error loading students: {e}")
            error_label = ctk.CTkLabel(
                self.students_frame,
                text="Không thể tải danh sách sinh viên",
                text_color="#F44336"
            )
            error_label.pack(padx=20, pady=50)
    
    def _create_student_card(
        self,
        parent,
        student_code: str,
        current_status: AttendanceStatus
    ) -> ctk.CTkFrame:
        """
        Tạo card cho sinh viên.
        
        Args:
            parent: Parent widget
            student_code: Mã sinh viên
            current_status: Trạng thái điểm danh hiện tại
            
        Returns:
            CTkFrame chứa student info
        """
        card = ctk.CTkFrame(parent)
        card.grid_columnconfigure(0, weight=1)
        
        # Student info
        info_label = ctk.CTkLabel(
            card,
            text=f"👤 {student_code}",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        info_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        # Status buttons frame
        status_frame = ctk.CTkFrame(card, fg_color="transparent")
        status_frame.grid(row=0, column=1, padx=15, pady=15)
        
        # Present button
        present_btn = ctk.CTkButton(
            status_frame,
            text="✓ Có mặt",
            command=lambda: self.on_mark_status(student_code, AttendanceStatus.PRESENT, card),
            width=100,
            height=35,
            fg_color="#4CAF50" if current_status == AttendanceStatus.PRESENT else "#757575"
        )
        present_btn.pack(side="left", padx=5)
        
        # Absent button
        absent_btn = ctk.CTkButton(
            status_frame,
            text="✗ Vắng",
            command=lambda: self.on_mark_status(student_code, AttendanceStatus.ABSENT, card),
            width=100,
            height=35,
            fg_color="#F44336" if current_status == AttendanceStatus.ABSENT else "#757575"
        )
        absent_btn.pack(side="left", padx=5)
        
        # Store references for updating
        card.present_btn = present_btn
        card.absent_btn = absent_btn
        card.student_code = student_code
        
        return card
    
    def on_mark_status(self, student_code: str, status: AttendanceStatus, card: ctk.CTkFrame):
        """
        Handler đánh dấu status cho sinh viên.
        
        Args:
            student_code: Mã sinh viên
            status: Status mới
            card: Card widget của sinh viên
        """
        # Update status
        self.attendance_status[student_code] = status
        
        # Update button colors
        if status == AttendanceStatus.PRESENT:
            card.present_btn.configure(fg_color="#4CAF50")
            card.absent_btn.configure(fg_color="#757575")
        else:
            card.present_btn.configure(fg_color="#757575")
            card.absent_btn.configure(fg_color="#F44336")
        
        print(f"Marked {student_code} as {status.value}")
    
    def on_mark_all_present(self):
        """Handler đánh dấu tất cả có mặt."""
        for widget in self.students_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and hasattr(widget, 'student_code'):
                self.on_mark_status(
                    widget.student_code,
                    AttendanceStatus.PRESENT,
                    widget
                )
    
    def on_mark_all_absent(self):
        """Handler đánh dấu tất cả vắng."""
        for widget in self.students_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and hasattr(widget, 'student_code'):
                self.on_mark_status(
                    widget.student_code,
                    AttendanceStatus.ABSENT,
                    widget
                )
    
    def on_save(self):
        """Handler lưu điểm danh."""
        try:
            success_count = 0
            error_count = 0
            
            for student_code, status in self.attendance_status.items():
                success, message = self.controller.mark_manual_attendance(
                    self.teacher,
                    self.session.session_id,
                    student_code,
                    status
                )
                
                if success:
                    success_count += 1
                else:
                    error_count += 1
                    print(f"Error marking {student_code}: {message}")
            
            # Show result
            result_text = f"Đã lưu {success_count} điểm danh"
            if error_count > 0:
                result_text += f" ({error_count} lỗi)"
            
            print(result_text)
            # TODO: Show dialog or toast
            
        except Exception as e:
            print(f"Error saving attendance: {e}")
            # TODO: Show error dialog
