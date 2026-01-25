"""
Session Management Page - Quản lý phiên điểm danh
=================================================

Page quản lý các phiên điểm danh của giáo viên.
Match UI from Image 2.
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
    Matches Image 2 UI.
    """
    
    def __init__(self, parent, teacher: Teacher, controller: TeacherController):
        super().__init__(parent, fg_color="transparent")
        
        self.teacher = teacher
        self.controller = controller
        self.sessions: List[AttendanceSession] = []
        
        # Grid layout: Main Content (Left) + Quick Actions (Right)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._setup_ui()
        # self.load_sessions() # Call to load real data

    def _setup_ui(self):
        # --- Left Column: Header + Session List ---
        self.left_col = ctk.CTkFrame(self, fg_color="transparent")
        self.left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        self._create_header(self.left_col)
        self._create_session_list(self.left_col)
        
        # --- Right Column: Quick Actions ---
        self.right_col = ctk.CTkFrame(self, fg_color="transparent")
        self.right_col.grid(row=0, column=1, sticky="n", pady=0)
        
        self._create_quick_actions(self.right_col)

    def _create_header(self, parent):
        # Header Container
        header_frm = ctk.CTkFrame(parent, fg_color="transparent")
        header_frm.pack(fill="x", pady=(0, 30))
        
        # Title & Subtitle
        title_area = ctk.CTkFrame(header_frm, fg_color="transparent")
        title_area.pack(side="left")
        
        ctk.CTkLabel(
            title_area, 
            text="Attendance Management", 
            font=("Inter", 24, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_area,
            text="Review lab sessions or manually update student status for cohorts (~60 students)",
            font=("Inter", 12),
            text_color="#94A3B8"
        ).pack(anchor="w")

        # Buttons (History, Manual Entry)
        btn_area = ctk.CTkFrame(header_frm, fg_color="transparent")
        btn_area.pack(side="right")
        
        # History Button (Dark)
        ctk.CTkButton(
            btn_area,
            text="HISTORY",
            fg_color="black",
            text_color="white",
            font=("Inter", 11, "bold"),
            width=80,
            height=32,
            corner_radius=16,
            hover_color="#333"
        ).pack(side="left", padx=(0, 10))
        
        # Manual Entry Button (Outline)
        ctk.CTkButton(
            btn_area,
            text="MANUAL ENTRY",
            fg_color="transparent",
            border_width=1,
            border_color="#E2E8F0",
            text_color="#64748B",
            font=("Inter", 11, "bold"),
            width=100,
            height=32,
            corner_radius=16,
            hover_color="#F1F5F9"
        ).pack(side="left")

    def _create_session_list(self, parent):
        # Container Card
        container = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        container.pack(fill="both", expand=True)
        
        # Top Bar (Title + Search)
        top_bar = ctk.CTkFrame(container, fg_color="transparent")
        top_bar.pack(fill="x", padx=30, pady=25)
        
        ctk.CTkLabel(
            top_bar,
            text="RECENT SESSIONS",
            font=("Inter", 12, "bold"),
            text_color="#94A3B8"
        ).pack(side="left")
        
        # Search Box
        search_frm = ctk.CTkFrame(top_bar, fg_color="transparent", border_width=1, border_color="#E2E8F0", corner_radius=20, width=200, height=35)
        search_frm.pack(side="right")
        search_frm.pack_propagate(False)
        
        ctk.CTkLabel(search_frm, text="🔍", font=("Arial", 12), text_color="#94A3B8").pack(side="left", padx=(10, 5))
        ctk.CTkEntry(search_frm, placeholder_text="Find session", border_width=0, fg_color="transparent", height=30, font=("Inter", 12)).pack(fill="x", padx=5)

        # Column Headers
        headers = ctk.CTkFrame(container, fg_color="#F8FAFC", height=40, corner_radius=0)
        headers.pack(fill="x", padx=1) # Thin border effect if bg is different
        
        # Use grid for columns
        headers.grid_columnconfigure(0, weight=2) # Course
        headers.grid_columnconfigure(1, weight=1) # Date
        headers.grid_columnconfigure(2, weight=1) # Headcount
        
        ctk.CTkLabel(headers, text="COURSE", font=("Inter", 10, "bold"), text_color="#94A3B8").grid(row=0, column=0, sticky="w", padx=30, pady=10)
        ctk.CTkLabel(headers, text="DATE", font=("Inter", 10, "bold"), text_color="#94A3B8").grid(row=0, column=1, sticky="w", padx=10)
        ctk.CTkLabel(headers, text="HEADCOUNT", font=("Inter", 10, "bold"), text_color="#94A3B8").grid(row=0, column=2, sticky="e", padx=30)
        
        # List Items Area (Scrollable if needed, using frame for now)
        list_area = ctk.CTkScrollableFrame(container, fg_color="transparent")
        list_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mock Data Items
        self._add_session_item(list_area, "Machine Learning", "CLOSED", "Jan 5th, 2026", 56, 60)
        self._add_session_item(list_area, "Big Data Analysis", "ACTIVE", "Jan 5th, 2026", 52, 60)
        # Add more if needed

    def _add_session_item(self, parent, course_name, status, date_str, current, max_students):
        item = ctk.CTkFrame(parent, fg_color="transparent", height=70)
        item.pack(fill="x", pady=5)
        
        item.grid_columnconfigure(0, weight=2)
        item.grid_columnconfigure(1, weight=1)
        item.grid_columnconfigure(2, weight=1)
        
        # 1. Course Info
        course_frame = ctk.CTkFrame(item, fg_color="transparent")
        course_frame.grid(row=0, column=0, sticky="w", padx=20)
        
        ctk.CTkLabel(course_frame, text=course_name, font=("Inter", 13, "bold"), text_color="#0F172A").pack(anchor="w")
        
        status_color = "#94A3B8" if status == "CLOSED" else "#22C55E" # Green for Active
        ctk.CTkLabel(course_frame, text=status, font=("Inter", 10, "bold"), text_color=status_color).pack(anchor="w")

        # 2. Date
        ctk.CTkLabel(item, text=date_str, font=("Inter", 12, "bold"), text_color="#334155").grid(row=0, column=1, sticky="w", padx=10)
        
        # 3. Headcount (Progress bar style)
        count_frame = ctk.CTkFrame(item, fg_color="transparent")
        count_frame.grid(row=0, column=2, sticky="e", padx=20)
        
        # Text 56/60
        ctk.CTkLabel(count_frame, text=f"{current}/{max_students}", font=("Inter", 12, "bold"), text_color="#334155").pack(anchor="e")
        
        # Progress Bar visual
        # Background bar
        bg_bar = ctk.CTkFrame(count_frame, height=6, width=100, fg_color="#E2E8F0", corner_radius=3)
        bg_bar.pack(anchor="e", pady=(5,0))
        bg_bar.pack_propagate(False)
        
        # Fill bar
        pct = current / max_students
        fill_width = int(100 * pct)
        fill_bar = ctk.CTkFrame(bg_bar, height=6, width=fill_width, fg_color="#6366F1", corner_radius=3)
        fill_bar.place(x=0, y=0)

        # Separator line
        sep = ctk.CTkFrame(parent, height=1, fg_color="#F1F5F9")
        sep.pack(fill="x", padx=20)

    def _create_quick_actions(self, parent):
        ctk.CTkLabel(
            parent,
            text="QUICK ACTIONS",
            font=("Inter", 11, "bold"),
            text_color="#94A3B8"
        ).pack(fill="x", padx=10, pady=(20, 15), anchor="w")
        
        # Action Cards
        self._add_action_card(parent, "QR Lab Key", "SESSION START", "🔳", "#EEF2FF", "#6366F1")
        self._add_action_card(parent, "Remote Link", "HYBRID MODE", "🔗", "#Ffff", "#000") # Simple white
        self._add_action_card(parent, "Bulk CSV", "9C9DA2", "📄", "#FFF", "#000")

    def _add_action_card(self, parent, title, subtitle, icon, bg_color_icon, icon_color):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, height=90)
        card.pack(fill="x", pady=8)
        card.pack_propagate(False)
        
        # Icon
        # If bg_color_icon is meant for valid color string
        icon_box = ctk.CTkFrame(card, width=50, height=50, fg_color="#F8FAFC", corner_radius=12) # Default placeholder bg
        icon_box.pack(side="left", padx=20)
        # Apply specific color if needed
        # ...
        
        ctk.CTkLabel(icon_box, text=icon, font=("Arial", 20), text_color=icon_color).place(relx=0.5, rely=0.5, anchor="center")
        
        # Text
        text_box = ctk.CTkFrame(card, fg_color="transparent")
        text_box.pack(side="left", fill="y", pady=20)
        
        ctk.CTkLabel(text_box, text=title, font=("Inter", 12, "bold"), text_color="#0F172A").pack(anchor="w")
        
        subtitle_color = "#6366F1" if "SESSION START" in subtitle else "#94A3B8"
        ctk.CTkLabel(text_box, text=subtitle, font=("Inter", 10, "bold"), text_color=subtitle_color).pack(anchor="w")
