"""
Admin Layout - Main Layout for Admin Interface
==============================================

Layout chính cho Admin với dark sidebar và header.
Matching UI from provided screenshots.
"""

import customtkinter as ctk
from typing import Callable, Optional

class AdminLayout(ctk.CTkFrame):
    """
    Main layout for Admin interface.
    Dark sidebar + light content area.
    """
    
    def __init__(self, parent, on_navigate: Callable, user):
        super().__init__(parent, fg_color="#F3F4F6")
        
        self.on_navigate = on_navigate
        self.user = user
        self.current_path = "dashboard"
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Sidebar fixed width
        self.grid_columnconfigure(1, weight=1)  # Content flexible
        
        # Pack to fill window
        self.pack(fill="both", expand=True)
        
        # Create UI components
        self._create_sidebar()
        self._create_main_area()
    
    def _create_sidebar(self):
        """Create dark sidebar with navigation."""
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            width=240, 
            fg_color="#1E293B",  # Dark blue-gray
            corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        
        # Logo/Branding
        logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=30)
        
        ctk.CTkLabel(
            logo_frame,
            text="🎓 UNIATTEND",
            font=("Inter", 16, "bold"),
            text_color="#A855F7"  # Purple
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            logo_frame,
            text="INSTITUTIONAL",
            font=("Inter", 10),
            text_color="#64748B"
        ).pack(anchor="w")
        
        # Main Menu Label
        ctk.CTkLabel(
            self.sidebar_frame,
            text="MAIN MENU",
            font=("Inter", 10, "bold"),
            text_color="#64748B"
        ).pack(fill="x", padx=20, pady=(20, 10), anchor="w")
        
        # Menu Items
        menu_items = [
            ("📊 Dashboard", "dashboard"),
            ("📄 System Reports", "reports"),
            ("👥 User Management", "user_management"),
            ("⚙️ System Config", "system_config"),
        ]
        
        for label, key in menu_items:
            self._create_menu_button(label, key)
        
        # Spacer
        ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", height=20).pack()
        
        # Status Section (at bottom)
        status_frame = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color="#334155",  # Lighter dark
            corner_radius=12,
            height=60
        )
        status_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        status_frame.pack_propagate(False)
        
        # STATUS label
        ctk.CTkLabel(
            status_frame,
            text="STATUS",
            font=("Inter", 9, "bold"),
            text_color="#64748B"
        ).pack(anchor="w", padx=15, pady=(10, 0))
        
        # SYSTEM LIVE with green dot
        live_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        live_frame.pack(anchor="w", padx=15, pady=(5, 10))
        
        ctk.CTkLabel(
            live_frame,
            text="● SYSTEM LIVE",
            font=("Inter", 11, "bold"),
            text_color="#22C55E"  # Green
        ).pack(side="left")
        
        # Sign Out
        sign_out_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="↩ Sign Out",
            font=("Inter", 11),
            fg_color="transparent",
            text_color="#94A3B8",
            hover_color="#334155",
            anchor="w",
            command=lambda: self.on_navigate("logout") if self.on_navigate else None
        )
        sign_out_btn.pack(side="bottom", fill="x", padx=20, pady=(0, 10))
    
    def _create_menu_button(self, label: str, key: str):
        """Create a menu button."""
        is_active = self.current_path == key
        
        btn = ctk.CTkButton(
            self.sidebar_frame,
            text=label,
            font=("Inter", 12, "bold" if is_active else "normal"),
            fg_color="#0EA5E9" if is_active else "transparent",  # Cyan for active
            text_color="white" if is_active else "#94A3B8",
            hover_color="#0284C7" if is_active else "#334155",
            anchor="w",
            height=45,
            corner_radius=10,
            command=lambda: self.on_navigate(key) if self.on_navigate else None
        )
        btn.pack(fill="x", padx=20, pady=3)
    
    def _create_main_area(self):
        """Create main content area with header."""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=1, sticky="nsew")
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header
        self._create_header(main_container)
        
        # Content Area
        self.content_area = ctk.CTkFrame(main_container, fg_color="transparent")
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
    
    def _create_header(self, parent):
        """Create header with search and user info."""
        header = ctk.CTkFrame(parent, fg_color="white", height=70, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", padx=30, pady=15)
        
        # Search bar (left)
        search_frame = ctk.CTkFrame(
            header_content,
            fg_color="#F1F5F9",
            corner_radius=20,
            height=40,
            width=400
        )
        search_frame.pack(side="left")
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=("Arial", 14),
            text_color="#94A3B8"
        ).pack(side="left", padx=(15, 5))
        
        ctk.CTkEntry(
            search_frame,
            placeholder_text="Search...",
            border_width=0,
            fg_color="transparent",
            font=("Inter", 12)
        ).pack(fill="both", expand=True, padx=(0, 15))
        
        # User info (right)
        user_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        user_frame.pack(side="right")
        
        # User name
        name_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
        name_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            name_frame,
            text=self.user.full_name if self.user else "Admin User",
            font=("Inter", 12, "bold"),
            text_color="#0F172A",
            anchor="e"
        ).pack(anchor="e")
        
        ctk.CTkLabel(
            name_frame,
            text="ADMIN",
            font=("Inter", 9, "bold"),
            text_color="#A855F7",  # Purple
            anchor="e"
        ).pack(anchor="e")
        
        # Avatar
        avatar = ctk.CTkLabel(
            user_frame,
            text="TT",
            width=45,
            height=45,
            corner_radius=22,
            fg_color="#A855F7",  # Purple
            text_color="white",
            font=("Inter", 14, "bold")
        )
        avatar.pack(side="left")
