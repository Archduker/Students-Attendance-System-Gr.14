"""
Teacher Dashboard - Dashboard Page for Teachers
================================================

Dashboard hiển thị thống kê và thông tin cho giáo viên.
"""

import customtkinter as ctk
from typing import Optional
from datetime import datetime

from core.models import Teacher
from controllers.teacher_controller import TeacherController


class TeacherDashboardPage(ctk.CTkFrame):
    """
    Dashboard page cho Teacher.
    
    Hiển thị:
    - Số lượng lớp phụ trách
    - Tổng số sinh viên
    - Tỷ lệ điểm danh trung bình
    - Danh sách session gần đây
    """
    
    def __init__(self, parent, teacher: Teacher, controller: TeacherController):
        """
        Khởi tạo Teacher Dashboard.
        
        Args:
            parent: Parent widget
            teacher: Teacher object
            controller: TeacherController instance
        """
        super().__init__(parent)
        
        self.teacher = teacher
        self.controller = controller
        
        self._setup_ui()
        self.load_data()
    
    def _setup_ui(self):
        """Setup giao diện."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            self,
            text=f"Dashboard - {self.teacher.full_name}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Stats Frame
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Stat Cards (placeholders)
        self.stat_cards = []
        stat_labels = [
            ("Lớp phụ trách", "total_classes"),
            ("Tổng sinh viên", "total_students"),
            ("Session đang mở", "active_sessions"),
            ("Tỷ lệ điểm danh TB", "avg_attendance_rate")
        ]
        
        for i, (label, key) in enumerate(stat_labels):
            card = self._create_stat_card(self.stats_frame, label, "0")
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            self.stat_cards.append((card, key))
        
        # Recent Sessions Frame
        sessions_label = ctk.CTkLabel(
            self,
            text="Phiên điểm danh gần đây",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        sessions_label.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Sessions Table (simplified scrollable frame)
        self.sessions_frame = ctk.CTkScrollableFrame(self, height=300)
        self.sessions_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.sessions_frame.grid_columnconfigure(0, weight=1)
        
        # Action Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            command=self.load_data,
            width=150
        )
        refresh_btn.pack(side="left", padx=10)
        
        new_session_btn = ctk.CTkButton(
            button_frame,
            text="➕ Tạo phiên mới",
            command=self.on_create_session,
            width=150
        )
        new_session_btn.pack(side="left", padx=10)
    
    def _create_stat_card(self, parent, label: str, value: str) -> ctk.CTkFrame:
        """
        Tạo một stat card.
        
        Args:
            parent: Parent widget
            label: Nhãn
            value: Giá trị
            
        Returns:
            CTkFrame chứa stat card
        """
        card = ctk.CTkFrame(parent)
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#2196F3"
        )
        value_label.pack(padx=20, pady=(20, 5))
        
        label_label = ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(size=12)
        )
        label_label.pack(padx=20, pady=(5, 20))
        
        card.value_label = value_label  # Store reference for updates
        
        return card
    
    def load_data(self):
        """Load dữ liệu dashboard."""
        try:
            # Get stats from controller
            stats = self.controller.get_dashboard_stats(self.teacher)
            
            # Update stat cards
            stat_map = {
                "total_classes": str(stats.get("total_classes", 0)),
                "total_students": str(stats.get("total_students", 0)),
                "active_sessions": str(stats.get("active_sessions", 0)),
                "avg_attendance_rate": f"{stats.get('avg_attendance_rate', 0):.1f}%"
            }
            
            for card, key in self.stat_cards:
                card.value_label.configure(text=stat_map.get(key, "0"))
            
            # Load recent sessions
            self._load_sessions()
            
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
    
    def _load_sessions(self):
        """Load danh sách sessions gần đây."""
        try:
            # Clear existing sessions
            for widget in self.sessions_frame.winfo_children():
                widget.destroy()
            
            # Get sessions from controller
            sessions = self.controller.get_session_list(self.teacher)
            
            if not sessions:
                no_data_label = ctk.CTkLabel(
                    self.sessions_frame,
                    text="Chưa có phiên điểm danh nào",
                    font=ctk.CTkFont(size=14)
                )
                no_data_label.pack(padx=20, pady=50)
                return
            
            # Display sessions
            for i, session in enumerate(sessions[:10]):  # Limit to 10
                session_card = self._create_session_card(self.sessions_frame, session)
                session_card.pack(fill="x", padx=10, pady=5)
        
        except Exception as e:
            print(f"Error loading sessions: {e}")
    
    def _create_session_card(self, parent, session) -> ctk.CTkFrame:
        """
        Tạo card hiển thị thông tin session.
        
        Args:
            parent: Parent widget
            session: AttendanceSession object
            
        Returns:
            CTkFrame chứa session info
        """
        card = ctk.CTkFrame(parent)
        card.grid_columnconfigure(0, weight=1)
        
        # Session info
        info_text = f"📚 {session.class_id} | {session.method.value} | "
        info_text += f"⏰ {session.start_time.strftime('%Y-%m-%d %H:%M')}"
        
        info_label = ctk.CTkLabel(
            card,
            text=info_text,
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        info_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        # Status badge
        status_color = "#4CAF50" if session.is_open() else "#9E9E9E"
        status_text = "OPEN" if session.is_open() else "CLOSED"
        
        status_label = ctk.CTkLabel(
            card,
            text=status_text,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=status_color
        )
        status_label.grid(row=0, column=1, padx=15, pady=10)
        
        return card
    
    def on_create_session(self):
        """
        Handler khi click nút Tạo phiên mới.
        Placeholder - sẽ mở dialog tạo session.
        """
        print("Create new session clicked")
        # TODO: Open CreateSessionDialog
