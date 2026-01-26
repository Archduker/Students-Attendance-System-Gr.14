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
    
    def set_active_page(self, page_key: str):
        """Update active page and refresh menu."""
        self.current_path = page_key
        self._refresh_menu_buttons()

    def _create_sidebar(self):
        """Create dark sidebar with navigation."""
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            width=260, 
            fg_color="#0F172A",  # Darker Slate 900
            corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        
        # Logo/Branding
        logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_frame.pack(fill="x", padx=30, pady=(40, 30))
        
        # Logo Icon replacement (Text for now)
        ctk.CTkLabel(
            logo_frame,
            text="🎓",
            font=("Inter", 24),
            text_color="#A855F7"
        ).pack(side="left", padx=(0, 10))
        
        branding_text = ctk.CTkFrame(logo_frame, fg_color="transparent")
        branding_text.pack(side="left")
        
        ctk.CTkLabel(
            branding_text,
            text="UNIATTEND",
            font=("Inter", 20, "bold"),
            text_color="#A855F7"  # Purple
        ).pack(anchor="w", pady=(0, 0))
        
        ctk.CTkLabel(
            branding_text,
            text="INSTITUTIONAL",
            font=("Inter", 10, "bold"),
            text_color="#64748B"
        ).pack(anchor="w", pady=(0, 0))
        
        # Main Menu Label
        ctk.CTkLabel(
            self.sidebar_frame,
            text="MAIN MENU",
            font=("Inter", 11, "bold"),
            text_color="#64748B"
        ).pack(fill="x", padx=30, pady=(10, 15), anchor="w")
        
        # Menu Items
        self.menu_items = [
            ("📊 Dashboard", "dashboard"),
            ("📄 System Reports", "reports"),
            ("👥 User Management", "user_management"),
            ("📚 Class Management", "class_management"),
        ]
        
        # Container for menu buttons
        self.menu_buttons_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.menu_buttons_container.pack(fill="x", padx=15, pady=0)
        
        self._refresh_menu_buttons()
        
        # Spacer to push bottom elements down
        ctk.CTkFrame(self.sidebar_frame, fg_color="transparent").pack(fill="both", expand=True)
        
        # Status Section (at bottom)
        status_frame = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color="#1E293B",  # Lighter dark for status
            corner_radius=15,
            height=80
        )
        status_frame.pack(side="bottom", fill="x", padx=20, pady=(0, 30))
        status_frame.pack_propagate(False)
        
        # STATUS label
        ctk.CTkLabel(
            status_frame,
            text="STATUS",
            font=("Inter", 10, "bold"),
            text_color="#64748B"
        ).pack(anchor="w", padx=20, pady=(15, 0))
        
        # SYSTEM LIVE with green dot
        live_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        live_frame.pack(anchor="w", padx=20, pady=(5, 10))
        
        ctk.CTkLabel(
            live_frame,
            text="●",
            font=("Inter", 14),
            text_color="#22C55E"
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            live_frame,
            text="SYSTEM LIVE",
            font=("Inter", 12, "bold"),
            text_color="#22C55E"
        ).pack(side="left")
        
        # Sign Out button
        sign_out_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="↩ Sign Out",
            font=("Inter", 12),
            fg_color="transparent",
            text_color="#94A3B8",
            hover_color="#334155",
            anchor="w",
            height=40,
            command=lambda: self.on_navigate("logout") if self.on_navigate else None
        )
        sign_out_btn.pack(side="bottom", fill="x", padx=30, pady=(10, 10))

    def _refresh_menu_buttons(self):
        """Refresh menu buttons to update active state."""
        # Clear existing buttons
        for widget in self.menu_buttons_container.winfo_children():
            widget.destroy()
        
        # Recreate all buttons with current active state
        for label, key in self.menu_items:
            is_active = self.current_path == key
            
            # Common styling
            btn_fg = "#0EA5E9" if is_active else "transparent"  # Sky 500 for active
            text_color = "white" if is_active else "#94A3B8"
            hover_color = "#0284C7" if is_active else "#1E293B"
            font_weight = "bold" if is_active else "normal"
            
            btn = ctk.CTkButton(
                self.menu_buttons_container,
                text=label,
                font=("Inter", 13, font_weight),
                fg_color=btn_fg,
                text_color=text_color,
                hover_color=hover_color,
                anchor="w",
                height=50,
                corner_radius=10,
                command=lambda k=key: self.on_navigate(k) if self.on_navigate else None
            )
            btn.pack(fill="x", padx=0, pady=5)

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
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
    
    def _create_header(self, parent):
        """Create header with search and user info."""
        header = ctk.CTkFrame(parent, fg_color="white", height=80, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", padx=40, pady=20)
        
        # Search bar (left)
        search_frame = ctk.CTkFrame(
            header_content,
            fg_color="#F1F5F9",
            corner_radius=12,
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
        ).pack(side="left", padx=(15, 10))
        
        ctk.CTkEntry(
            search_frame,
            placeholder_text="Search anything...",
            border_width=0,
            fg_color="transparent",
            font=("Inter", 13),
            placeholder_text_color="#94A3B8",
            text_color="#1E293B"
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
            font=("Inter", 13, "bold"),
            text_color="#0F172A",
            anchor="e"
        ).pack(anchor="e")
        
        ctk.CTkLabel(
            name_frame,
            text="ADMINISTRATOR",
            font=("Inter", 10, "bold"),
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
            fg_color="#F3E8FF",  # Light Purple
            text_color="#A855F7",
            font=("Inter", 14, "bold")
        )
        avatar.pack(side="left")

