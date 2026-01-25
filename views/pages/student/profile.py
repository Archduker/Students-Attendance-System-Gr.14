import customtkinter as ctk

class ProfilePage(ctk.CTkFrame):
    def __init__(self, master, on_navigate=None, user=None):
        super().__init__(master, fg_color="#F3F4F6")
        self.pack(expand=True, fill="both")
        
        self.user = user
        self.display_name = user.full_name if user else "Student"
        self.display_role = user.role.value if user and hasattr(user, 'role') else "Student"
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=3) # Left Col (Info)
        self.grid_columnconfigure(1, weight=2) # Right Col (Settings)
        
        # 1. Profile Header (Full Width)
        self._create_profile_header()
        
        # 2. Personal Info Card (Row 1 Col 0)
        self._create_personal_info(row=1, col=0)
        
        # 3. Security Card (Row 2 Col 0)
        self._create_security(row=2, col=0)
        
        # 4. Quick Settings (Row 1 Col 1)
        self._create_settings(row=1, col=1)
        
        # 5. Support Card (Row 2 Col 1)
        self._create_support(row=2, col=1)

    def _create_profile_header(self):
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=15, height=120)
        card.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        card.pack_propagate(False)
        
        # Avatar
        initials = "".join([n[0] for n in self.display_name.split()[:2]]).upper()
        avatar = ctk.CTkLabel(card, text=initials, width=80, height=80, fg_color="#FEF3C7", text_color="#D97706", font=("Inter", 24, "bold"), corner_radius=40)
        avatar.pack(side="left", padx=30)
        
        # Info
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left")
        ctk.CTkLabel(info, text=self.display_name, font=("Inter", 20, "bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(info, text=f"{self.display_role} - Data Science & AI", font=("Inter", 12), text_color="#64748B").pack(anchor="w", pady=(2, 10))
        
        # Tags
        tags = ctk.CTkFrame(info, fg_color="transparent")
        tags.pack(anchor="w")
        ctk.CTkLabel(tags, text="VERIFIED USER", fg_color="#DBEAFE", text_color="#2563EB", font=("Inter", 9, "bold"), corner_radius=5, padx=8, pady=2).pack(side="left")
        ctk.CTkLabel(tags, text="ACTIVE SESSION", fg_color="#DCFCE7", text_color="#166534", font=("Inter", 9, "bold"), corner_radius=5, padx=8, pady=2).pack(side="left", padx=10)

    def _create_personal_info(self, row, col):
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        card.grid(row=row, column=col, sticky="nsew", padx=(0, 20), pady=(0, 20))
        
        ctk.CTkLabel(card, text="Personal Information", font=("Inter", 13, "bold"), text_color="#1E293B").pack(anchor="w", padx=25, pady=20)
        
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=25, pady=(0, 25))
        
        email = self.user.email if self.user else "N/A"
        
        self._add_field(grid, 0, 0, "FULL NAME", self.display_name)
        self._add_field(grid, 0, 1, "EMAIL ADDRESS", email)
        self._add_field(grid, 1, 0, "DEPARTMENT", "Data Science & AI")
        self._add_field(grid, 1, 1, "PRIMARY ROLE", self.display_role)
        
        ctk.CTkButton(card, text="Update Information ✎", fg_color="transparent", text_color="#3B82F6", anchor="w", font=("Inter", 11), hover=False).pack(anchor="w", padx=20, pady=(0, 20))

    def _add_field(self, parent, r, c, label, val):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=r, column=c, sticky="ew", pady=10, padx=(0, 20))
        ctk.CTkLabel(f, text="👤 " + label if "NAME" in label else "📧 " + label if "EMAIL" in label else "🏢 " + label, font=("Inter", 10, "bold"), text_color="#94A3B8").pack(anchor="w")
        ctk.CTkLabel(f, text=val, font=("Inter", 12, "bold"), text_color="#1E293B").pack(anchor="w")

    def _create_security(self, row, col):
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        card.grid(row=row, column=col, sticky="nsew", padx=(0, 20))
        
        ctk.CTkLabel(card, text="Security & Preferences", font=("Inter", 13, "bold"), text_color="#1E293B").pack(anchor="w", padx=25, pady=20)
        
        # Change Password
        r1 = ctk.CTkFrame(card, fg_color="transparent")
        r1.pack(fill="x", padx=25, pady=10)
        ctk.CTkLabel(r1, text="Change Password", font=("Inter", 12, "bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(r1, text="Last changed 3 months ago", font=("Inter", 11), text_color="#94A3B8").pack(anchor="w")
        
        # 2FA
        r2 = ctk.CTkFrame(card, fg_color="transparent")
        r2.pack(fill="x", padx=25, pady=20)
        ctk.CTkLabel(r2, text="Two-Factor Auth", font=("Inter", 12, "bold"), text_color="#1E293B").pack(side="left")
        ctk.CTkSwitch(r2, text="").pack(side="right")

    def _create_settings(self, row, col):
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        card.grid(row=row, column=col, sticky="nsew", pady=(0, 20))
        
        ctk.CTkLabel(card, text="Quick Settings", font=("Inter", 13, "bold"), text_color="#1E293B").pack(anchor="w", padx=25, pady=20)
        
        r1 = ctk.CTkFrame(card, fg_color="transparent")
        r1.pack(fill="x", padx=25, pady=10)
        ctk.CTkLabel(r1, text="🔔 Push Notification", text_color="#64748B", font=("Inter", 12)).pack(side="left")
        ctk.CTkSwitch(r1, text="").pack(side="right")
        
        r2 = ctk.CTkFrame(card, fg_color="transparent")
        r2.pack(fill="x", padx=25, pady=20)
        ctk.CTkLabel(r2, text="🌐 App Language", text_color="#64748B", font=("Inter", 12)).pack(side="left")
        ctk.CTkLabel(r2, text="English (US) ⌄", text_color="#94A3B8", font=("Inter", 12)).pack(side="right")

    def _create_support(self, row, col):
        card = ctk.CTkFrame(self, fg_color="#3B82F6", corner_radius=15) # Blue bg
        card.grid(row=row, column=col, sticky="nsew")
        
        ctk.CTkLabel(card, text="Need Support?", font=("Inter", 13, "bold"), text_color="white").pack(anchor="w", padx=25, pady=(25, 10))
        ctk.CTkLabel(card, text="Having issues with your account or attendance\ntracking? Our help desk is available 24/7", font=("Inter", 10), text_color="#DBEAFE", justify="left", anchor="w").pack(anchor="w", padx=25)
        
        ctk.CTkButton(card, text="Contact Support", fg_color="white", text_color="#3B82F6", font=("Inter", 11, "bold")).pack(fill="x", padx=25, pady=25)
