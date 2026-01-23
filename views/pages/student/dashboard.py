"""
Student Dashboard Page - Main dashboard for students
====================================================

Dashboard hiển thị:
- Thống kê điểm danh (tỷ lệ, số buổi)
- Lịch học
- Bản ghi điểm danh gần đây
"""

import customtkinter as ctk
from typing import Optional, Dict, Any
from datetime import datetime

from views.styles.theme import COLORS, FONTS, SPACING, RADIUS
from controllers import StudentController


class StudentDashboard(ctk.CTkFrame):
    """
    Dashboard page cho Student.
    
    Hiển thị:
    - Attendance statistics
    - Class schedule  
    - Recent attendance records
    """
    
    def __init__(
        self, 
        parent, 
        controller: StudentController,
        student_code: str,
        **kwargs
    ):
        """
        Khởi tạo Student Dashboard.
        
        Args:
            parent: Parent widget
            controller: StudentController instance
            student_code: Mã sinh viên đang đăng nhập
        """
        super().__init__(parent, **kwargs)
        
        self.controller = controller
        self.student_code = student_code
        self.dashboard_data = None
        
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Thiết lập UI components."""
        self.configure(fg_color=COLORS["bg_secondary"])
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["lg"])
        
        # Header
        self._create_header(main_container)
        
        # Content area với scroll
        scroll_frame = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent"
        )
        scroll_frame.pack(fill="both", expand=True, pady=(SPACING["md"], 0))
        
        # Statistics cards
        self.stats_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.stats_container.pack(fill="x", pady=(0, SPACING["lg"]))
        
        # Schedule section
        self.schedule_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.schedule_container.pack(fill="x", pady=(0, SPACING["lg"]))
        
        # Recent attendance section
        self.recent_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.recent_container.pack(fill="both", expand=True)
    
    def _create_header(self, parent):
        """Tạo header section."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACING["lg"]))
        
        # Title
        title = ctk.CTkLabel(
            header,
            text="📊 Dashboard",
            font=(FONTS["family"], FONTS["size_3xl"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title.pack(side="left")
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            header,
            text="🔄 Làm mới",
            width=120,
            height=36,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self._load_data
        )
        refresh_btn.pack(side="right")
    
    def _create_stat_card(self, parent, title: str, value: str, icon: str, color: str):
        """Tạo một card thống kê."""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_primary"],
            corner_radius=RADIUS["lg"]
        )
        
        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=(FONTS["family"], FONTS["size_3xl"]),
            text_color=color
        )
        icon_label.pack(pady=(SPACING["md"], SPACING["sm"]))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=(FONTS["family"], FONTS["size_2xl"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        value_label.pack()
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS["text_secondary"]
        )
        title_label.pack(pady=(SPACING["xs"], SPACING["md"]))
        
        return card
    
    def _load_data(self):
        """Load dashboard data từ controller."""
        # Show loading
        self._show_loading()
        
        # Get data
        result = self.controller.handle_get_dashboard(self.student_code)
        
        if result["success"]:
            self.dashboard_data = result["data"]
            self._render_dashboard()
        else:
            self._show_error(result.get("error", "Không thể tải dữ liệu"))
    
    def _show_loading(self):
        """Hiển thị loading state."""
        # Clear containers
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        for widget in self.schedule_container.winfo_children():
            widget.destroy()
        for widget in self.recent_container.winfo_children():
            widget.destroy()
        
        # Show loading message
        loading = ctk.CTkLabel(
            self.stats_container,
            text="⏳ Đang tải dữ liệu...",
            font=(FONTS["family"], FONTS["size_lg"]),
            text_color=COLORS["text_secondary"]
        )
        loading.pack(pady=SPACING["xl"])
    
    def _render_dashboard(self):
        """Render dashboard với data đã load."""
        if not self.dashboard_data:
            return
        
        stats = self.dashboard_data.get("statistics", {})
        schedule = self.dashboard_data.get("schedule", [])
        
        # Clear containers
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        for widget in self.schedule_container.winfo_children():
            widget.destroy()
        for widget in self.recent_container.winfo_children():
            widget.destroy()
        
        # Render statistics cards
        self._render_statistics(stats)
        
        # Render schedule
        self._render_schedule(schedule)
        
        # Render recent attendance
        self._render_recent_attendance(stats.get("recent_attendance", []))
    
    def _render_statistics(self, stats: Dict[str, Any]):
        """Render statistics cards."""
        # Grid layout for cards
        cards_frame = ctk.CTkFrame(self.stats_container, fg_color="transparent")
        cards_frame.pack(fill="x")
        
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Attendance rate card
        rate_card = self._create_stat_card(
            cards_frame,
            "Tỷ lệ điểm danh",
            f"{stats.get('attendance_rate', 0)}%",
            "📈",
            COLORS["success"]
        )
        rate_card.grid(row=0, column=0, padx=SPACING["sm"], sticky="ew")
        
        # Total sessions card
        total_card = self._create_stat_card(
            cards_frame,
            "Tổng số buổi",
            str(stats.get('total_sessions', 0)),
            "📚",
            COLORS["primary"]
        )
        total_card.grid(row=0, column=1, padx=SPACING["sm"], sticky="ew")
        
        # Present count card
        present_card = self._create_stat_card(
            cards_frame,
            "Có mặt",
            str(stats.get('present_count', 0)),
            "✅",
            COLORS["success"]
        )
        present_card.grid(row=0, column=2, padx=SPACING["sm"], sticky="ew")
        
        # Absent count card
        absent_card = self._create_stat_card(
            cards_frame,
            "Vắng mặt",
            str(stats.get('absent_count', 0)),
            "❌",
            COLORS["error"]
        )
        absent_card.grid(row=0, column=3, padx=SPACING["sm"], sticky="ew")
    
    def _render_schedule(self, schedule: list):
        """Render class schedule."""
        # Section title
        title = ctk.CTkLabel(
            self.schedule_container,
            text="📅 Lịch học",
            font=(FONTS["family"], FONTS["size_xl"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]))
        
        if not schedule:
            no_data = ctk.CTkLabel(
                self.schedule_container,
                text="Không có lịch học",
                font=(FONTS["family"], FONTS["size_base"]),
                text_color=COLORS["text_secondary"]
            )
            no_data.pack(pady=SPACING["md"])
            return
        
        # Schedule cards
        for cls in schedule:
            self._create_schedule_card(self.schedule_container, cls)
    
    def _create_schedule_card(self, parent, class_data: Dict[str, Any]):
        """Tạo card cho một lớp học."""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_primary"],
            corner_radius=RADIUS["md"]
        )
        card.pack(fill="x", pady=SPACING["sm"])
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=SPACING["md"], pady=SPACING["md"])
        
        # Class name
        name = ctk.CTkLabel(
            content,
            text=class_data.get("class_name", "N/A"),
            font=(FONTS["family"], FONTS["size_lg"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        name.pack(anchor="w")
        
        # Subject code
        subject = ctk.CTkLabel(
            content,
            text=f"Mã môn: {class_data.get('subject_code', 'N/A')}",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS["text_secondary"]
        )
        subject.pack(anchor="w", pady=(SPACING["xs"], 0))
    
    def _render_recent_attendance(self, records: list):
        """Render recent attendance records."""
        # Section title
        title = ctk.CTkLabel(
            self.recent_container,
            text="🕒 Điểm danh gần đây",
            font=(FONTS["family"], FONTS["size_xl"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]))
        
        if not records:
            no_data = ctk.CTkLabel(
                self.recent_container,
                text="Chưa có bản ghi điểm danh",
                font=(FONTS["family"], FONTS["size_base"]),
                text_color=COLORS["text_secondary"]
            )
            no_data.pack(pady=SPACING["md"])
            return
        
        # Records list
        for record in records:
            self._create_attendance_record_row(self.recent_container, record)
    
    def _create_attendance_record_row(self, parent, record: Dict[str, Any]):
        """Tạo một row cho attendance record."""
        row = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_primary"],
            corner_radius=RADIUS["md"]
        )
        row.pack(fill="x", pady=SPACING["sm"])
        
        content = ctk.CTkFrame(row, fg_color="transparent")
        content.pack(fill="x", padx=SPACING["md"], pady=SPACING["sm"])
        
        # Date and class
        info_text = f"{record.get('date', 'N/A')} - {record.get('class_name', 'N/A')}"
        info = ctk.CTkLabel(
            content,
            text=info_text,
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_primary"]
        )
        info.pack(side="left")
        
        # Status badge
        status = record.get('status', 'ABSENT')
        status_color = COLORS["success"] if status == "PRESENT" else COLORS["error"]
        status_text = "✅ Có mặt" if status == "PRESENT" else "❌ Vắng"
        
        status_label = ctk.CTkLabel(
            content,
            text=status_text,
            font=(FONTS["family"], FONTS["size_sm"], FONTS["weight_bold"]),
            text_color=status_color
        )
        status_label.pack(side="right")
    
    def _show_error(self, message: str):
        """Hiển thị error message."""
        # Clear containers
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        
        error = ctk.CTkLabel(
            self.stats_container,
            text=f"❌ {message}",
            font=(FONTS["family"], FONTS["size_lg"]),
            text_color=COLORS["error"]
        )
        error.pack(pady=SPACING["xl"])
    
    def refresh(self):
        """Public method để refresh dashboard."""
        self._load_data()
