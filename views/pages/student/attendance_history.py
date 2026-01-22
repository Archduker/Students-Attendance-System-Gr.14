"""
Attendance History Page - View attendance history
=================================================

Hiển thị:
- Lịch sử điểm danh với filters
- Tìm kiếm theo ngày, lớp
- Xuất báo cáo
"""

import customtkinter as ctk
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from tkinter import messagebox

from views.styles.theme import COLORS, FONTS, SPACING, RADIUS
from controllers import StudentController


class AttendanceHistoryPage(ctk.CTkFrame):
    """
    Page hiển thị lịch sử điểm danh của sinh viên.
    
    Features:
    - Filter theo ngày, lớp
    - Hiển thị danh sách records
    - Search và sort
    """
    
    def __init__(
        self,
        parent,
        controller: StudentController,
        student_code: str,
        **kwargs
    ):
        """
        Khởi tạo Attendance History Page.
        
        Args:
            parent: Parent widget
            controller: StudentController instance
            student_code: Mã sinh viên
        """
        super().__init__(parent, **kwargs)
        
        self.controller = controller
        self.student_code = student_code
        self.current_records = []
        
        self._setup_ui()
        self._load_history()
    
    def _setup_ui(self):
        """Thiết lập UI components."""
        self.configure(fg_color=COLORS["bg_secondary"])
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["lg"])
        
        # Header
        self._create_header(main_container)
        
        # Filters
        self._create_filters(main_container)
        
        # Records list với scroll
        self.records_scroll = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent"
        )
        self.records_scroll.pack(fill="both", expand=True, pady=(SPACING["md"], 0))
        
        # Records container
        self.records_container = ctk.CTkFrame(self.records_scroll, fg_color="transparent")
        self.records_container.pack(fill="both", expand=True)
    
    def _create_header(self, parent):
        """Tạo header section."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACING["lg"]))
        
        # Title
        title = ctk.CTkLabel(
            header,
            text="📜 Lịch sử điểm danh",
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
            command=self._load_history
        )
        refresh_btn.pack(side="right")
    
    def _create_filters(self, parent):
        """Tạo filters section."""
        filters_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_primary"],
            corner_radius=RADIUS["lg"]
        )
        filters_frame.pack(fill="x", pady=(0, SPACING["md"]))
        
        content = ctk.CTkFrame(filters_frame, fg_color="transparent")
        content.pack(fill="x", padx=SPACING["md"], pady=SPACING["md"])
        
        # Title
        title = ctk.CTkLabel(
            content,
            text="🔍 Bộ lọc",
            font=(FONTS["family"], FONTS["size_lg"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]))
        
        # Filter inputs
        inputs_frame = ctk.CTkFrame(content, fg_color="transparent")
        inputs_frame.pack(fill="x")
        
        # Start date
        date_frame = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        date_frame.pack(side="left", padx=(0, SPACING["md"]))
        
        start_label = ctk.CTkLabel(
            date_frame,
            text="Từ ngày:",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS["text_secondary"]
        )
        start_label.pack(anchor="w")
        
        self.start_date_entry = ctk.CTkEntry(
            date_frame,
            width=150,
            height=32,
            corner_radius=RADIUS["md"],
            placeholder_text="YYYY-MM-DD"
        )
        self.start_date_entry.pack()
        
        # End date
        end_frame = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        end_frame.pack(side="left", padx=(0, SPACING["md"]))
        
        end_label = ctk.CTkLabel(
            end_frame,
            text="Đến ngày:",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS["text_secondary"]
        )
        end_label.pack(anchor="w")
        
        self.end_date_entry = ctk.CTkEntry(
            end_frame,
            width=150,
            height=32,
            corner_radius=RADIUS["md"],
            placeholder_text="YYYY-MM-DD"
        )
        self.end_date_entry.pack()
        
        # Class ID
        class_frame = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        class_frame.pack(side="left", padx=(0, SPACING["md"]))
        
        class_label = ctk.CTkLabel(
            class_frame,
            text="Mã lớp:",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS["text_secondary"]
        )
        class_label.pack(anchor="w")
        
        self.class_entry = ctk.CTkEntry(
            class_frame,
            width=150,
            height=32,
            corner_radius=RADIUS["md"],
            placeholder_text="Nhập mã lớp..."
        )
        self.class_entry.pack()
        
        # Apply button
        apply_btn = ctk.CTkButton(
            inputs_frame,
            text="Áp dụng",
            width=100,
            height=32,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self._apply_filters
        )
        apply_btn.pack(side="left", pady=(14, 0))
        
        # Clear button
        clear_btn = ctk.CTkButton(
            inputs_frame,
            text="Xóa bộ lọc",
            width=100,
            height=32,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["secondary"],
            hover_color=COLORS["secondary_hover"],
            command=self._clear_filters
        )
        clear_btn.pack(side="left", padx=SPACING["sm"], pady=(14, 0))
    
    def _load_history(self, filters: Optional[Dict[str, Any]] = None):
        """Load attendance history."""
        # Show loading
        self._show_loading()
        
        # Get history
        result = self.controller.handle_get_attendance_history(
            self.student_code,
            filters
        )
        
        if result["success"]:
            self.current_records = result["data"]["records"]
            self._render_records()
        else:
            self._show_error(result.get("error", "Không thể tải lịch sử"))
    
    def _apply_filters(self):
        """Áp dụng filters."""
        filters = {}
        
        start_date = self.start_date_entry.get().strip()
        if start_date:
            filters["start_date"] = start_date
        
        end_date = self.end_date_entry.get().strip()
        if end_date:
            filters["end_date"] = end_date
        
        class_id = self.class_entry.get().strip()
        if class_id:
            filters["class_id"] = class_id
        
        self._load_history(filters)
    
    def _clear_filters(self):
        """Xóa tất cả filters."""
        self.start_date_entry.delete(0, "end")
        self.end_date_entry.delete(0, "end")
        self.class_entry.delete(0, "end")
        self._load_history()
    
    def _show_loading(self):
        """Hiển thị loading state."""
        # Clear records
        for widget in self.records_container.winfo_children():
            widget.destroy()
        
        loading = ctk.CTkLabel(
            self.records_container,
            text="⏳ Đang tải dữ liệu...",
            font=(FONTS["family"], FONTS["size_lg"]),
            text_color=COLORS["text_secondary"]
        )
        loading.pack(pady=SPACING["xl"])
    
    def _render_records(self):
        """Render danh sách records."""
        # Clear container
        for widget in self.records_container.winfo_children():
            widget.destroy()
        
        if not self.current_records:
            no_data = ctk.CTkLabel(
                self.records_container,
                text="📭 Không có bản ghi điểm danh",
                font=(FONTS["family"], FONTS["size_lg"]),
                text_color=COLORS["text_secondary"]
            )
            no_data.pack(pady=SPACING["xl"])
            return
        
        # Summary
        summary = ctk.CTkLabel(
            self.records_container,
            text=f"Tổng số: {len(self.current_records)} bản ghi",
            font=(FONTS["family"], FONTS["size_base"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        summary.pack(anchor="w", pady=(0, SPACING["md"]))
        
        # Table header
        self._create_table_header(self.records_container)
        
        # Records
        for record in self.current_records:
            self._create_record_row(self.records_container, record)
    
    def _create_table_header(self, parent):
        """Tạo header cho table."""
        header = ctk.CTkFrame(
            parent,
            fg_color=COLORS["primary"],
            corner_radius=RADIUS["md"]
        )
        header.pack(fill="x", pady=(0, SPACING["sm"]))
        
        content = ctk.CTkFrame(header, fg_color="transparent")
        content.pack(fill="x", padx=SPACING["md"], pady=SPACING["sm"])
        
        # Columns
        columns = [
            ("Ngày", 0.2),
            ("Giờ", 0.15),
            ("Lớp", 0.25),
            ("Mã lớp", 0.2),
            ("Trạng thái", 0.2)
        ]
        
        for col_name, width in columns:
            label = ctk.CTkLabel(
                content,
                text=col_name,
                font=(FONTS["family"], FONTS["size_base"], FONTS["weight_bold"]),
                text_color=COLORS["text_white"]
            )
            label.pack(side="left", fill="x", expand=True, padx=SPACING["xs"])
    
    def _create_record_row(self, parent, record: Dict[str, Any]):
        """Tạo một row cho record."""
        row = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_primary"],
            corner_radius=RADIUS["md"]
        )
        row.pack(fill="x", pady=SPACING["xs"])
        
        content = ctk.CTkFrame(row, fg_color="transparent")
        content.pack(fill="x", padx=SPACING["md"], pady=SPACING["sm"])
        
        # Date
        date = ctk.CTkLabel(
            content,
            text=record.get("date", "N/A"),
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS["text_primary"]
        )
        date.pack(side="left", fill="x", expand=True, padx=SPACING["xs"])
        
        # Time
        time = ctk.CTkLabel(
            content,
            text=record.get("time", "N/A"),
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS["text_primary"]
        )
        time.pack(side="left", fill="x", expand=True, padx=SPACING["xs"])
        
        # Class name
        class_name = ctk.CTkLabel(
            content,
            text=record.get("class_name", "N/A"),
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS["text_primary"]
        )
        class_name.pack(side="left", fill="x", expand=True, padx=SPACING["xs"])
        
        # Class ID
        class_id = ctk.CTkLabel(
            content,
            text=record.get("class_id", "N/A"),
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS["text_secondary"]
        )
        class_id.pack(side="left", fill="x", expand=True, padx=SPACING["xs"])
        
        # Status badge
        status = record.get("status", "ABSENT")
        if status == "PRESENT":
            status_text = "✅ Có mặt"
            status_color = COLORS["success"]
        else:
            status_text = "❌ Vắng"
            status_color = COLORS["error"]
        
        status_label = ctk.CTkLabel(
            content,
            text=status_text,
            font=(FONTS["family"], FONTS["size_sm"], FONTS["weight_bold"]),
            text_color=status_color
        )
        status_label.pack(side="left", fill="x", expand=True, padx=SPACING["xs"])
    
    def _show_error(self, message: str):
        """Hiển thị error message."""
        for widget in self.records_container.winfo_children():
            widget.destroy()
        
        error = ctk.CTkLabel(
            self.records_container,
            text=f"❌ {message}",
            font=(FONTS["family"], FONTS["size_lg"]),
            text_color=COLORS["error"]
        )
        error.pack(pady=SPACING["xl"])
    
    def refresh(self):
        """Refresh history."""
        self._load_history()
