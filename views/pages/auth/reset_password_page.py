import customtkinter as ctk
from typing import Optional, Callable
import re
from views.styles.theme import COLORS, FONTS, SPACING, RADIUS

class ResetPasswordPage(ctk.CTkFrame):
    """
    Trang Reset Password với thiết kế Split-Screen hiện đại.
    Design matches LoginPage pixel-perfectly.
    """
    
    def __init__(
        self, 
        master, 
        auth_controller=None,
        on_back_to_login: Optional[Callable] = None
    ):
        super().__init__(master, fg_color="white")
        self.pack(expand=True, fill="both")
        
        self.auth_controller = auth_controller
        self.on_back_to_login = on_back_to_login
        
        # Grid layout: 55% Left, 45% Right
        self.grid_columnconfigure(0, weight=11)
        self.grid_columnconfigure(1, weight=9)
        self.grid_rowconfigure(0, weight=1)

        self._create_left_panel()
        self._create_right_panel()

    def _create_left_panel(self):
        """Tạo panel bên trái (Dark Blue Theme) - Reused from LoginPage"""
        self.left_frame = ctk.CTkFrame(
            self,
            fg_color="#0F172A", # Dark Navy
            corner_radius=0
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Content Container
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

        # 3. Main Headline
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
        add_text(h1_line1, "Smart ", "#38BDF8")
        add_text(h1_line1, "and ", "white")
        add_text(h1_line1, "Secure", "#38BDF8") 

        ctk.CTkLabel(
            self.left_content,
            text="Attendance\nManagement System.",
            font=("Inter", 40, "bold"),
            text_color="white",
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=(0, 25))

        # 4. Description
        ctk.CTkLabel(
            self.left_content,
            text="Empowering the HCMC University of Transport with\ncutting-edge attendance tracking and real-time\nstudent insights.",
            font=("Inter", 14),
            text_color="#94A3B8",
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=(0, 60))

        # 5. Features
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

        # 6. Footer
        self.footer_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.footer_frame.pack(side="bottom", fill="x", padx=40, pady=30)
        
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
        """Tạo panel bên phải (Reset Form)"""
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
            text="Reset Access",
            text_color="#000000",
            font=("Inter", 36, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            self.form_container,
            text="Enter your institutional email to\nrecover access.",
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
            text_color="#9CA3AF",
            font=("Inter", 11, "bold")
        ).pack(anchor="w", pady=(0, 8))

        self.email_entry = ctk.CTkEntry(
            self.form_container,
            placeholder_text="", 
            font=("Inter", 14),
            height=48,
            fg_color="#F3F4F6", # Gray-100
            border_width=0,
            text_color="#111827",
            corner_radius=10
        )
        self.email_entry.pack(fill="x", pady=(0, 30))
        self.email_entry.configure(placeholder_text="name@ut.edu.vn")
        self.email_entry.bind("<Return>", lambda e: self._handle_reset())

        # 3. Action Button
        self.reset_btn = ctk.CTkButton(
            self.form_container,
            text="Request Reset >",
            font=("Inter", 14, "bold"),
            height=52,
            fg_color="#000000",
            text_color="white",
            hover_color="#333333",
            corner_radius=26,
            command=self._handle_reset
        )
        self.reset_btn.pack(fill="x", pady=(0, 20))
        
        # 4. Return Link
        self.back_btn = ctk.CTkButton(
            self.form_container,
            text="Return to Login",
            font=("Inter", 13, "bold"),
            text_color="#6B7280",
            fg_color="transparent",
            hover_color="#F3F4F6", 
            width=0,
            height=30,
            command=self._handle_back
        )
        self.back_btn.pack(pady=(0, 25))
        
        # Message Label
        self.message_label = ctk.CTkLabel(
            self.form_container,
            text="",
            text_color="#10B981", # Success Green default
            font=("Inter", 11),
            anchor="center",
            wraplength=300
        )
        self.message_label.pack(fill="x", pady=(0, 10))

        # 5. Institutional Access (Tabs) - Decorative but keeps UI consistent
        ctk.CTkLabel(
            self.form_container,
            text="INSTITUTIONAL ACCESS",
            text_color="#D1D5DB", 
            font=("Inter", 11, "bold"),
            anchor="center"
        ).pack(fill="x", pady=(0, 15))

        self.role_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.role_frame.pack(fill="x")
        self.role_frame.grid_columnconfigure(0, weight=1)
        self.role_frame.grid_columnconfigure(1, weight=1)
        self.role_frame.grid_columnconfigure(2, weight=1)

        role_icons = {"Student": "🎓", "Teacher": "🖥️", "Admin": "🛡️"}
        roles = ["Student", "Teacher", "Admin"]

        for i, label in enumerate(roles):
            btn = ctk.CTkButton(
                self.role_frame,
                text=f"{role_icons[label]}\n{label}",
                font=("Inter", 11, "bold"),
                fg_color="transparent", 
                text_color="#9CA3AF", 
                hover_color="#F3F4F6", # Just allow hover, no selection logic needed for reset really
                width=80,
                height=70,
                corner_radius=12,
                state="disabled" # Maybe disable them to indicate this is just reset page? Or keep enabled for consistency? Mockup shows "Student" selected. I'll make them visual only.
            )
            # Match style of "Student selected" from login
            if label == "Student":
                btn.configure(fg_color="#EFF6FF", text_color="#3B82F6", state="normal")
            
            btn.grid(row=0, column=i, sticky="ew", padx=5)

    def _validate_email(self, email: str) -> tuple[bool, str]:
        if not email:
            return False, "Vui lòng nhập email"
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Email không hợp lệ"
        return True, ""

    def _handle_reset(self):
        self.message_label.configure(text="")
        email = self.email_entry.get().strip()
        
        is_valid, error = self._validate_email(email)
        if not is_valid:
            self.message_label.configure(text=error, text_color="#EF4444")
            return

        self.reset_btn.configure(text="Processing...", state="disabled")
        self.after(500, lambda: self._process_reset(email))

    def _process_reset(self, email):
        if not self.auth_controller:
            self.message_label.configure(text="Auth Controller not connected", text_color="#EF4444")
        else:
            try:
                result = self.auth_controller.handle_reset_password(email)
                if result["success"]:
                    msg = result.get("message", "Password reset link sent to email!")
                    self.message_label.configure(text=msg, text_color="#10B981")
                else:
                    self.message_label.configure(text=result.get("message", "Failed to reset."), text_color="#EF4444")
            except Exception as e:
                self.message_label.configure(text=f"Error: {e}", text_color="#EF4444")
        
        self.reset_btn.configure(text="Request Reset >", state="normal")

    def _handle_back(self):
        if self.on_back_to_login:
            self.on_back_to_login()
