"""
Session Detail View - Chi tiết phiên điểm danh & Điểm danh thủ công
===================================================================

Page quản lý chi tiết một phiên điểm danh, danh sách sinh viên.
Match UI from Image 3.
"""

import customtkinter as ctk
from typing import Optional, List
from datetime import datetime

class SessionDetailPage(ctk.CTkFrame):
    """
    Page chi tiết session / manual entry.
    Matches Image 3 UI.
    """
    
    def __init__(self, parent, session_id=None):
        super().__init__(parent, fg_color="transparent")
        self.session_id = session_id
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self._setup_ui()
        # self.load_data()

    def _setup_ui(self):
        # 1. Header Area
        self._create_header(self)
        
        # 2. Main Card
        self._create_roster_card(self)

    def _create_header(self, parent):
        header_frm = ctk.CTkFrame(parent, fg_color="transparent")
        header_frm.grid(row=0, column=0, sticky="ew", pady=(0, 20), padx=20)
        
        # Title
        title_area = ctk.CTkFrame(header_frm, fg_color="transparent")
        title_area.pack(side="left")
        
        ctk.CTkLabel(title_area, text="Attendance Management", font=("Inter", 24, "bold"), text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(title_area, text="Review lab sessions or manually update student status for cohorts (~60 students)", font=("Inter", 12), text_color="#94A3B8").pack(anchor="w")

        # Buttons
        btn_area = ctk.CTkFrame(header_frm, fg_color="transparent")
        btn_area.pack(side="right")
        
        # HISTORY (Outline)
        ctk.CTkButton(
            btn_area, text="HISTORY", fg_color="transparent", border_width=1, border_color="#E2E8F0",
            text_color="#64748B", font=("Inter", 11, "bold"), width=80, height=32, corner_radius=16, hover_color="#F1F5F9"
        ).pack(side="left", padx=(0, 10))
        
        # MANUAL ENTRY (Dark/Active) - as per image 3
        ctk.CTkButton(
            btn_area, text="MANUAL ENTRY", fg_color="#0F172A", text_color="white",
            font=("Inter", 11, "bold"), width=120, height=32, corner_radius=16, hover_color="#1E293B"
        ).pack(side="left")

    def _create_roster_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        card.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # Card Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=25)
        
        info = ctk.CTkFrame(header, fg_color="transparent")
        info.pack(side="left")
        
        ctk.CTkLabel(info, text="Data Science Roster", font=("Inter", 18, "bold"), text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(info, text="Machine Learning - Cohort Average: 60 Scholars", font=("Inter", 12), text_color="#94A3B8").pack(anchor="w")
        
        # Controls (Search + Button)
        controls = ctk.CTkFrame(header, fg_color="transparent")
        controls.pack(side="right")
        
        search_frm = ctk.CTkFrame(controls, fg_color="transparent", border_width=1, border_color="#E2E8F0", corner_radius=20, width=200, height=35)
        search_frm.pack(side="left", padx=(0, 10))
        search_frm.pack_propagate(False)
        ctk.CTkLabel(search_frm, text="🔍", font=("Arial", 12), text_color="#94A3B8").pack(side="left", padx=(10, 5))
        ctk.CTkEntry(search_frm, placeholder_text="Search scholar...", border_width=0, fg_color="transparent", height=30, font=("Inter", 12)).pack(fill="x")
        
        ctk.CTkButton(
            controls, text="SET 100% PRESENT", fg_color="#0F172A", text_color="white",
            font=("Inter", 11, "bold"), width=150, height=35, corner_radius=8, hover_color="#1E293B"
        ).pack(side="left")

        # Student List
        self.list_frame = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Mock Students
        students = [
            ("Phan Nhat Tai", "S01", "09:12 AM", "present"),
            ("Hoang Thuy Linh", "S02", "09:13 AM", "present"),
            ("Dam Vinh Hung", "S03", "-", "absent"),
            ("Tran Thi Bich Phuong", "S04", "09:12 AM", "late"),
            ("Ho Ngoc Ha", "S05", "09:20 AM", "present"),
        ]
        
        for name, sid, ping, status in students:
            self._add_student_row(self.list_frame, name, sid, ping, status)

    def _add_student_row(self, parent, name, student_id, last_ping, initial_status):
        row = ctk.CTkFrame(parent, fg_color="transparent", height=70)
        row.pack(fill="x", pady=5)
        
        # 1. Avatar + Info
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", padx=10)
        
        # Avatar placeholder
        avatar = ctk.CTkLabel(
            info_frame, text="PT", width=40, height=40, corner_radius=20,
            fg_color="#F1F5F9", text_color="#64748B", font=("Inter", 12, "bold")
        )
        avatar.pack(side="left", padx=(0, 15))
        
        # Text
        text_f = ctk.CTkFrame(info_frame, fg_color="transparent")
        text_f.pack(side="left")
        
        ctk.CTkLabel(text_f, text=name, font=("Inter", 13, "bold"), text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(text_f, text=f"ID: {student_id} LAST PING: {last_ping}", font=("Inter", 10, "bold"), text_color="#94A3B8").pack(anchor="w")

        # 2. Status Buttons
        status_frame = ctk.CTkFrame(row, fg_color="transparent")
        status_frame.pack(side="right", padx=10)
        
        # Determine colors based on status
        present_fg = "#DCFCE7" if initial_status == "present" else "transparent"
        present_icon_c = "#22C55E" if initial_status == "present" else "#CBD5E1"
        
        late_fg = "#FEF3C7" if initial_status == "late" else "transparent"
        late_icon_c = "#D97706" if initial_status == "late" else "#CBD5E1"

        absent_fg = "#FEE2E2" if initial_status == "absent" else "transparent"
        absent_icon_c = "#EF4444" if initial_status == "absent" else "#CBD5E1"

        # Buttons (Circular Icon style)
        self._create_status_btn(status_frame, "✔️", present_fg, present_icon_c) # Present
        self._create_status_btn(status_frame, "📋", late_fg, late_icon_c)    # Late (Clipboard icon)
        self._create_status_btn(status_frame, "✖️", absent_fg, absent_icon_c)  # Absent
        
        # Separator
        ctk.CTkFrame(parent, height=1, fg_color="#F1F5F9").pack(fill="x", padx=10)

    def _create_status_btn(self, parent, icon, fg_color, text_color):
        btn = ctk.CTkButton(
            parent,
            text=icon,
            width=36,
            height=36,
            corner_radius=18,
            fg_color=fg_color,
            text_color=text_color,
            font=("Arial", 16),
            hover_color="#F1F5F9",
             # No command for UI demo
        )
        btn.pack(side="left", padx=5)
