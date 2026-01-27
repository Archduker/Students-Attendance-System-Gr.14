import customtkinter as ctk
from datetime import datetime
import threading

from views.components.modal import Modal

# --- Constants & Theme ---
COLORS = {
    "primary": "#3B82F6",      # Blue
    "success": "#22C55E",      # Green
    "warning": "#F59E0B",      # Orange
    "error": "#EF4444",        # Red
    "purple": "#7C3AED",       # Purple
    
    "bg_light": "#F3F4F6",     # Light gray bg
    "bg_dark": "#0F172A",      # Dark bg
    "bg_card": "#FFFFFF",      # White card
    
    "text_primary": "#1E293B", # Dark text
    "text_secondary": "#64748B", # Gray text
    "text_muted": "#94A3B8",   # Light gray text
    "border": "#E2E8F0"        # Light border
}

FONTS = {
    "header": ("Inter", 28, "bold"),
    "subheader": ("Inter", 14),
    "tag": ("Inter", 11, "bold"),
    "card_label": ("Inter", 11, "bold"),
    "card_value": ("Inter", 28, "bold"),
    "section_title": ("Inter", 12, "bold"),
    "body_bold": ("Inter", 12, "bold"),
    "body": ("Inter", 12),
    "body_sm": ("Inter", 11),
    "body_xs": ("Inter", 10)
}

class StudentDashboard(ctk.CTkFrame):
    def __init__(self, master, on_navigate=None, user=None, user_name="Student", student_service=None, student_controller=None):
        super().__init__(master, fg_color=COLORS["bg_light"])
        self.pack(expand=True, fill="both")
        
        self.on_navigate = on_navigate
        self.user = user
        self.student_service = student_service
        self.student_controller = student_controller
        
        # Determine display name and student code
        self.display_name = user_name
        self.student_code = "UNKNOWN"
        
        if user:
            self.display_name = user.full_name if hasattr(user, 'full_name') else user.username
            if hasattr(user, 'student_code'):
                self.student_code = user.student_code
            elif hasattr(user, 'username'): 
                self.student_code = user.username
        
        # Setup UI Containers
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Init UI
        self._init_ui()
        
        # Load Data
        self.refresh_dashboard()
        
        # Start Auto Refresh (1 minute)
        self.after(60000, self._auto_refresh_loop)

    def _auto_refresh_loop(self):
        if self.winfo_exists():
            self.refresh_dashboard()
            self.after(60000, self._auto_refresh_loop)

    def _init_ui(self):
        # 1. Welcome Section
        self._create_welcome_section()
        
        # 2. Stats Section
        self.stats_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.stats_container.pack(fill="x", pady=(25, 0))
        
        # 3. Bottom Grid (Schedule & Log)
        self.bottom_grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.bottom_grid.pack(fill="both", expand=True, pady=25)
        self.bottom_grid.grid_columnconfigure(0, weight=3)
        self.bottom_grid.grid_columnconfigure(1, weight=2)
        self.bottom_grid.grid_rowconfigure(0, weight=1)
        
        # Schedule Frame (Left)
        self.schedule_frame = ctk.CTkFrame(self.bottom_grid, fg_color=COLORS["bg_card"], corner_radius=16, border_width=1, border_color=COLORS["border"])
        self.schedule_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        self.schedule_frame.pack_propagate(False)
        
        # Log Frame (Right, Dark)
        self.log_frame = ctk.CTkFrame(self.bottom_grid, fg_color=COLORS["bg_dark"], corner_radius=16)
        self.log_frame.grid(row=0, column=1, sticky="nsew")
        self.log_frame.pack_propagate(False)

    def _create_welcome_section(self):
        frm = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frm.pack(fill="x")
        
        # Student Tag
        tag = ctk.CTkLabel(
            frm, 
            text=f"●  {self.student_code}", 
            text_color=COLORS["purple"], 
            fg_color="#F3E8FF", 
            corner_radius=6, 
            font=FONTS["tag"], 
            padx=10, pady=4
        )
        tag.pack(anchor="w", pady=(0, 8))
        
        # Greeting
        ctk.CTkLabel(frm, text=f"Hi, {self.display_name}!", font=FONTS["header"], text_color=COLORS["text_primary"]).pack(anchor="w")
        
        # Date/Subtext
        today_str = datetime.now().strftime("%A, %d %B %Y")
        ctk.CTkLabel(frm, text=f"Today is {today_str}. Have a great learning session!", font=FONTS["subheader"], text_color=COLORS["text_secondary"]).pack(anchor="w")
        
        # Action Button
        action_btn = ctk.CTkButton(
            frm,
            text="MARK SESSION PRESENT  ➔",
            font=("Inter", 11, "bold"),
            fg_color="black",
            text_color="white",
            corner_radius=20,
            height=40,
            hover_color="#333333",
            command=self._on_mark_present_click
        )
        action_btn.place(relx=1.0, rely=0.5, anchor="e")

    def refresh_dashboard(self):
        """Fetch data and update UI."""
        print(f"DEBUG: refresh_dashboard called for student: {self.student_code}")
        
        if not self.student_service:
            print("❌ ERROR: student_service is None!")
            # Show empty/demo state if service not injected (fallback)
            self._update_stats_demo()
            return
            
        try:
            print(f"📊 Fetching dashboard stats for {self.student_code}...")
            # Fetch Data
            # 1. Stats & Recent Log
            stats = self.student_service.get_dashboard_stats(self.student_code)
            print(f"✅ Stats retrieved: {stats}")
            
            # 2. Today's Sessions
            print(f"📅 Fetching today's sessions...")
            todays_sessions = self.student_service.get_todays_sessions(self.student_code)
            print(f"✅ Sessions retrieved: {len(todays_sessions)} sessions")
            
            # Update UI
            self._update_stats(stats)
            self._update_schedule(todays_sessions)
            self._update_log(stats.get("recent_attendance", []))
            
        except Exception as e:
            print(f"❌ Error refreshing dashboard: {e}")
            import traceback
            traceback.print_exc()
            # Could show error toast here

    def _update_stats(self, stats):
        # Clear old stats
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        
        # Safe dictionary access with defaults
        attendance_rate = stats.get('attendance_rate', 0) if stats else 0
        total_sessions = stats.get('total_sessions', 0) if stats else 0
        present_count = stats.get('present_count', 0) if stats else 0
        absent_count = stats.get('absent_count', 0) if stats else 0
        
        print(f"📊 Updating stats - Rate: {attendance_rate}%, Total: {total_sessions}, Present: {present_count}, Absent: {absent_count}")
        
        # Data preparation
        items = [
            ("ATTENDANCE", f"{attendance_rate}%", "✅", COLORS["success"]),
            ("TOTAL SESSIONS", str(total_sessions), "📚", COLORS["purple"]),
            ("PRESENT", str(present_count), "✅", COLORS["success"]),
            ("ABSENT", str(absent_count), "❌", COLORS["error"])
        ]
        
        for i, (label, val, icon, color) in enumerate(items):
            self._create_stat_card(self.stats_container, label, val, icon, color, i==0)
            
    def _create_stat_card(self, parent, label, value, icon, color, is_first):
        card = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], height=120, corner_radius=16, border_width=1, border_color=COLORS["border"])
        card.pack(side="left", fill="x", expand=True, padx=(0 if is_first else 15, 0))
        card.pack_propagate(False)
        
        head = ctk.CTkFrame(card, fg_color="transparent")
        head.pack(fill="x", padx=25, pady=(25, 10))
        
        # Icon + Label
        ctk.CTkLabel(head, text=icon, font=("Inter", 14)).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(head, text=label, text_color=COLORS["text_muted"], font=FONTS["card_label"]).pack(side="left")
        
        # Value
        ctk.CTkLabel(card, text=value, text_color=COLORS["text_primary"], font=FONTS["card_value"]).pack(anchor="w", padx=25)
        
        # Bottom Line
        # ctk.CTkFrame(card, height=4, fg_color=color, width=1000).pack(side="bottom", fill="x") # Optional accent

    def _update_schedule(self, sessions):
        # Clear
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()
            
        # Header
        head = ctk.CTkFrame(self.schedule_frame, fg_color="transparent")
        head.pack(fill="x", padx=25, pady=25)
        ctk.CTkLabel(head, text="ACADEMIC SCHEDULE TODAY", font=FONTS["section_title"], text_color=COLORS["text_secondary"]).pack(side="left")
        ctk.CTkLabel(head, text="SEMESTER PLAN", font=FONTS["card_label"], text_color=COLORS["primary"]).pack(side="right")
        
        # Content
        if not sessions or sessions is None:
            print(f"⚠️ No sessions to display: {sessions}")
            self._show_empty_state(self.schedule_frame, "No classes scheduled for today")
            return
        
        print(f"📚 Displaying {len(sessions)} sessions for today")
        scroll = ctk.CTkScrollableFrame(self.schedule_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 15))
        
        for session in sessions:
            self._create_schedule_item(scroll, session)

    def _create_schedule_item(self, parent, session):
        row = ctk.CTkFrame(parent, fg_color="transparent", height=80)
        row.pack(fill="x", padx=10, pady=5)
        
        # Icon Box (Initials)
        initials = session['class_name'][:2].upper()
        icon_box = ctk.CTkFrame(row, width=50, height=50, fg_color="white", border_width=1, border_color=COLORS["border"], corner_radius=12)
        icon_box.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(icon_box, text=session['subject_code'][:3], font=FONTS["body_xs"], text_color="gray").place(relx=0.5, rely=0.3, anchor="center")
        ctk.CTkLabel(icon_box, text=initials, font=FONTS["body_bold"], text_color="black").place(relx=0.5, rely=0.7, anchor="center")
        
        # Info
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(info, text=session['class_name'], font=FONTS["body_bold"], text_color=COLORS["text_primary"]).pack(anchor="w")
        
        time_text = f"🕒 {session['start_time']} - {session['end_time']}   📍 {session['room']}"
        ctk.CTkLabel(info, text=time_text, font=FONTS["body_sm"], text_color=COLORS["text_secondary"]).pack(anchor="w", pady=(4, 0))
        
        # Status Badge
        status = session['status']
        bg_color = "#F3E8FF" if status == "OPEN" else "#F3F4F6"
        fg_color = COLORS["purple"] if status == "OPEN" else COLORS["text_secondary"]
        status_text = "IN SESSION" if status == "OPEN" else status
        
        ctk.CTkLabel(
            row, 
            text=status_text, 
            fg_color=bg_color, 
            text_color=fg_color, 
            font=FONTS["tag"], 
            corner_radius=12, 
            width=100, 
            height=30
        ).pack(side="right")

    def _update_log(self, logs):
        # Clear
        for widget in self.log_frame.winfo_children():
            widget.destroy()
            
        # Header
        ctk.CTkLabel(self.log_frame, text="VERIFICATION LOG", font=FONTS["section_title"], text_color=COLORS["success"]).pack(anchor="w", padx=25, pady=25)
        
        # Handle None or empty logs
        if not logs or logs is None:
            print(f"⚠️ No logs to display: {logs}")
            self._show_empty_state(self.log_frame, "No attendance records yet", dark=True)
        else:
            print(f"📋 Displaying {len(logs)} log entries")
            scroll = ctk.CTkScrollableFrame(self.log_frame, fg_color="transparent")
            scroll.pack(fill="both", expand=True, padx=5, pady=(0, 20))
            
            for log in logs:
                self._create_log_item(scroll, log)
        
        # Download Button
        ctk.CTkButton(
            self.log_frame, 
            text="DOWNLOAD FULL TRANSCRIPT",
            font=FONTS["tag"],
            fg_color="transparent",
            border_width=1,
            border_color="#334155",
            hover_color="#1E293B",
            height=40,
            corner_radius=20
        ).pack(side="bottom", pady=30)

    def _create_log_item(self, parent, log):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=8)
        
        # Status color
        status_map = {
            "PRESENT": COLORS["success"],
            "ABSENT": COLORS["error"],
            "LATE": COLORS["warning"]
        }
        color = status_map.get(log['status'], COLORS["text_muted"])
        
        # Bar indicator
        ctk.CTkFrame(row, width=3, height=40, fg_color=color).pack(side="left")
        
        content = ctk.CTkFrame(row, fg_color="transparent")
        content.pack(side="left", padx=15, fill="x", expand=True)
        
        # Top line
        top = ctk.CTkFrame(content, fg_color="transparent")
        top.pack(fill="x")
        ctk.CTkLabel(top, text=log.get('class_name', 'Unknown Class'), font=FONTS["body_bold"], text_color="white").pack(side="left")
        
        # Format date for right side
        # Assuming log['date'] is YYYY-MM-DD
        try:
            date_obj = datetime.strptime(log['date'], "%Y-%m-%d")
            date_str = date_obj.strftime("%d %b")
        except:
            date_str = log['date']
            
        ctk.CTkLabel(top, text=f"{date_str}, {log['time']}", font=FONTS["body_xs"], text_color=COLORS["text_secondary"]).pack(side="right")
        
        # Bottom line
        ctk.CTkLabel(content, text=f"Status: {log['status'].title()}", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).pack(anchor="w", pady=(2, 0))

    def _show_empty_state(self, parent, message, dark=False):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(expand=True, fill="both")
        
        icon = "📭"
        color = COLORS["text_muted"] if not dark else "#475569"
        
        ctk.CTkLabel(frame, text=icon, font=("Inter", 40)).pack(pady=(20, 10))
        ctk.CTkLabel(frame, text=message, font=FONTS["body"], text_color=color).pack()

    def _update_stats_demo(self):
        # Fallback for preview/testing without service
        stats = {
            "attendance_rate": 95,
            "total_sessions": 18,
            "present_count": 17,
            "absent_count": 1
        }
        self._update_stats(stats)
        self._show_empty_state(self.schedule_frame, "Service not connected")
        self._show_empty_state(self.log_frame, "Service not connected", dark=True)

    def _on_mark_present_click(self):
        if self.on_navigate:
            self.on_navigate("submit_attendance")
