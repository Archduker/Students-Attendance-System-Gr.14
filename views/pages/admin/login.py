"""
Admin Login Page
================

Login page cho admin module.
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Callable


class AdminLoginPage(ctk.CTkFrame):
    """
    Admin Login Page.
    
    Features:
        - Username/password input
        - Login validation
        - Remember me option
        - Callback on successful login
    """
    
    def __init__(
        self,
        parent,
        auth_controller,
        on_login_success: Optional[Callable] = None,
        **kwargs
    ):
        """
        Khởi tạo Admin Login Page.
        
        Args:
            parent: Parent widget
            auth_controller: AuthController instance
            on_login_success: Callback function khi login thành công
        """
        super().__init__(parent, **kwargs)
        
        self.auth_controller = auth_controller
        self.on_login_success = on_login_success
        
        self._init_ui()
    
    def _init_ui(self):
        """Khởi tạo UI components."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Center container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0)
        
        # Login card
        login_card = ctk.CTkFrame(container, width=450, height=550, corner_radius=15)
        login_card.pack(padx=40, pady=40)
        login_card.pack_propagate(False)
        
        # Logo/Icon
        icon_label = ctk.CTkLabel(
            login_card,
            text="🛡️",
            font=ctk.CTkFont(size=60)
        )
        icon_label.pack(pady=(40, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            login_card,
            text="Admin Login",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            login_card,
            text="Student Attendance System",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Form frame
        form_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        form_frame.pack(fill="x", padx=40)
        
        # Username label
        username_label = ctk.CTkLabel(
            form_frame,
            text="Username",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        username_label.pack(fill="x", pady=(0, 5))
        
        # Username entry
        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your username",
            height=45,
            font=ctk.CTkFont(size=13)
        )
        self.username_entry.pack(fill="x", pady=(0, 20))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Password label
        password_label = ctk.CTkLabel(
            form_frame,
            text="Password",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 5))
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your password",
            show="•",
            height=45,
            font=ctk.CTkFont(size=13)
        )
        self.password_entry.pack(fill="x", pady=(0, 15))
        self.password_entry.bind("<Return>", lambda e: self._on_login())
        
        # Remember me checkbox
        self.remember_var = ctk.BooleanVar(value=False)
        remember_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Remember me",
            variable=self.remember_var,
            font=ctk.CTkFont(size=12)
        )
        remember_checkbox.pack(anchor="w", pady=(0, 30))
        
        # Login button
        self.login_btn = ctk.CTkButton(
            form_frame,
            text="Login",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._on_login
        )
        self.login_btn.pack(fill="x", pady=(0, 15))
        
        # Error label (hidden by default)
        self.error_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#d32f2f"
        )
        self.error_label.pack(fill="x")
        
        # Footer info
        info_label = ctk.CTkLabel(
            login_card,
            text="Only admin users can access this panel",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_label.pack(side="bottom", pady=20)
        
        # Focus username by default
        self.username_entry.focus()
    
    def _on_login(self):
        """Handle login button click."""
        # Clear previous error
        self.error_label.configure(text="")
        
        # Get credentials
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validate input
        if not username:
            self._show_error("Please enter username")
            self.username_entry.focus()
            return
        
        if not password:
            self._show_error("Please enter password")
            self.password_entry.focus()
            return
        
        # Disable button during login
        self.login_btn.configure(state="disabled", text="Logging in...")
        self.update()
        
        try:
            # Call auth controller
            result = self.auth_controller.handle_login(username, password)
            
            if result.get("success"):
                user = result.get("user")
                role = result.get("role", "")
                
                # Check if user is admin
                if role.upper() != "ADMIN":
                    self._show_error("Access denied. Admin role required.")
                    self.login_btn.configure(state="normal", text="Login")
                    return
                
                # Login successful
                if self.on_login_success:
                    self.on_login_success(user)
            else:
                error = result.get("error", "Login failed")
                self._show_error(error)
                self.login_btn.configure(state="normal", text="Login")
                
        except Exception as e:
            self._show_error(f"Error: {str(e)}")
            self.login_btn.configure(state="normal", text="Login")
    
    def _show_error(self, message: str):
        """
        Hiển thị error message.
        
        Args:
            message: Error message
        """
        self.error_label.configure(text=f"⚠️ {message}")
    
    def clear_form(self):
        """Clear login form."""
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.error_label.configure(text="")
        self.login_btn.configure(state="normal", text="Login")
