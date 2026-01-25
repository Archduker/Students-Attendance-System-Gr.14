import customtkinter as ctk
from typing import Optional, Callable
from views.styles.theme import COLORS, FONTS, SPACING, RADIUS

class LoginPage(ctk.CTkFrame):
    """
    Trang đăng nhập với thiết kế Split-Screen hiện đại.
    Modified: Pixel-perfect adjustments for fonts, sizing, and alignment to match mockup.
    """
    
    def __init__(
        self, 
        master, 
        auth_controller=None,
        on_login_success: Optional[Callable] = None,
        on_forgot_password: Optional[Callable] = None
    ):
        super().__init__(master, fg_color="white")
        self.pack(expand=True, fill="both")
        
        self.auth_controller = auth_controller
        self.on_login_success = on_login_success
        self.on_forgot_password = on_forgot_password
        
        # Grid layout: 55% Left, 45% Right to match visual balance
        self.grid_columnconfigure(0, weight=11)
        self.grid_columnconfigure(1, weight=9)
        self.grid_rowconfigure(0, weight=1)

        self._create_left_panel()
        self._create_right_panel()

    def _create_left_panel(self):
        """Tạo panel bên trái (Dark Blue Theme)"""
        self.left_frame = ctk.CTkFrame(
            self,
            fg_color="#0F172A", # Dark Navy
            corner_radius=0
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Content Container - centered vertically, with left padding
        self.left_content = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.left_content.place(relx=0.1, rely=0.5, anchor="w")

        # 1. Logo Section
        self.logo_frame = ctk.CTkFrame(self.left_content, fg_color="transparent")
        self.logo_frame.pack(anchor="w", pady=(0, 40))
        
        self.logo_icon = ctk.CTkLabel(
            self.logo_frame,
            text="🛡️", 
            font=("Arial", 28),
            text_color="#6366f1"
        )
        self.logo_icon.pack(side="left", padx=(0, 15))
        
        self.logo_text_frame = ctk.CTkFrame(self.logo_frame, fg_color="transparent")
        self.logo_text_frame.pack(side="left")
        
        ctk.CTkLabel(
            self.logo_text_frame,
            text="UNIATTEND",
            font=("Inter", 18, "bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            self.logo_text_frame,
            text="HCMC University of Transport",
            font=("Inter", 12),
            text_color="#94A3B8"
        ).pack(anchor="w")

        # 2. System Status Badge
        self.badge = ctk.CTkFrame(self.left_content, fg_color="#1E293B", corner_radius=20)
        self.badge.pack(anchor="w", pady=(0, 25))
        ctk.CTkLabel(
            self.badge,
            text="●   SYSTEM ONLINE • V3.5.0",
            font=("Inter", 10, "bold"),
            text_color="#22C55E",
            padx=15, 
            pady=5,
        ).pack()

        # 3. Main Headline (Multi-color workaround using stacked frames)
        # Line 1: "A <Smart> and <Secure>"
        h1_line1 = ctk.CTkFrame(self.left_content, fg_color="transparent")
        h1_line1.pack(anchor="w")
        
        def add_text(parent, text, color="white"):
            ctk.CTkLabel(
                parent, 
                text=text, 
                font=("Inter", 40, "bold"), 
                text_color=color,
                padx=0, pady=0
            ).pack(side="left")

        add_text(h1_line1, "A ")
        add_text(h1_line1, "Smart ", "#38BDF8") # Light Blue / Cyan
        add_text(h1_line1, "and ", "white")
        add_text(h1_line1, "Secure", "#38BDF8") 

        # Line 2 & 3
        ctk.CTkLabel(
            self.left_content,
            text="Attendance\nManagement System.",
            font=("Inter", 40, "bold"),
            text_color="white",
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=(0, 25))

        # 4. Marketing Description
        ctk.CTkLabel(
            self.left_content,
            text="Empowering the HCMC University of Transport with\ncutting-edge attendance tracking and real-time\nstudent insights.",
            font=("Inter", 14),
            text_color="#94A3B8",
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=(0, 60))

        # 5. Feature Chips
        self.features_frame = ctk.CTkFrame(self.left_content, fg_color="transparent")
        self.features_frame.pack(anchor="w", fill="x")

        features = [
            "Instant QR Verification",
            "Smart Analytics Dashboard",
            "Secure Identity Validation"
        ]
        
        for feat in features:
            f_frm = ctk.CTkFrame(self.features_frame, fg_color="transparent", border_width=1, border_color="#334155", corner_radius=30)
            f_frm.pack(side="left", padx=(0, 15), ipady=2)
            ctk.CTkLabel(
                f_frm, 
                text=feat, 
                text_color="#94A3B8", 
                font=("Inter", 11),
                padx=15,
                pady=6
            ).pack()

        # 6. Footer (Absolute positioning at bottom)
        self.footer_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.footer_frame.pack(side="bottom", fill="x", padx=40, pady=30)
        
        # Divider
        ctk.CTkFrame(self.footer_frame, fg_color="#334155", height=1).pack(fill="x", pady=(0, 15))
        
        links_frame = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        links_frame.pack(fill="x")
        
        for l in ["PRIVACY POLICY", "SECURITY AUDIT", "SUPPORT"]:
            ctk.CTkLabel(
                links_frame,
                text=l,
                text_color="#64748B",
                font=("Inter", 9, "bold")
            ).pack(side="left", padx=(0, 25))
            
        ctk.CTkLabel(
            links_frame,
            text="© 2026 UTH - IT Division",
            text_color="#64748B",
            font=("Inter", 9)
        ).pack(side="right")

    def _create_right_panel(self):
        """Tạo panel bên phải (Login Form)"""
        self.right_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=0
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        # Center container
        self.form_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.form_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7)

        # 1. Header Group
        ctk.CTkLabel(
            self.form_container,
            text="Login",
            text_color="#000000",
            font=("Inter", 36, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            self.form_container,
            text="Welcome back. Access your\nacademic portal below.",
            text_color="#6B7280",
            font=("Inter", 14),
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=(0, 35))

        # 2. Input Fields
        # Email
        ctk.CTkLabel(
            self.form_container,
            text="UNIVERSITY EMAIL",
            text_color="#9CA3AF", # Gray-400
            font=("Inter", 11, "bold")
        ).pack(anchor="w", pady=(0, 8))

        self.email_entry = ctk.CTkEntry(
            self.form_container,
            placeholder_text="", # No popup
            font=("Inter", 14),
            height=48,
            fg_color="#F3F4F6", # Gray-100
            border_width=0,
            text_color="#111827",
            corner_radius=10
        )
        self.email_entry.pack(fill="x", pady=(0, 20))
        # Adding simple placeholder manually
        self.email_entry.configure(placeholder_text="name@ut.edu.vn")

        # Password
        pwd_label_row = ctk.CTkFrame(self.form_container, fg_color="transparent")
        pwd_label_row.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(
            pwd_label_row,
            text="PASSWORD",
            text_color="#9CA3AF",
            font=("Inter", 11, "bold")
        ).pack(side="left")
        
        self.forgot_btn = ctk.CTkButton(
            pwd_label_row,
            text="Forgot Password?",
            font=("Inter", 11, "bold"),
            text_color="#3B82F6",
            fg_color="transparent",
            hover=False,
            width=0,
            command=self._handle_forgot_password
        )
        self.forgot_btn.pack(side="right")

        self.password_entry = ctk.CTkEntry(
            self.form_container,
            placeholder_text="••••••",
            show="•",
            font=("Inter", 14),
            height=48,
            fg_color="#F3F4F6",
            border_width=0,
            text_color="#111827",
        )
        self.password_entry.pack(fill="x", pady=(0, 15))

        # Remember Me Checkbox
        self.remember_var = ctk.BooleanVar(value=False)
        self.remember_cb = ctk.CTkCheckBox(
            self.form_container,
            text="Remember me",
            variable=self.remember_var,
            font=("Inter", 12),
            text_color="#6B7280",
            fg_color="#0F172A",
            checkbox_height=20,
            checkbox_width=20,
            hover_color="#334155",
            corner_radius=5
        )
        self.remember_cb.pack(anchor="w", pady=(0, 25))
        
        # Load saved session
        try:
            from config.session_config import load_session
            saved_session = load_session()
            if saved_session and saved_session.get("last_email"):
                self.email_entry.insert(0, saved_session["last_email"])
                if saved_session.get("remember"):
                    self.remember_var.set(True)
        except Exception:
            pass

        # 3. Action Button
        self.login_btn = ctk.CTkButton(
            self.form_container,
            text="Proceed to Dashboard  >",
            font=("Inter", 14, "bold"),
            height=52,
            fg_color="#000000",
            text_color="white",
            hover_color="#333333",
            corner_radius=26,
            command=self._handle_login
        )
        self.login_btn.pack(fill="x", pady=(0, 45))
        
        # Error Label
        self.error_label = ctk.CTkLabel(
            self.form_container,
            text="",
            text_color="#EF4444",
            font=("Inter", 11),
            anchor="w"
        )
        self.error_label.pack(fill="x", pady=(0, 10))

        # 4. Institutional Access (Tabs)
        ctk.CTkLabel(
            self.form_container,
            text="INSTITUTIONAL ACCESS",
            text_color="#D1D5DB", # Light gray
            font=("Inter", 11, "bold"),
            anchor="center"
        ).pack(fill="x", pady=(0, 15))

        self.role_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.role_frame.pack(fill="x")
        self.role_frame.grid_columnconfigure(0, weight=1)
        self.role_frame.grid_columnconfigure(1, weight=1)
        self.role_frame.grid_columnconfigure(2, weight=1)

        self.role_var = ctk.StringVar(value="STUDENT")
        self.role_buttons = {}

        roles = [
            ("Student", "STUDENT", "🎓"),
            ("Teacher", "TEACHER", "🖥️"),
            ("Admin", "ADMIN", "🛡️")
        ]

        for i, (label, value, icon) in enumerate(roles):
            # Container for each role to handle selection styling
            btn = ctk.CTkButton(
                self.role_frame,
                text=f"{icon}\n{label}",
                font=("Inter", 11, "bold"),
                fg_color="transparent",
                text_color="#9CA3AF" if value != "STUDENT" else "#3B82F6",
                hover_color="#F3F4F6",
                width=80,
                height=70,
                corner_radius=12,
                command=lambda v=value: self._select_role(v)
            )
            btn.grid(row=0, column=i, sticky="ew", padx=5)
            self.role_buttons[value] = btn
            
        # Initial visual state
        self._select_role("STUDENT")

    def _select_role(self, role_value):
        """Handle role selection visual state"""
        self.role_var.set(role_value)
        
        for val, btn in self.role_buttons.items():
            is_selected = (val == role_value)
            btn.configure(
                text_color="#3B82F6" if is_selected else "#9CA3AF",
                fg_color="#EFF6FF" if is_selected else "transparent",
                border_width=0
            )
        
        # Update placeholder if needed
        if role_value == "ADMIN":
            self.email_entry.configure(placeholder_text="admin@ut.edu.vn")
        else:
            self.email_entry.configure(placeholder_text="name@ut.edu.vn")

    def _handle_login(self):
        self.error_label.configure(text="")
        name = self.email_entry.get().strip()
        pwd = self.password_entry.get()
        
        if not name or not pwd:
            self.error_label.configure(text="Please enter valid credentials.")
            return
            
        self.login_btn.configure(text="Verifying...", state="disabled")
        self.after(500, lambda: self._process_login(name, pwd))
        
    def _process_login(self, email, password):
        if self.auth_controller:
            try:
                # Role Validation Rule
                selected_role = self.role_var.get()
                
                result = self.auth_controller.handle_login(email, password)
                if result.get("success"):
                    user = result["user"]
                    
                    # Validate role matches
                    if user.role.value != selected_role:
                        self.error_label.configure(
                            text=f"❌ Incorrect role! This account is {user.role.value}, not {selected_role}."
                        )
                        self.login_btn.configure(text="Proceed to Dashboard  >", state="normal")
                        return

                    # Save session
                    if self.remember_var.get():
                        try:
                            from config.session_config import save_session
                            save_session(email, True)
                        except:
                            pass
                            
                    if self.on_login_success:
                        self.on_login_success(user, self.remember_var.get())
                    return # Stop execution to avoid accessing destroyed widgets
                else:
                    self.error_label.configure(text=result.get("error", "Access Denied"))
            except Exception as e:
                try:
                    if hasattr(self, 'error_label') and self.error_label.winfo_exists():
                        self.error_label.configure(text=f"Error: {e}")
                except:
                    print(f"Login Error: {e}")
        
        # Only re-enable button if login failed or didn't proceed
        if self.winfo_exists():
            self.login_btn.configure(text="Proceed to Dashboard  >", state="normal")
            self.login_btn.configure(text="Proceed to Dashboard >", state="normal")

    def _handle_forgot_password(self):
        if self.on_forgot_password:
            self.on_forgot_password()
