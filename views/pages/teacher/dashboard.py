"""
Teacher Dashboard - Dashboard Page for Teachers
================================================

Dashboard hiển thị thống kê và thông tin cho giáo viên.
Match UI from Image 1.
"""

import customtkinter as ctk
import tkinter as tk
from typing import Optional, List
from datetime import datetime

# Assuming these exist or will serve as placeholders
from core.models import Teacher
from controllers.teacher_controller import TeacherController

class TeacherDashboardPage(ctk.CTkFrame):
    """
    Dashboard page cho Teacher.
    Matches Image 1 UI.
    """
    
    def __init__(self, parent, teacher: Teacher, controller: TeacherController):
        super().__init__(parent, fg_color="transparent")
        
        self.teacher = teacher
        self.controller = controller
        
        # Grid layout: Main Content (Left) + Side Panel (Right)
        self.grid_columnconfigure(0, weight=3) # Main content
        self.grid_columnconfigure(1, weight=1) # Side panel (Class Roadmap)
        self.grid_rowconfigure(0, weight=1)
        
        self._setup_ui()
        # self.load_data() # Call to load dynamic data

    def _setup_ui(self):
        # --- Left Column: Stats & Graph ---
        self.left_col = ctk.CTkFrame(self, fg_color="transparent")
        self.left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        # 1. Stats Row
        self._create_stats_row(self.left_col)
        
        # 2. Graph Section
        self._create_graph_section(self.left_col)
        
        # --- Right Column: Class Roadmap ---
        self._create_roadmap_panel(self)

    def _create_stats_row(self, parent):
        # Title / Subtitle
        # In the image, there is a purple tag "DS FACULTY LOAD: 3 SUBJECTS"
        # and "You have 2 classes in today's session"
        
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        tag = ctk.CTkLabel(
            header_frame, 
            text="● DS FACULTY LOAD: 3 SUBJECTS", 
            text_color="#A855F7", # Purple-500
            font=("Inter", 12, "bold"),
            anchor="w"
        )
        tag.pack(fill="x")
        
        sub = ctk.CTkLabel(
            header_frame,
            text="You have 2 classes in today's session",
            text_color="#64748B",
            font=("Inter", 12),
            anchor="w"
        )
        sub.pack(fill="x", pady=(5, 0))

        # Stats Cards Container
        stats_container = ctk.CTkFrame(parent, fg_color="transparent")
        stats_container.pack(fill="x", pady=10)
        
        # 4 Cards
        # 1. Assigned Subject
        self._add_stat_card(stats_container, "ASSIGNED SUBJECT", "14", "📖", "#6366F1", side="left")
        # 2. Unique Student
        self._add_stat_card(stats_container, "UNIQUE STUDENT", "180", "👥", "#0EA5E9", side="left")
        # 3. Avg Attendance
        self._add_stat_card(stats_container, "AVG ATTENDANCE", "5%", "📈", "#F59E0B", side="left")
        # 4. Avg Attendance %
        self._add_stat_card(stats_container, "AVG ATTENDANCE", "94.2%", "💓", "#10B981", side="left")

    def _add_stat_card(self, parent, title, value, icon, icon_color, side="left"):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        card.pack(side=side, expand=True, fill="both", padx=5)
        
        # Inner layout
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(padx=20, pady=20, fill="both")
        
        # Icon Area (Left)
        icon_lbl = ctk.CTkLabel(
            content, 
            text=icon, 
            font=("Arial", 24),
            text_color=icon_color,
            width=40 
        )
        icon_lbl.pack(side="left", padx=(0, 10))
        
        # Text Area (Right)
        text_area = ctk.CTkFrame(content, fg_color="transparent")
        text_area.pack(side="left")
        
        ctk.CTkLabel(
            text_area, 
            text=title, 
            font=("Inter", 10, "bold"),
            text_color="#94A3B8"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_area, 
            text=value, 
            font=("Inter", 20, "bold"),
            text_color="#1E293B"
        ).pack(anchor="w")

    def _create_graph_section(self, parent):
        graph_card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, height=400)
        graph_card.pack(fill="x", pady=20)
        graph_card.pack_propagate(False) # Force height
        
        # Graph Header
        header = ctk.CTkFrame(graph_card, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            header,
            text="ATTENDANCE LOAD (PRESENT / MAX)",
            font=("Inter", 12, "bold"),
            text_color="#1E293B"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text="ACTIVE TELEMETRY",
            font=("Inter", 10, "bold"),
            text_color="#6366F1",
            fg_color="#EEF2FF",
            corner_radius=5,
            width=120,
            height=25
        ).pack(side="right")
        
        # Canvas for Graph Drawing
        self.canvas = tk.Canvas(
            graph_card, 
            bg="white", 
            highlightthickness=0,
            height=300
        )
        self.canvas.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Draw Mock Graph
        self._draw_mock_graph()

    def _draw_mock_graph(self):
        w = 800 # approximate available width
        h = 300
        padding = 40
        
        # Axes
        self.canvas.create_line(padding, h-padding, w-padding, h-padding, fill="#E2E8F0", width=1) # X axis
        self.canvas.create_line(padding, padding, padding, h-padding, fill="#E2E8F0", width=1) # Y axis
        
        # Grid lines (Horizontal)
        for i in range(4):
            y = padding + (h-2*padding) * i / 3
            self.canvas.create_line(padding, y, w-padding, y, fill="#F1F5F9", width=1, dash=(5, 5))
            
        # Data points (Mocking the curve in image)
        # Mon, Tue, Wed, Thu, Fri, Sat
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        points = [
            (0, 120),  # Mon (High)
            (1, 60),   # Tue
            (2, 55),   # Wed
            (3, 70),   # Thu
            (4, 80),   # Fri
            (5, 60)    # Sat
        ]
        
        # Scale mapping
        x_step = (w - 2*padding) / (len(days) - 1)
        y_max = 150
        
        canvas_points = []
        for i, val in points:
            x = padding + i * x_step
            y = (h - padding) - (val / y_max * (h - 2*padding))
            canvas_points.append((x, y))
            
            # X Labels
            self.canvas.create_text(x, h-padding+15, text=days[i], fill="#94A3B8", font=("Arial", 10))

        # Y Labels (approx)
        for i in range(4):
            y = padding + (h-2*padding) * i / 3
            val = y_max - (i/3 * y_max)
            self.canvas.create_text(padding-20, y, text=str(int(val)), fill="#94A3B8", font=("Arial", 10))

        # Draw Smoothish Line (Polyline for simplicity)
        # To make it smooth like the image would require bezier curves, stick to lines for MVP or simple smooth
        # Simple line
        for i in range(len(canvas_points) - 1):
            x1, y1 = canvas_points[i]
            x2, y2 = canvas_points[i+1]
            self.canvas.create_line(x1, y1, x2, y2, fill="#8B5CF6", width=3, capstyle=tk.ROUND, smooth=True)

    def _create_roadmap_panel(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="#0F172A", corner_radius=15) # Dark Blue Panel
        panel.grid(row=0, column=1, sticky="nsew", pady=0)
        panel.pack_propagate(False)
        
        # Header
        ctk.CTkLabel(
            panel,
            text="CLASS ROADMAP",
            text_color="#22C55E", # Green
            font=("Inter", 12, "bold"),
            anchor="w"
        ).pack(fill="x", padx=20, pady=(25, 10))
        
        # Today Section
        ctk.CTkLabel(
            panel,
            text="TODAY",
            text_color="white",
            font=("Inter", 11, "bold"),
            anchor="w"
        ).pack(fill="x", padx=20, pady=(10, 5))
        
        self._add_class_item(panel, "Probability and Statistics", "8:00 AM - 56/60", "#EC4899") # Pink accent
        self._add_class_item(panel, "Computer Architecture", "1:00 PM - 54/60", "#FACC15") # Yellow accent
        
        # Tomorrow Section
        ctk.CTkLabel(
            panel,
            text="TOMORROW",
            text_color="white",
            font=("Inter", 11, "bold"),
            anchor="w"
        ).pack(fill="x", padx=20, pady=(20, 5))
        
        self._add_class_item(panel, "Data Structures and Algorithms", "10:00 AM - 0/50", "#EF4444") # Red
        self._add_class_item(panel, "Databases", "3:30 PM - 56/60", "#22C55E") # Green

        # Button at bottom
        ctk.CTkButton(
            panel,
            text="VIEW ALL LAB SCHEDULES",
            fg_color="#334155",
            hover_color="#475569",
            text_color="white",
            height=40,
            font=("Inter", 10, "bold"),
            corner_radius=20
        ).pack(side="bottom", padx=20, pady=30, fill="x")

    def _add_class_item(self, parent, name, time_info, accent_color):
        item = ctk.CTkFrame(parent, fg_color="#1E293B", corner_radius=10)
        item.pack(fill="x", padx=20, pady=5)
        
        # Accent Bar
        bar = ctk.CTkFrame(item, fg_color=accent_color, width=4, corner_radius=2)
        bar.pack(side="left", fill="y", padx=(0, 10))
        
        # Content
        content = ctk.CTkFrame(item, fg_color="transparent")
        content.pack(side="left", padx=5, pady=10)
        
        ctk.CTkLabel(
            content,
            text=name,
            text_color="white",
            font=("Inter", 11, "bold"),
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            content,
            text=time_info,
            text_color="#94A3B8",
            font=("Inter", 10),
            anchor="w"
        ).pack(anchor="w")
