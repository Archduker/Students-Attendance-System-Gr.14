"""
Student Profile Page
===================

Trang profile của Student, tương tự Teacher profile.
"""

import customtkinter as ctk
from typing import Optional
from core.models import Student

class ProfilePage(ctk.CTkFrame):
    """
    Page hồ sơ cá nhân Student.
    Design tương tự Teacher profile.
    """
    
    def __init__(self, parent, on_navigate=None, user=None):
        super().__init__(parent, fg_color="transparent")
        self.pack(expand=True, fill="both")
        
        self.user = user
        
        # Grid layout: Main (Left) + Sidebar (Right)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._setup_ui()
    
    def _setup_ui(self):
        # --- Left Column ---
        self.left_col = ctk.CTkFrame(self, fg_color="transparent")
        self.left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        self._create_profile_header(self.left_col)
        self._create_personal_info(self.left_col)
        self._create_security_prefs(self.left_col)
        
        # --- Right Column ---
        self.right_col = ctk.CTkFrame(self, fg_color="transparent")
        self.right_col.grid(row=0, column=1, sticky="n")
        
        self._create_quick_settings(self.right_col)
        self._create_support_card(self.right_col)
    
    def _create_profile_header(self, parent):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=20, border_width=1, border_color="#E2E8F0")
        card.pack(fill="x", pady=(0, 20))
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(padx=30, pady=30, fill="x")
        
        # Avatar (Large)
        if self.user and self.user.full_name:
            initials = "".join([word[0].upper() for word in self.user.full_name.split()[:2]])
        else:
            initials = "ST"  # Student default
            
        avatar = ctk.CTkLabel(
            content, text=initials, width=80, height=80, corner_radius=40,
            fg_color="#FEF3C7", text_color="#D97706", font=("Inter", 24, "bold") # Yellow/Orange
        )
        avatar.pack(side="left", padx=(0, 20))
        
        # Info
        info = ctk.CTkFrame(content, fg_color="transparent")
        info.pack(side="left")
        
        name = self.user.full_name if self.user else "Student"
        ctk.CTkLabel(info, text=name, font=("Inter", 20, "bold"), text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(info, text="STUDENT - Data Science & AI", font=("Inter", 12), text_color="#64748B").pack(anchor="w")
        
        # Tags
        tags = ctk.CTkFrame(info, fg_color="transparent")
        tags.pack(anchor="w", pady=(10, 0))
        
        self._create_tag(tags, "VERIFIED USER", "#DBEAFE", "#2563EB") # Blue
        self._create_tag(tags, "ACTIVE SESSION", "#DCFCE7", "#16A34A") # Green
    
    def _create_tag(self, parent, text, bg, fg):
        lbl = ctk.CTkLabel(
            parent, text=text, text_color=fg, fg_color=bg,
            font=("Inter", 10, "bold"), corner_radius=5, width=90, height=24
        )
        lbl.pack(side="left", padx=(0, 10))
    
    def _create_personal_info(self, parent):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        card.pack(fill="x", pady=10)
        
        # Header
        ctk.CTkLabel(card, text="Personal Information", font=("Inter", 12, "bold"), text_color="#0F172A").pack(anchor="w", padx=20, pady=20)
        
        # Grid for fields
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=20, pady=(0, 20))
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        
        # Use dynamic user data
        name = self.user.full_name if self.user else "Student"
        email = self.user.email if self.user else "student@ut.edu.vn"
        
        self._add_field(grid, 0, 0, "FULL NAME", name, "👤")
        self._add_field(grid, 0, 1, "EMAIL ADDRESS", email, "✉️")
        self._add_field(grid, 1, 0, "DEPARTMENT", "Data Science & AI", "🏢")
        self._add_field(grid, 1, 1, "PRIMARY ROLE", "Student", "🛡️")
        
        # Update Link
        link = ctk.CTkLabel(card, text="Update Information ✏️", font=("Inter", 12, "underline"), text_color="#3B82F6", cursor="hand2")
        link.pack(anchor="w", padx=20, pady=(0, 20))
    
    def _add_field(self, parent, row, col, label, value, icon):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=row, column=col, sticky="w", pady=10)
        
        ctk.CTkLabel(f, text=f"{icon} {label}", font=("Inter", 10, "bold"), text_color="#94A3B8").pack(anchor="w")
        ctk.CTkLabel(f, text=value, font=("Inter", 12, "bold"), text_color="#0F172A").pack(anchor="w")
    
    def _create_security_prefs(self, parent):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(card, text="Security & Preferences", font=("Inter", 12, "bold"), text_color="#0F172A").pack(anchor="w", padx=20, pady=20)
        
        # Change Password
        item1 = ctk.CTkFrame(card, fg_color="transparent")
        item1.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(item1, text="🔑", font=("Arial", 16)).pack(side="left", padx=(0, 10))
        
        text1 = ctk.CTkFrame(item1, fg_color="transparent")
        text1.pack(side="left")
        ctk.CTkLabel(text1, text="Change Password", font=("Inter", 12, "bold"), text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(text1, text="Last changed 3 months ago", font=("Inter", 10), text_color="#94A3B8").pack(anchor="w")
        
        ctk.CTkLabel(item1, text="✏️", font=("Arial", 12), text_color="#94A3B8").pack(side="right")
        
        # 2FA
        item2 = ctk.CTkFrame(card, fg_color="transparent")
        item2.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(item2, text="🛡️", font=("Arial", 16)).pack(side="left", padx=(0, 10))
        
        text2 = ctk.CTkFrame(item2, fg_color="transparent")
        text2.pack(side="left")
        ctk.CTkLabel(text2, text="Two-Factor Auth", font=("Inter", 12, "bold"), text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(text2, text="Enabled for extra security", font=("Inter", 10), text_color="#94A3B8").pack(anchor="w")
        
        switch = ctk.CTkSwitch(item2, text="", onvalue=True, offvalue=False, button_color="#10B981")
        switch.select()
        switch.pack(side="right")
    
    def _create_quick_settings(self, parent):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(card, text="Quick Settings", font=("Inter", 12, "bold"), text_color="#0F172A").pack(anchor="w", padx=20, pady=20)
        
        # Push Notif
        item1 = ctk.CTkFrame(card, fg_color="transparent")
        item1.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(item1, text="🔔 Push Notification", font=("Inter", 11), text_color="#64748B").pack(side="left")
        
        switch = ctk.CTkSwitch(item1, text="", command=None, button_color="#3B82F6")
        switch.select()
        switch.pack(side="right")
        
        # Language
        item2 = ctk.CTkFrame(card, fg_color="transparent")
        item2.pack(fill="x", padx=20, pady=(15, 20))
        ctk.CTkLabel(item2, text="🌐 App Language", font=("Inter", 11), text_color="#64748B").pack(side="left")
        
        ctk.CTkLabel(item2, text="English (US) ⌄", font=("Inter", 11), text_color="#94A3B8").pack(side="right")
    
    def _create_support_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color="#3B82F6", corner_radius=15) # Blue background
        card.pack(fill="x", pady=0)
        
        ctk.CTkLabel(card, text="Need Support?", font=("Inter", 12, "bold"), text_color="white").pack(anchor="w", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            card, 
            text="Having issues with your account or attendance tracking? Our help desk is available 24/7", 
            font=("Inter", 10), 
            text_color="#DBEAFE", # Light Blue
            wraplength=200,
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        btn = ctk.CTkButton(
            card, text="Contact Support", fg_color="white", text_color="#2563EB",
            font=("Inter", 11, "bold"), height=35
        )
        btn.pack(fill="x", padx=20, pady=(0, 20))
