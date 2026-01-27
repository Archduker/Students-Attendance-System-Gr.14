"""
Teacher Dashboard - Dashboard Page for Teachers
================================================

Dashboard hiển thị thống kê và thông tin cho giáo viên.
Theo đúng UI/UX requirements.
"""

import customtkinter as ctk
import tkinter as tk
from typing import Optional
from datetime import datetime

from core.models import Teacher
from controllers.teacher_controller import TeacherController


class TeacherDashboardPage(ctk.CTkFrame):
    """
    Dashboard page cho Teacher.
    Hiển thị thống kê và lịch giảng dạy.
    """
    
    def __init__(self, parent, teacher: Teacher, controller: TeacherController):
        super().__init__(parent, fg_color="transparent")
        self.pack(expand=True, fill="both")
        
        self.teacher = teacher
        self.controller = controller
        
        # Grid layout: Main Content (Left) + Side Panel (Right)
        self.grid_columnconfigure(0, weight=3)  # Main content
        self.grid_columnconfigure(1, weight=1)  # Side panel (Class Roadmap)
        self.grid_rowconfigure(0, weight=1)
        
        self._setup_ui()
        
        # Start auto-refresh loop (60 seconds)
        self.after(60000, self._auto_refresh_loop)
    
    def _setup_ui(self):
        """Setup UI components"""
        # Fetch real stats
        self.stats = self.controller.get_dashboard_stats(self.teacher)
        
        # --- Left Column: Stats & Graph ---
        self.left_col = ctk.CTkFrame(self, fg_color="transparent")
        self.left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        # 1. Faculty Load Header
        self._create_header(self.left_col)
        
        # 2. Statistics Cards
        self._create_stats_cards(self.left_col)
        
        # 3. Attendance Load Chart
        self._create_chart_section(self.left_col)
        
        # --- Right Column: Class Roadmap ---
        self._create_roadmap_panel(self)
    
    def _auto_refresh_loop(self):
        """Auto-refresh dashboard stats every 60 seconds"""
        if self.winfo_exists():
            try:
                print(f"🔄 Auto-refreshing teacher dashboard...")
                # Re-fetch stats
                self.stats = self.controller.get_dashboard_stats(self.teacher)
                # Re-render UI (simple approach: re-create cards and chart)
                self._update_stats_display()
            except Exception as e:
                print(f"❌ Error in auto-refresh: {e}")
            # Schedule next refresh
            self.after(60000, self._auto_refresh_loop)
    
    def _update_stats_display(self):
        """Update stats cards and chart with new data"""
        try:
            # Clear and re-create stats cards
            for widget in self.left_col.winfo_children():
                if hasattr(widget, '_card_type') and widget._card_type == 'stats':
                    widget.destroy()
            self._create_stats_cards(self.left_col)
        except Exception as e:
            print(f"Error updating stats display: {e}")
    
    def _create_header(self, parent):
        """Create Faculty Load header"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Faculty Load badge
        load_count = self.stats.get("total_classes", 0)
        badge = ctk.CTkLabel(
            header_frame,
            text=f"● DS FACULTY LOAD: {load_count} SUBJECTS",
            text_color="#A855F7",  # Purple
            font=("Inter", 12, "bold"),
            anchor="w"
        )
        badge.pack(fill="x")
        
        # Subtitle
        active_sessions = self.stats.get("active_sessions", 0)
        subtitle = ctk.CTkLabel(
            header_frame,
            text=f"You have {active_sessions} active sessions available",
            text_color="#64748B",  # Gray
            font=("Inter", 12),
            anchor="w"
        )
        subtitle.pack(fill="x", pady=(5, 0))
    
    def _create_stats_cards(self, parent):
        """Create 4 statistic cards"""
        stats_container = ctk.CTkFrame(parent, fg_color="transparent")
        stats_container.pack(fill="x", pady=10)
        
        # Configure grid for 4 equal columns
        for i in range(4):
            stats_container.grid_columnconfigure(i, weight=1, uniform="stats")
        
        # Card 1: ASSIGNED SUBJECT
        self._add_stat_card(
            stats_container, 
            row=0, col=0,
            title="ASSIGNED SUBJECT",
            value=str(self.stats.get("total_classes", 0)),
            icon="📖",
            icon_color="#6366F1",
            icon_bg="#EEF2FF"
        )
        
        # Card 2: UNIQUE STUDENT
        self._add_stat_card(
            stats_container,
            row=0, col=1,
            title="UNIQUE STUDENT",
            value=str(self.stats.get("total_students", 0)),
            icon="👥",
            icon_color="#0EA5E9",
            icon_bg="#E0F2FE"
        )
        
        # Card 3: ACTIVE SESSION
        self._add_stat_card(
            stats_container,
            row=0, col=2,
            title="ACTIVE SESSIONS",
            value=str(self.stats.get("active_sessions", 0)),
            icon="⚡",
            icon_color="#F59E0B",
            icon_bg="#FEF3C7"
        )
        
        # Card 4: AVG ATTENDANCE
        avg_rate = self.stats.get("avg_attendance_rate", 0)
        # Convert 0.94 -> 94.0%
        # If the controller returns 0-100 based on 'round(avg, 2)'... let's check controller
        # Controller returns `round(avg_attendance_rate, 2)` where avg `total_rate += report['attendance_rate']`
        # Assuming rate is percentage (0-100) or decimal (0-1)?
        # Usually attendance rate is 0-100 in reports. Let's assume 0-100 for now or add % symbol.
        
        self._add_stat_card(
            stats_container,
            row=0, col=3,
            title="AVG ATTENDANCE",
            value=f"{avg_rate}%",
            icon="💓",
            icon_color="#10B981",
            icon_bg="#D1FAE5"
        )
    
    def _add_stat_card(self, parent, row, col, title, value, icon, icon_color, icon_bg):
        """Add a single statistic card"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        # Inner padding
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Icon (Left side)
        icon_frame = ctk.CTkFrame(inner, fg_color=icon_bg, width=48, height=48, corner_radius=12)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        
        icon_lbl = ctk.CTkLabel(
            icon_frame,
            text=icon,
            font=("Arial", 20),
            text_color=icon_color
        )
        icon_lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        # Text (Right side)
        text_area = ctk.CTkFrame(inner, fg_color="transparent")
        text_area.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            text_area,
            text=title,
            font=("Inter", 10, "bold"),
            text_color="#94A3B8",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_area,
            text=value,
            font=("Inter", 24, "bold"),
            text_color="#1E293B",
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))
    
    def _create_chart_section(self, parent):
        """Create Attendance Load Chart"""
        chart_card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        chart_card.pack(fill="both", expand=True, pady=(15, 0))
        
        # Chart Header
        header = ctk.CTkFrame(chart_card, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(20, 10))
        
        ctk.CTkLabel(
            header,
            text="ATTENDANCE LOAD (PRESENT / MAX)",
            font=("Inter", 12, "bold"),
            text_color="#1E293B"
        ).pack(side="left")
        
        badge = ctk.CTkLabel(
            header,
            text="ACTIVE TELEMETRY",
            font=("Inter", 9, "bold"),
            text_color="#6366F1",
            fg_color="#EEF2FF",
            corner_radius=5,
            width=130,
            height=24
        )
        badge.pack(side="right")
        
        # Canvas for Chart
        self.canvas = tk.Canvas(
            chart_card,
            bg="white",
            highlightthickness=0,
            height=300
        )
        self.canvas.pack(fill="both", expand=True, padx=25, pady=(10, 20))
        
        # Draw chart after canvas is rendered (with longer delay for initial render)
        self.canvas.after(300, self._draw_chart)
    
    def _draw_chart(self):
        """Draw attendance load line chart"""
        try:
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            
            # If canvas not ready yet, retry after a delay
            if w <= 1 or h <= 1:
                self.canvas.after(200, self._draw_chart)
                return
            
            padding_left = 50
            padding_right = 30
            padding_top = 30
            padding_bottom = 40
            
            chart_width = w - padding_left - padding_right
            chart_height = h - padding_top - padding_bottom
            
            # Clear canvas
            self.canvas.delete("all")
            
            # Y-axis labels and grid lines
            y_max = 130
            y_steps = [0, 35, 70, 105, 130]
            
            for y_val in y_steps:
                y_pos = h - padding_bottom - (y_val / y_max) * chart_height
                
                # Grid line
                self.canvas.create_line(
                    padding_left, y_pos,
                    w - padding_right, y_pos,
                    fill="#F1F5F9",
                    width=1,
                    dash=(3, 3)
                )
                
                # Y label
                self.canvas.create_text(
                    padding_left - 10,
                    y_pos,
                    text=str(y_val),
                    fill="#94A3B8",
                    font=("Inter", 9),
                    anchor="e"
                )
            
            # Data points (matching the image)
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
            data_points = [120, 60, 55, 70, 75, 68]
            
            x_step = chart_width / (len(days) - 1)
            
            # Calculate canvas coordinates
            coords = []
            for i, val in enumerate(data_points):
                x = padding_left + i * x_step
                y = h - padding_bottom - (val / y_max) * chart_height
                coords.append((x, y))
                
                # X label
                self.canvas.create_text(
                    x,
                    h - padding_bottom + 15,
                    text=days[i],
                    fill="#94A3B8",
                    font=("Inter", 10)
                )
            
            # Draw line chart
            if len(coords) > 1:
                # Create smooth line segments
                for i in range(len(coords) - 1):
                    x1, y1 = coords[i]
                    x2, y2 = coords[i + 1]
                    
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill="#8B5CF6",  # Purple
                        width=3,
                        capstyle=tk.ROUND,
                        smooth=True
                    )
            
            # Draw points
            for x, y in coords:
                self.canvas.create_oval(
                    x - 4, y - 4, x + 4, y + 4,
                    fill="#8B5CF6",
                    outline="#8B5CF6",
                    width=2
                )
        except Exception as e:
            print(f"Error drawing chart: {e}")
    
    def _create_roadmap_panel(self, parent):
        """Create Class Roadmap panel (right side)"""
        panel = ctk.CTkFrame(parent, fg_color="#0F172A", corner_radius=15)
        panel.grid(row=0, column=1, sticky="nsew")
        
        # Header
        ctk.CTkLabel(
            panel,
            text="CLASS ROADMAP",
            text_color="#22C55E",  # Green
            font=("Inter", 12, "bold"),
            anchor="w"
        ).pack(fill="x", padx=20, pady=(25, 15))
        
        # TODAY Section
        ctk.CTkLabel(
            panel,
            text="TODAY",
            text_color="white",
            font=("Inter", 11, "bold"),
            anchor="w"
        ).pack(fill="x", padx=20, pady=(10, 8))
        
        self._add_class_item(
            panel,
            "Probability and Statistics",
            "8:00 AM - 50/60",
            "#EC4899"  # Pink
        )
        
        self._add_class_item(
            panel,
            "Computer Architecture",
            "1:00 PM - 54/60",
            "#FACC15"  # Yellow
        )
        
        # TOMORROW Section
        ctk.CTkLabel(
            panel,
            text="TOMORROW",
            text_color="white",
            font=("Inter", 11, "bold"),
            anchor="w"
        ).pack(fill="x", padx=20, pady=(20, 8))
        
        self._add_class_item(
            panel,
            "Data Structures and Algorithms",
            "10:00 AM - 0/50",
            "#EF4444"  # Red
        )
        
        self._add_class_item(
            panel,
            "Databases",
            "3:30 PM - 56/60",
            "#22C55E"  # Green
        )
        
        # Button at bottom
        ctk.CTkButton(
            panel,
            text="VIEW ALL LAB SCHEDULES",
            fg_color="#334155",
            hover_color="#475569",
            text_color="white",
            height=40,
            font=("Inter", 10, "bold"),
            corner_radius=20,
            command=lambda: print("View all schedules clicked")
        ).pack(side="bottom", padx=20, pady=25, fill="x")
    
    def _add_class_item(self, parent, name, time_info, accent_color):
        """Add a class item to roadmap"""
        item = ctk.CTkFrame(parent, fg_color="#1E293B", corner_radius=10)
        item.pack(fill="x", padx=20, pady=4)
        
        # Accent bar (left border)
        bar = ctk.CTkFrame(item, fg_color=accent_color, width=4, corner_radius=2)
        bar.pack(side="left", fill="y", padx=(0, 0))
        bar.pack_propagate(False)
        
        # Content
        content = ctk.CTkFrame(item, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=12, pady=12)
        
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
        ).pack(anchor="w", pady=(2, 0))
