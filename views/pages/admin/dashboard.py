"""
Admin Dashboard - System Pulse
==============================

Dashboard tổng quan hệ thống cho Admin.
Matching UI from Image 2: System Pulse with metrics, purple wave chart, and Access Control panel.
"""

import customtkinter as ctk
from typing import Optional
import math

class AdminDashboard(ctk.CTkFrame):
    """
    Admin Dashboard showing system pulse and metrics.
    Matches Image 2 design.
    """
    
    def __init__(self, parent, admin_user=None, controller=None):
        super().__init__(parent, fg_color="transparent")
        
        self.admin_user = admin_user
        self.controller = controller
        
        # Grid layout: Main content (left, 70%) + Access Control (right, 30%)
        self.grid_columnconfigure(0, weight=7)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        self._setup_ui()
        # self.load_data()
    
    def _setup_ui(self):
        # Left column: Main content
        left_col = ctk.CTkFrame(self, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        self._create_header(left_col)
        self._create_metrics_cards(left_col)
        self._create_attendance_graph(left_col)
        self._create_audit_alerts(left_col)
        
        # Right column: Access Control
        right_col = ctk.CTkFrame(self, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew")
        
        self._create_access_control(right_col)
    
    def _create_header(self, parent):
        """Header with title and Reboot button."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        # Title section
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="System Pulse",
            font=("Inter", 26, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Monitoring 9 academic time-slots and infrastructure integrity.",
            font=("Inter", 12),
            text_color="#64748B"
        ).pack(anchor="w")
        
        # Reboot button
        ctk.CTkButton(
            header,
            text="Reboot Telemetry",
            fg_color="#0F172A",
            text_color="white",
            font=("Inter", 11, "bold"),
            width=150,
            height=35,
            corner_radius=8,
            hover_color="#1E293B"
        ).pack(side="right")
    
    def _create_metrics_cards(self, parent):
        """4 metrics cards in a row."""
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        
        # Configure grid for 4 equal columns
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Mock data - will be replaced with real data from controller
        metrics = [
            ("💚 Cluster Health", "Optimal", "#22C55E"),
            ("🔵 QR Latency", "14ms", "#3B82F6"),
            ("🟣 DB Connections", "182", "#A855F7"),
            ("🟡 Verified Auth", "1.2K", "#EAB308"),
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            self._create_metric_card(cards_frame, label, value, color, i)
    
    def _create_metric_card(self, parent, label, value, color, col):
        """Single metric card."""
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E2E8F0"
        )
        card.grid(row=0, column=col, sticky="ew", padx=7, pady=5)
        
        # Content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", padx=20, pady=20)
        
        # Label with icon
        ctk.CTkLabel(
            content,
            text=label,
            font=("Inter", 11),
            text_color="#64748B"
        ).pack(anchor="w")
        
        # Value
        ctk.CTkLabel(
            content,
            text=value,
            font=("Inter", 24, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w", pady=(5, 0))
    
    def _create_attendance_graph(self, parent):
        """Purple wave chart showing attendance pulse."""
        graph_card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E2E8F0"
        )
        graph_card.pack(fill="both", expand=True, pady=(0, 20))
        
        # Header
        header = ctk.CTkFrame(graph_card, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=20)
        
        # Title
        title_area = ctk.CTkFrame(header, fg_color="transparent")
        title_area.pack(side="left")
        
        ctk.CTkLabel(
            title_area,
            text="Global Attendance Pulse (5 Daily Peaks)",
            font=("Inter", 14, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")
        
        # Active badge
        badge = ctk.CTkLabel(
            header,
            text="ACTIVE TELEMETRY",
            font=("Inter", 9, "bold"),
            text_color="#A855F7",
            fg_color="#F3E8FF",
            corner_radius=5,
            padx=10,
            pady=5
        )
        badge.pack(side="right")
        
        # Canvas for chart
        canvas = ctk.CTkCanvas(
            graph_card,
            bg="white",
            highlightthickness=0,
            height=250
        )
        canvas.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        
        # Draw simple wave chart after widget is shown
        canvas.bind("<Configure>", lambda e: self._draw_wave_chart(canvas))
    
    def _draw_wave_chart(self, canvas):
        """Draw purple wave chart on canvas."""
        canvas.delete("all")  # Clear previous drawings
        
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Draw time labels (X-axis)
        times = ["07:30", "08:00", "09:00", "10:00", "11:30", "12:30", "13:00", "14:30", "15:00", "16:30", "17:30"]
        step_x = width / (len(times) - 1)
        
        for i, time in enumerate(times):
            x = i * step_x
            canvas.create_text(x, height - 10, text=time, fill="#94A3B8", font=("Inter", 9))
        
        # Draw wave (5 peaks as mentioned)
        points = []
        num_points = 50
        for i in range(num_points):
            x = (i / (num_points - 1)) * width
            # Create wave with 5 peaks
            y_val = 0.5 + 0.4 * math.sin(5 * 2 * math.pi * i / num_points)
            y = (1 - y_val) * (height - 40) + 20
            points.append((x, y))
        
        # Fill area under curve (light purple)
        fill_points = [(0, height - 30)] + points + [(width, height - 30)]
        canvas.create_polygon(fill_points, fill="#E9D5FF", outline="")
        
        # Draw line (dark purple)
        for i in range(len(points) - 1):
            canvas.create_line(
                points[i][0], points[i][1],
                points[i+1][0], points[i+1][1],
                fill="#A855F7", width=3, smooth=True
            )
    
    def _create_audit_alerts(self, parent):
        """Identity Audit Alerts section."""
        alerts_card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E2E8F0"
        )
        alerts_card.pack(fill="x")
        
        # Content
        content = ctk.CTkFrame(alerts_card, fg_color="transparent")
        content.pack(fill="x", padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            header,
            text="Identity Audit Alerts",
            font=("Inter", 13, "bold"),
            text_color="#0F172A"
        ).pack(side="left")
        
        badge = ctk.CTkLabel(
            header,
            text="1 URGENT",
            font=("Inter", 9, "bold"),
            text_color="#EF4444",
            fg_color="#FEE2E2",
            corner_radius=5,
            padx=8,
            pady=4
        )
        badge.pack(side="right")
        
        # Alert item
        alert = ctk.CTkFrame(content, fg_color="#FEF2F2", corner_radius=10)
        alert.pack(fill="x", pady=5)
        
        alert_content = ctk.CTkFrame(alert, fg_color="transparent")
        alert_content.pack(fill="x", padx=15, pady=12)
        
        # Alert text
        info_frame = ctk.CTkFrame(alert_content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text="Geofence Violation Detected",
            font=("Inter", 12, "bold"),
            text_color="#DC2626"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text="3 students attempted validation outside HCMC UT perimeter.",
            font=("Inter", 10),
            text_color="#7F1D1D"
        ).pack(anchor="w")
        
        # Time
        ctk.CTkLabel(
            alert_content,
            text="4m ago",
            font=("Inter", 10),
            text_color="#94A3B8"
        ).pack(side="right", padx=(10, 0))
        
        # Link
        link = ctk.CTkLabel(
            content,
            text="Audit GPS Logs",
            font=("Inter", 11, "underline"),
            text_color="#3B82F6",
            cursor="hand2"
        )
        link.pack(anchor="w", pady=(5, 0))
    
    def _create_access_control(self, parent):
        """Access Control panel (dark theme)."""
        panel = ctk.CTkFrame(
            parent,
            fg_color="#0F172A",  # Dark
            corner_radius=15
        )
        panel.pack(fill="both", expand=True)
        
        # Header
        ctk.CTkLabel(
            panel,
            text="ACCESS CONTROL",
            font=("Inter", 12, "bold"),
            text_color="#22D3EE"  # Cyan
        ).pack(anchor="w", padx=25, pady=(25, 20))
        
        # QR Encryption section
        qr_section = ctk.CTkFrame(panel, fg_color="transparent")
        qr_section.pack(fill="x", padx=25, pady=(0, 20))
        
        ctk.CTkLabel(
            qr_section,
            text="QR ENCRYPTION",
            font=("Inter", 9, "bold"),
            text_color="#64748B"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            qr_section,
            text="AES-256 Rotation",
            font=("Inter", 13, "bold"),
            text_color="white"
        ).pack(anchor="w", pady=(5, 5))
        
        status_frame = ctk.CTkFrame(qr_section, fg_color="transparent")
        status_frame.pack(anchor="w")
        
        ctk.CTkLabel(
            status_frame,
            text="● ACTIVE",
            font=("Inter", 10),
            text_color="#22C55E"
        ).pack(side="left")
        
        # Identity Sync section
        sync_section = ctk.CTkFrame(panel, fg_color="transparent")
        sync_section.pack(fill="x", padx=25, pady=(0, 25))
        
        ctk.CTkLabel(
            sync_section,
            text="IDENTITY SYNC",
            font=("Inter", 9, "bold"),
            text_color="#64748B"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            sync_section,
            text="1,250 Verified Profiles",
            font=("Inter", 13, "bold"),
            text_color="white"
        ).pack(anchor="w", pady=(5, 10))
        
        # Progress bar
        progress_bg = ctk.CTkFrame(sync_section, height=6, fg_color="#334155", corner_radius=3)
        progress_bg.pack(fill="x", pady=(0, 5))
        progress_bg.pack_propagate(False)
        
        progress_fill = ctk.CTkFrame(progress_bg, height=6, fg_color="#A855F7", corner_radius=3)
        progress_fill.place(relwidth=0.83, relheight=1)  # 83% = 1250/1500
        
        # Button
        ctk.CTkButton(
            panel,
            text="SYSTEM-WIDE AUDIT",
            fg_color="#6366F1",
            text_color="white",
            font=("Inter", 11, "bold"),
            height=40,
            corner_radius=8,
            hover_color="#4F46E5"
        ).pack(fill="x", padx=25, pady=(0, 25))
