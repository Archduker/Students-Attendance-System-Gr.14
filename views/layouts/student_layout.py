import customtkinter as ctk
from typing import Callable, Optional
from views.styles.theme import COLORS, FONTS, RADIUS

class StudentLayout(ctk.CTkFrame):
    """
    Main layout for Student Pages.
    Includes:
    - Left Sidebar (Navigation)
    - Top Header (Search, Profile)
    - Main Content Area
    """
    def __init__(self, master, current_path="dashboard", on_navigate: Optional[Callable] = None, user=None):
        super().__init__(master, fg_color="#F3F4F6") # Light gray bg for content
        self.pack(expand=True, fill="both")
        
        self.current_path = current_path
        self.on_navigate = on_navigate
        self.user = user

        # Structure: Sidebar (Left) + Main Content (Right)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_sidebar()
        self._create_main_area()

    
    def set_active_page(self, page_key: str):
        """Update active page and refresh menu."""
        # Ensure clean key comparison
        self.current_path = page_key.strip()
        print(f"DEBUG: Navigation -> {self.current_path}") # Debug print
        self._refresh_menu_buttons()
        # Force redraw to ensure visual update immediately
        self.update_idletasks()

    def _create_sidebar(self):
        """Builds the distinct dark blue sidebar"""
        self.sidebar_frame = ctk.CTkFrame(
            self,
            fg_color="#0F172A", # Dark Navy
            width=260,
            corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False) # Fixed width
        
        # 1. App Logo
        self.logo_frm = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.logo_frm.pack(fill="x", padx=20, pady=30)
        
        ctk.CTkLabel(
            self.logo_frm, 
            text="🛡️", 
            font=("Arial", 24),
            text_color="#6366f1"
        ).pack(side="left")
        
        logo_text = ctk.CTkFrame(self.logo_frm, fg_color="transparent")
        logo_text.pack(side="left", padx=10)
        
        ctk.CTkLabel(logo_text, text="UNIATTEND", font=("Inter", 16, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(logo_text, text="INSTITUTIONAL", font=("Inter", 9, "bold"), text_color="#38BDF8").pack(anchor="w")

        # 2. Menu Section
        ctk.CTkLabel(self.sidebar_frame, text="MAIN MENU", text_color="#64748B", font=("Inter", 10, "bold"), anchor="w").pack(fill="x", padx=25, pady=(20, 10))
        
        # Menu Items Definition
        self.menu_items = [
            ("Dashboard", "dashboard", "88"),
            ("Submit Attendance", "submit_attendance", "📅"),
            ("History", "history", "🕒"),
            ("Profile", "profile", "👤")
        ]
        
        # Container for menu buttons
        self.menu_buttons_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.menu_buttons_container.pack(fill="x", padx=0, pady=0)
        
        self._refresh_menu_buttons()

        # 3. Bottom Status
        self.bottom_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", padx=20, pady=30)
        
        # Status Card
        status_card = ctk.CTkFrame(self.bottom_frame, fg_color="#1E293B", corner_radius=15)
        status_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(status_card, text="STATUS", text_color="#64748B", font=("Inter", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 0))
        ctk.CTkLabel(status_card, text="● SYSTEM LIVE", text_color="#22C55E", font=("Inter", 11, "bold")).pack(anchor="w", padx=15, pady=(2, 10))

        # Sign Out
        signout_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Sign Out",
            fg_color="transparent",
            text_color="#94A3B8",
            hover_color="#1E293B",
            anchor="w",
            font=("Inter", 12),
            command=lambda: self.on_navigate("logout") if self.on_navigate else None
        )
        signout_btn.pack(fill="x")
        
        # Report Bug (Bottom of sidebar)
        bug_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Report Bug 🐛",
            fg_color="#334155",
            text_color="#F8FAFC",
            hover_color="#475569",
            anchor="center",
            font=("Inter", 11, "bold"),
            height=32,
            corner_radius=16,
            command=self._open_bug_tracker
        )
        bug_btn.pack(fill="x", pady=(15, 0))

    def _open_bug_tracker(self):
        import webbrowser
        webbrowser.open("http://localhost:8989")

    def _refresh_menu_buttons(self):
        """Refresh menu buttons to update active state."""
        # Clear existing buttons
        for widget in self.menu_buttons_container.winfo_children():
            widget.destroy()
            
        for label, key, icon in self.menu_items:
            self._add_menu_item(label, key, icon)

    def _add_menu_item(self, label, key, icon):
        # Comparison with safe strip and lowercase handling if needed (though keys are lowercase here)
        active = (self.current_path == key)
        
        bg_color = "#1E293B" if active else "transparent" # Highlight active
        text_color = "#38BDF8" if active else "#94A3B8"
        font_weight = "bold" if active else "normal"
        
        btn = ctk.CTkButton(
            self.menu_buttons_container,
            text=f"  {icon}   {label}",
            anchor="w",
            height=45,
            fg_color=bg_color,
            text_color=text_color,
            font=("Inter", 12, font_weight),
            hover_color="#1E293B",
            corner_radius=10,
            command=lambda k=key: self.on_navigate(k) if self.on_navigate else None
        )
             
        btn.pack(fill="x", padx=15, pady=4)

    def _create_main_area(self):
        """Top Header + Content Area"""
        self.main_frame = ctk.CTkFrame(self, fg_color="#F3F4F6", corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        # 1. Header
        self.header = ctk.CTkFrame(self.main_frame, fg_color="white", height=70, corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        # Search Bar
        search_frm = ctk.CTkFrame(self.header, fg_color="#F3F4F6", height=40, width=400, corner_radius=20)
        search_frm.pack(side="left", padx=30, pady=15)
        search_frm.pack_propagate(False)
        ctk.CTkLabel(search_frm, text="🔍", font=("Arial", 14), text_color="gray").pack(side="left", padx=(15, 5))
        ctk.CTkEntry(search_frm, placeholder_text="Search...", border_width=0, fg_color="transparent", height=30).pack(side="left", fill="x", expand=True)

        # Profile / Notifs
        user_area = ctk.CTkFrame(self.header, fg_color="transparent")
        user_area.pack(side="right", padx=30)
        
        ctk.CTkLabel(user_area, text="🔔", font=("Arial", 16), text_color="gray").pack(side="left", padx=15)
        
        # User Info
        info_frm = ctk.CTkFrame(user_area, fg_color="transparent")
        info_frm.pack(side="left", padx=10)
        
        # Dynamic User Data
        display_name = self.user.full_name if self.user else "Student"
        display_role = self.user.role.value if self.user and hasattr(self.user, 'role') else "Student"
        
        ctk.CTkLabel(info_frm, text=display_name, font=("Inter", 12, "bold"), text_color="black").pack(anchor="e")
        ctk.CTkLabel(info_frm, text=display_role, font=("Inter", 10), text_color="#6366F1").pack(anchor="e")
        
        # Avatar
        ctk.CTkLabel(user_area, text="TN", width=35, height=35, fg_color="#FEF3C7", text_color="#D97706", font=("Inter", 12, "bold"), corner_radius=17).pack(side="left", padx=(10, 0))

        # 2. Content Container (Scrollable or Static)
        # We'll use a frame where child pages can pack themselves
        self.content_area = ctk.CTkFrame(self.main_frame, fg_color="#F3F4F6")
        self.content_area.pack(expand=True, fill="both", padx=30, pady=30)

