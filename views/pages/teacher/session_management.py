"""
Session Management Page - Quản lý phiên điểm danh
=================================================

Page quản lý các phiên điểm danh của giáo viên.
"""

import customtkinter as ctk
from typing import Optional, List
from datetime import datetime

from core.models import Teacher
from core.models.attendance_session import AttendanceSession
from controllers.teacher_controller import TeacherController


class SessionManagementPage(ctk.CTkFrame):
    """
    Page quản lý sessions cho Teacher.
    
    Chức năng:
    - Hiển thị danh sách sessions
    - Filter theo lớp/trạng thái
    - Xem chi tiết, đóng session
    """
    
    def __init__(self, parent, teacher: Teacher, controller: TeacherController):
        """
        Khởi tạo Session Management Page.
        
        Args:
            parent: Parent widget
            teacher: Teacher object
            controller: TeacherController instance
        """
        super().__init__(parent)
        
        self.teacher = teacher
        self.controller = controller
        self.sessions: List[AttendanceSession] = []
        
        self._setup_ui()
        self.load_sessions()
    
    def _setup_ui(self):
        """Setup giao diện."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="Quản lý phiên điểm danh",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Filter Frame
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Class filter
        ctk.CTkLabel(filter_frame, text="Lọc theo lớp:").pack(side="left", padx=10)
        
        self.class_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Tất cả"],
            command=self.on_filter_change,
            width=200
        )
        self.class_filter.pack(side="left", padx=10)
        
        # Status filter
        ctk.CTkLabel(filter_frame, text="Trạng thái:").pack(side="left", padx=10)
        
        self.status_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Tất cả", "OPEN", "CLOSED"],
            command=self.on_filter_change,
            width=150
        )
        self.status_filter.pack(side="left", padx=10)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            filter_frame,
            text="🔄 Refresh",
            command=self.load_sessions,
            width=100
        )
        refresh_btn.pack(side="right", padx=10)
        
        # Sessions List Frame
        self.sessions_frame = ctk.CTkScrollableFrame(self, height=400)
        self.sessions_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.sessions_frame.grid_columnconfigure(0, weight=1)
        
        # Action Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        
        new_session_btn = ctk.CTkButton(
            button_frame,
            text="➕ Tạo phiên mới",
            command=self.on_create_session,
            width=150
        )
        new_session_btn.pack(side="left", padx=10)
    
    def load_sessions(self):
        """Load danh sách sessions."""
        try:
            # Get sessions from controller
            self.sessions = self.controller.get_session_list(self.teacher)
            
            # Update class filter options
            classes = list(set(s.class_id for s in self.sessions))
            self.class_filter.configure(values=["Tất cả"] + classes)
            
            # Apply current filters
            self.apply_filters()
            
        except Exception as e:
            print(f"Error loading sessions: {e}")
            self._show_error("Không thể tải danh sách phiên điểm danh")
    
    def apply_filters(self):
        """Áp dụng bộ lọc và hiển thị sessions."""
        # Clear current display
        for widget in self.sessions_frame.winfo_children():
            widget.destroy()
        
        # Get filter values
        class_filter = self.class_filter.get()
        status_filter = self.status_filter.get()
        
        # Filter sessions
        filtered_sessions = self.sessions
        
        if class_filter != "Tất cả":
            filtered_sessions = [s for s in filtered_sessions if s.class_id == class_filter]
        
        if status_filter != "Tất cả":
            filtered_sessions = [s for s in filtered_sessions if s.status.value == status_filter]
        
        # Display filtered sessions
        if not filtered_sessions:
            no_data_label = ctk.CTkLabel(
                self.sessions_frame,
                text="Không có phiên nào phù hợp",
                font=ctk.CTkFont(size=14)
            )
            no_data_label.pack(padx=20, pady=50)
            return
        
        # Create session cards
        for session in filtered_sessions:
            card = self._create_session_card(self.sessions_frame, session)
            card.pack(fill="x", padx=10, pady=5)
    
    def _create_session_card(self, parent, session: AttendanceSession) -> ctk.CTkFrame:
        """
        Tạo card hiển thị session.
        
        Args:
            parent: Parent widget
            session: AttendanceSession object
            
        Returns:
            CTkFrame chứa session info
        """
        card = ctk.CTkFrame(parent)
        card.grid_columnconfigure(0, weight=1)
        
        # Row 1: Session Info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Session ID and Class
        title_text = f"📝 {session.session_id} | 📚 {session.class_id}"
        title_label = ctk.CTkLabel(
            info_frame,
            text=title_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Time info
        time_text = f"⏰ {session.start_time.strftime('%Y-%m-%d %H:%M')} - {session.end_time.strftime('%H:%M')}"
        time_label = ctk.CTkLabel(
            info_frame,
            text=time_text,
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        time_label.grid(row=1, column=0, sticky="w", pady=5)
        
        # Method and Status
        method_text = f"🔧 {session.method.value}"
        status_color = "#4CAF50" if session.is_open() else "#9E9E9E"
        status_text = "🟢 OPEN" if session.is_open() else "⚫ CLOSED"
        
        details_text = f"{method_text} | {status_text}"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=ctk.CTkFont(size=12),
            anchor="w",
            text_color=status_color
        )
        details_label.grid(row=2, column=0, sticky="w")
        
        # Row 2: Action Buttons
        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.grid(row=1, column=0, padx=15, pady=(5, 10), sticky="ew")
        
        # View Details button
        view_btn = ctk.CTkButton(
            action_frame,
            text="👁️ Xem chi tiết",
            command=lambda: self.on_view_details(session),
            width=120,
            height=30
        )
        view_btn.pack(side="left", padx=5)
        
        # Close Session button (only if open)
        if session.is_open():
            close_btn = ctk.CTkButton(
                action_frame,
                text="🔒 Đóng phiên",
                command=lambda: self.on_close_session(session),
                width=120,
                height=30,
                fg_color="#FF5722"
            )
            close_btn.pack(side="left", padx=5)
        
        return card
    
    def on_filter_change(self, value):
        """Handler khi thay đổi filter."""
        self.apply_filters()
    
    def on_create_session(self):
        """Handler tạo phiên mới."""
        print("Create new session clicked")
        # TODO: Open CreateSessionDialog
    
    def on_view_details(self, session: AttendanceSession):
        """
        Handler xem chi tiết session.
        
        Args:
            session: AttendanceSession object
        """
        print(f"View details for session: {session.session_id}")
        # TODO: Open session details view or modal
    
    def on_close_session(self, session: AttendanceSession):
        """
        Handler đóng session.
        
        Args:
            session: AttendanceSession object
        """
        # Confirm dialog
        confirm = self._show_confirm(
            f"Bạn có chắc muốn đóng phiên {session.session_id}?"
        )
        
        if confirm:
            success, message = self.controller.close_session(self.teacher, session.session_id)
            
            if success:
                self._show_info("Đóng phiên thành công")
                self.load_sessions()
            else:
                self._show_error(message)
    
    def _show_error(self, message: str):
        """Hiển thị error message."""
        print(f"ERROR: {message}")
        # TODO: Implement proper error dialog
    
    def _show_info(self, message: str):
        """Hiển thị info message."""
        print(f"INFO: {message}")
        # TODO: Implement proper info dialog
    
    def _show_confirm(self, message: str) -> bool:
        """
        Hiển thị confirm dialog.
        
        Args:
            message: Confirmation message
            
        Returns:
            True if confirmed
        """
        print(f"CONFIRM: {message}")
        # TODO: Implement proper confirm dialog
        return True  # Placeholder
