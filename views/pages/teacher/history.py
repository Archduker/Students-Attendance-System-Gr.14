"""
Attendance History Page
=======================

Page xem lịch sử điểm danh của giáo viên.
Match UI from Image 4.
"""

import customtkinter as ctk
from typing import Optional, List
from datetime import datetime
from core.models import Teacher
from controllers.teacher_controller import TeacherController

class HistoryPage(ctk.CTkFrame):
    """
    Page lịch sử điểm danh.
    Matches Image 4 UI.
    """
    
    def __init__(self, parent, teacher: Teacher, controller: TeacherController):
        super().__init__(parent, fg_color="transparent")
        self.pack(expand=True, fill="both")
        
        self.teacher = teacher
        self.controller = controller
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._setup_ui()
        self._load_real_data()

    def _load_real_data(self):
        """Fetch real sessions from DB"""
        try:
            # 1. Get classes map (id -> name)
            classes = self.controller.get_class_list(self.teacher)
            class_map = {c.class_id: c for c in classes}
            
            # 2. Get sessions
            sessions = self.controller.get_session_list(self.teacher)
            sessions.sort(key=lambda x: x.start_time, reverse=True)
            
            # Clear existing rows (if any)
            for widget in self.list_frame.winfo_children():
                widget.destroy()
            
            # Update footer count
            self.footer_label.configure(text=f"Showing {len(sessions)} records")
            
            # Add rows
            for s in sessions:
                c = class_map.get(s.class_id)
                course_name = c.class_name if c else s.class_id
                
                date_str = s.start_time.strftime("%d %b %Y")
                time_str = s.start_time.strftime("%I:%M %p")
                
                # Map status to UI badge
                # Session OPEN -> Active (Green), CLOSED -> Completed (Gray or Blue?)
                # But UI image uses PRESENT/ABSENT/LATE. 
                # Let's map OPEN -> ACTIVE (Green), CLOSED -> CLOSED (Gray)
                status = "ACTIVE" if s.is_open() else "CLOSED"
                
                self._add_row(self.list_frame, course_name, date_str, time_str, status)
                
        except Exception as e:
            print(f"Error loading history: {e}")

    def _setup_ui(self):
        # 1. Header
        self._create_header(self)
        
        # 2. History Table
        self._create_table_card(self)

    def _create_header(self, parent):
        header_frm = ctk.CTkFrame(parent, fg_color="transparent")
        header_frm.grid(row=0, column=0, sticky="ew", pady=(0, 20), padx=20)
        
        # Title
        title_area = ctk.CTkFrame(header_frm, fg_color="transparent")
        title_area.pack(side="left")
        
        ctk.CTkLabel(title_area, text="Attendance History", font=("Inter", 24, "bold"), text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(title_area, text="Review past sessions for your modules.", font=("Inter", 12), text_color="#94A3B8").pack(anchor="w")

        # Buttons
        btn_area = ctk.CTkFrame(header_frm, fg_color="transparent")
        btn_area.pack(side="right")
        
        # Filter
        ctk.CTkButton(
            btn_area, text="Filter", fg_color="transparent", border_width=1, border_color="#E2E8F0",
            text_color="#64748B", font=("Inter", 11, "bold"), width=80, height=32, corner_radius=8, hover_color="#F1F5F9"
        ).pack(side="left", padx=(0, 10))
        
        # Export Data
        ctk.CTkButton(
            btn_area, text="📥 Export Data", fg_color="#4F46E5", text_color="white", # Indigo-600
            font=("Inter", 11, "bold"), width=120, height=32, corner_radius=8, hover_color="#4338CA"
        ).pack(side="left")

    def _create_table_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        card.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # Card Controls
        controls = ctk.CTkFrame(card, fg_color="transparent")
        controls.pack(fill="x", padx=30, pady=25)
        
        # Search
        search_frm = ctk.CTkFrame(controls, fg_color="transparent", border_width=1, border_color="#E2E8F0", corner_radius=20, width=300, height=35)
        search_frm.pack(side="left")
        search_frm.pack_propagate(False)
        ctk.CTkLabel(search_frm, text="🔍", font=("Arial", 12), text_color="#94A3B8").pack(side="left", padx=(10, 5))
        ctk.CTkEntry(search_frm, placeholder_text="Search courses or dates...", border_width=0, fg_color="transparent", height=30, font=("Inter", 12)).pack(fill="x")
        
        # Semester Dropdown (Mock)
        ctk.CTkLabel(controls, text="📅 Semester 1, 2026", font=("Inter", 12), text_color="#64748B").pack(side="right")

        # Table Header
        headers = ctk.CTkFrame(card, fg_color="#F8FAFC", height=40, corner_radius=0)
        headers.pack(fill="x")
        
        # Modified columns for Teacher: Course, Date, Time, Status
        cols = [("COURSE NAME", 3), ("DATE", 2), ("TIME", 2), ("STATUS", 2), ("", 1)]
        headers.grid_columnconfigure(tuple(range(len(cols))), weight=1)
        
        for i, (col, weight) in enumerate(cols):
            headers.grid_columnconfigure(i, weight=weight)
            sticky = "w" if i < 3 else "" if i == 3 else "e"
            ctk.CTkLabel(headers, text=col, font=("Inter", 10, "bold"), text_color="#94A3B8").grid(row=0, column=i, sticky=sticky, padx=20, pady=10)

        # Table Rows
        self.list_frame = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Footer (Pagination)
        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.pack(fill="x", padx=30, pady=20)
        
        self.footer_label = ctk.CTkLabel(footer, text="Loading...", font=("Inter", 11), text_color="#94A3B8")
        self.footer_label.pack(side="left")
        
        p_frame = ctk.CTkFrame(footer, fg_color="transparent")
        p_frame.pack(side="right")
        
        ctk.CTkButton(p_frame, text="Previous", fg_color="transparent", border_width=1, border_color="#E2E8F0", text_color="#94A3B8", width=70, height=30).pack(side="left", padx=5)
        ctk.CTkButton(p_frame, text="Next", fg_color="#0F172A", text_color="white", width=70, height=30).pack(side="left")

    def _add_row(self, parent, course, date, time, status):
        row = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        row.pack(fill="x", pady=5)
        
        cols = [(3, "w"), (2, "w"), (2, "w"), (2, "c"), (1, "e")]
        for i, (weight, sticky) in enumerate(cols):
            row.grid_columnconfigure(i, weight=weight)
            
        # Course
        ctk.CTkLabel(row, text=course, font=("Inter", 12, "bold"), text_color="#0F172A").grid(row=0, column=0, sticky="w", padx=20)
        
        # Date
        ctk.CTkLabel(row, text=date, font=("Inter", 12), text_color="#64748B").grid(row=0, column=1, sticky="w", padx=20)
        
        # Time
        ctk.CTkLabel(row, text=time, font=("Inter", 12), text_color="#64748B").grid(row=0, column=2, sticky="w", padx=20)
        
        # Status Badge
        status_colors = {
            "ACTIVE": ("#DCFCE7", "#22C55E"), # Green
            "PRESENT": ("#DCFCE7", "#22C55E"), # Green (Legacy support)
            "CLOSED": ("#F1F5F9", "#64748B"),  # Gray
            "ABSENT": ("#FEE2E2", "#EF4444"),
        }
        bg, fg = status_colors.get(status, ("#F1F5F9", "#64748B"))
        
        badge = ctk.CTkLabel(
            row, text=status, font=("Inter", 10, "bold"), text_color=fg,
            fg_color=bg, corner_radius=5, width=80, height=24
        )
        badge.grid(row=0, column=3) 
        
        # Details Link
        link = ctk.CTkLabel(row, text="Details", font=("Inter", 12, "underline"), text_color="#3B82F6", cursor="hand2")
        link.grid(row=0, column=4, sticky="e", padx=20)
        
        # Separator
        ctk.CTkFrame(parent, height=1, fg_color="#F1F5F9").pack(fill="x", padx=10)
