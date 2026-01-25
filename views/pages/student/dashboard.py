import customtkinter as ctk
from views.layouts.student_layout import StudentLayout
from views.components.modal import Modal

class StudentDashboard(ctk.CTkFrame):
    def __init__(self, master, on_navigate=None, user=None, user_name="Student"):
        super().__init__(master, fg_color="#F3F4F6")
        self.pack(expand=True, fill="both")
        
        # Store user object and extract display name
        self.user = user
        if user:
            self.display_name = user.full_name if hasattr(user, 'full_name') else user_name
        else:
            self.display_name = user_name
            
        # Show Welcome Popup
        self.after(500, self._show_welcome_popup)

        # Welcome Section
        self._create_welcome_section()
        
        # Stats Cards
        self._create_stats_cards()
        
        # Bottom Section (Schedule + Log)
        self.bottom_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_grid.pack(fill="both", expand=True, pady=20)
        self.bottom_grid.grid_columnconfigure(0, weight=3) # Schedule
        self.bottom_grid.grid_columnconfigure(1, weight=2) # Log
        self.bottom_grid.grid_rowconfigure(0, weight=1)

        self._create_schedule(self.bottom_grid)
        self._create_verification_log(self.bottom_grid)

    def _show_welcome_popup(self):
        Modal(
            self.winfo_toplevel(),
            title="Welcome Back!",
            message=f"Good Morning, {self.display_name}!\nYour Probability and Statistics lab is starting in 15 minutes.",
            type="success",
            button_text="Go to Dashboard"
        )

    def _create_welcome_section(self):
        frm = ctk.CTkFrame(self, fg_color="transparent")
        frm.pack(fill="x", pady=(0, 20))
        
        # Breadcrumb / Tag
        # Use student code or Generic major if not available
        subtext = self.user.student_code if hasattr(self.user, 'student_code') else "DS Major • Year 2"
        ctk.CTkLabel(frm, text=f"●  {subtext}", text_color="#8B5CF6", fg_color="#F3E8FF", corner_radius=6, font=("Inter", 10, "bold"), padx=10, pady=2).pack(anchor="w", pady=(0, 10))
        
        # Header
        ctk.CTkLabel(frm, text=f"Hi, {self.display_name}!", font=("Inter", 24, "bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(frm, text="Your Probability and Statistics lab is live.", font=("Inter", 13), text_color="#64748B").pack(anchor="w")
        
        # Action Button (Floating right)
        action_btn = ctk.CTkButton(
            frm,
            text="MARK SESSION PRESENT  ➔",
            font=("Inter", 11, "bold"),
            fg_color="black",
            text_color="white",
            corner_radius=20,
            height=40
        )
        action_btn.place(relx=1.0, rely=0.5, anchor="e")

    def _create_stats_cards(self):
        cards_frm = ctk.CTkFrame(self, fg_color="transparent")
        cards_frm.pack(fill="x", pady=0)
        
        stats = [
            ("ATTENDANCE", "95%", "✅", "#22C55E"), # Green
            ("GPU LAB TIME", "18h", "🕒", "#7C3AED"), # Purple
            ("ABSENCES", "01", "🎒", "#EF4444"), # Red
            ("SCHOLAR RANK", "#11", "🏆", "#F59E0B")  # Orange
        ]
        
        for i, (label, val, icon, color) in enumerate(stats):
            card = ctk.CTkFrame(cards_frm, fg_color="white", height=100, corner_radius=15)
            card.pack(side="left", fill="x", expand=True, padx=(0 if i==0 else 15, 0))
            card.pack_propagate(False)
            
            # Header with icon
            head = ctk.CTkFrame(card, fg_color="transparent")
            head.pack(fill="x", padx=20, pady=15)
            ctk.CTkLabel(head, text=icon + " " + label, text_color="#94A3B8", font=("Inter", 10, "bold")).pack(side="left")
            
            # Value
            ctk.CTkLabel(card, text=val, text_color="#1E293B", font=("Inter", 24, "bold")).pack(anchor="w", padx=20)

    def _create_schedule(self, parent):
        container = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        container.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        container.pack_propagate(False)
        
        # Header
        head = ctk.CTkFrame(container, fg_color="transparent")
        head.pack(fill="x", padx=25, pady=20)
        ctk.CTkLabel(head, text="ACADEMIC SCHEDULE TODAY", font=("Inter", 11, "bold"), text_color="#64748B").pack(side="left")
        ctk.CTkLabel(head, text="SEMESTER PLAN", font=("Inter", 11, "bold"), text_color="#6366F1").pack(side="right")
        
        # Items
        items = [
            ("Python Programming Language", "08:45 AM - 09:20 AM", "B307", "IN SESSION", "#F3E8FF", "#7C3AED"),
            ("Mathematical Methods for ML", "12:10 PM - 14:50 AM", "F305", "UPCOMING", "#F3F4F6", "#94A3B8"),
            ("Software Technology", "15:00 PM - 17:15 AM", "C109", "UPCOMING", "#F3F4F6", "#94A3B8"),
        ]
        
        for title, time, room, status, badge_bg, badge_fg in items:
            row = ctk.CTkFrame(container, fg_color="transparent", height=70)
            row.pack(fill="x", padx=20, pady=5)
            
            # Icon Box
            icon_box = ctk.CTkFrame(row, width=45, height=45, fg_color="white", border_width=1, border_color="#E2E8F0", corner_radius=10)
            icon_box.pack(side="left")
            ctk.CTkLabel(icon_box, text="DS", font=("Inter", 8), text_color="gray").place(relx=0.5, rely=0.3, anchor="center")
            ctk.CTkLabel(icon_box, text=title[0:2].upper(), font=("Inter", 10, "bold"), text_color="black").place(relx=0.5, rely=0.7, anchor="center")
            
            # Info
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", padx=15)
            ctk.CTkLabel(info, text=title, font=("Inter", 12, "bold"), text_color="#1E293B").pack(anchor="w")
            ctk.CTkLabel(info, text=f"🕒 {time}   📍 {room}", font=("Inter", 10), text_color="#64748B").pack(anchor="w")

            # Status Badge
            ctk.CTkLabel(row, text=status, fg_color=badge_bg, text_color=badge_fg, font=("Inter", 9, "bold"), corner_radius=10, width=90, height=25).pack(side="right")

    def _create_verification_log(self, parent):
        container = ctk.CTkFrame(parent, fg_color="#0F172A", corner_radius=15) # Dark bg
        container.grid(row=0, column=1, sticky="nsew")
        container.pack_propagate(False)
        
        # Header
        ctk.CTkLabel(container, text="VERIFICATION LOG", font=("Inter", 12, "bold"), text_color="#22C55E").pack(anchor="w", padx=25, pady=25)
        
        # Log items (Simulated timeline)
        logs = [
            ("Probability and Statistics", "Present", "YESTERDAY, 15:46 PM", "#22C55E"), # Green bar
            ("Computer Architecture", "Late", "YESTERDAY, 10:20 AM", "#F59E0B"), # Orange bar
            ("Data Structures", "Absent", "1 JAN, 12:30 PM", "#EF4444"), # Red
            ("Databases", "Present", "1 JAN, 9:55 AM", "#22C55E"),
        ]
        
        for title, status, time, color in logs:
            row = ctk.CTkFrame(container, fg_color="transparent")
            row.pack(fill="x", padx=25, pady=8)
            
            # Bar indicator
            ctk.CTkFrame(row, width=3, height=35, fg_color=color).pack(side="left")
            
            content = ctk.CTkFrame(row, fg_color="transparent")
            content.pack(side="left", padx=10, fill="x", expand=True)
            
            # Top line
            top = ctk.CTkFrame(content, fg_color="transparent")
            top.pack(fill="x")
            ctk.CTkLabel(top, text=title, font=("Inter", 11, "bold"), text_color="white").pack(side="left")
            ctk.CTkLabel(top, text=time, font=("Inter", 9), text_color="#64748B").pack(side="right")
            
            # Bottom line
            ctk.CTkLabel(content, text=f"Status: {status}", font=("Inter", 10), text_color="#94A3B8").pack(anchor="w")

        # Download button
        ctk.CTkButton(
            container, 
            text="DOWNLOAD FULL TRANSCRIPT",
            font=("Inter", 10, "bold"),
            fg_color="transparent",
            border_width=1,
            border_color="#334155",
            hover_color="#1E293B",
            height=36,
            corner_radius=18
        ).pack(side="bottom", pady=30)
