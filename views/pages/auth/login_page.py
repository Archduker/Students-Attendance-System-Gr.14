"""
Login Page - Trang đăng nhập
============================

Trang đăng nhập với:
- Username/Password input với validation
- Remember Me checkbox
- Forgot Password link
- Error message display
- Kết nối với AuthController
"""

import customtkinter as ctk
from typing import Optional, Callable

from views.styles.theme import COLORS, FONTS, SPACING, RADIUS


class LoginPage(ctk.CTkFrame):
    """
    Trang đăng nhập.
    
    Example:
        >>> login_page = LoginPage(root, auth_controller, on_login_success)
    """
    
    def __init__(
        self, 
        master, 
        auth_controller=None,
        on_login_success: Optional[Callable] = None,
        on_forgot_password: Optional[Callable] = None
    ):
        """
        Khởi tạo LoginPage.
        
        Args:
            master: Parent widget
            auth_controller: AuthController instance
            on_login_success: Callback khi login thành công
            on_forgot_password: Callback khi click Forgot Password
        """
        super().__init__(master, fg_color="transparent")
        self.pack(expand=True, fill="both")
        
        self.auth_controller = auth_controller
        self.on_login_success = on_login_success
        self.on_forgot_password = on_forgot_password
        
        self._create_ui()
    
    def _create_ui(self):
        """Tạo UI components."""
        # Center container
        self.center_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS.get("bg_dark", "#1F2937"),
            corner_radius=RADIUS["lg"]
        )
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Title
        self.title_label = ctk.CTkLabel(
            self.center_frame,
            text="🎓 Student Attendance System",
            font=(FONTS["family"], FONTS["size_2xl"], "bold"),
            text_color=COLORS.get("primary", "#3B82F6")
        )
        self.title_label.pack(pady=(SPACING["xl"], SPACING["sm"]))
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.center_frame,
            text="Đăng nhập để tiếp tục",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS.get("text_secondary", "#6B7280")
        )
        self.subtitle_label.pack(pady=(0, SPACING["lg"]))
        
        # Form container
        self.form_frame = ctk.CTkFrame(
            self.center_frame,
            fg_color="transparent"
        )
        self.form_frame.pack(padx=SPACING["xl"], pady=SPACING["md"])
        
        # Username label
        self.username_label = ctk.CTkLabel(
            self.form_frame,
            text="Tên đăng nhập",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS.get("text_secondary", "#6B7280"),
            anchor="w"
        )
        self.username_label.pack(fill="x", pady=(0, SPACING["xs"]))
        
        # Username entry
        self.username_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Nhập username...",
            width=300,
            height=40,
            corner_radius=RADIUS["md"],
            font=(FONTS["family"], FONTS["size_base"])
        )
        self.username_entry.pack(pady=(0, SPACING["md"]))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Password label
        self.password_label = ctk.CTkLabel(
            self.form_frame,
            text="Mật khẩu",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS.get("text_secondary", "#6B7280"),
            anchor="w"
        )
        self.password_label.pack(fill="x", pady=(0, SPACING["xs"]))
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Nhập password...",
            show="•",
            width=300,
            height=40,
            corner_radius=RADIUS["md"],
            font=(FONTS["family"], FONTS["size_base"])
        )
        self.password_entry.pack(pady=(0, SPACING["md"]))
        self.password_entry.bind("<Return>", lambda e: self._handle_login())
        
        # Options row (Remember me + Forgot password)
        self.options_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )
        self.options_frame.pack(fill="x", pady=(0, SPACING["md"]))
        
        # Remember me checkbox
        self.remember_var = ctk.BooleanVar(value=False)
        self.remember_checkbox = ctk.CTkCheckBox(
            self.options_frame,
            text="Ghi nhớ đăng nhập",
            variable=self.remember_var,
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS.get("text_secondary", "#6B7280"),
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=4
        )
        self.remember_checkbox.pack(side="left")
        
        # Forgot password link
        self.forgot_btn = ctk.CTkButton(
            self.options_frame,
            text="Quên mật khẩu?",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS.get("primary", "#3B82F6"),
            fg_color="transparent",
            hover_color=COLORS.get("bg_tertiary", "#374151"),
            width=100,
            height=24,
            command=self._handle_forgot_password
        )
        self.forgot_btn.pack(side="right")
        
        # Error message label
        self.error_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS.get("error", "#EF4444"),
            wraplength=280
        )
        self.error_label.pack(pady=(0, SPACING["sm"]))
        
        # Login button
        self.login_btn = ctk.CTkButton(
            self.form_frame,
            text="Đăng nhập",
            font=(FONTS["family"], FONTS["size_base"], "bold"),
            fg_color=COLORS.get("primary", "#3B82F6"),
            hover_color=COLORS.get("primary_hover", "#2563EB"),
            width=300,
            height=44,
            corner_radius=RADIUS["md"],
            command=self._handle_login
        )
        self.login_btn.pack(pady=(SPACING["sm"], SPACING["xl"]))
        
        # Footer
        self.footer_label = ctk.CTkLabel(
            self.center_frame,
            text="© 2024 Group 14 - Student Attendance System",
            font=(FONTS["family"], FONTS["size_xs"]),
            text_color=COLORS.get("text_tertiary", "#9CA3AF")
        )
        self.footer_label.pack(pady=(0, SPACING["lg"]))
        
        # Focus on username entry
        self.username_entry.focus()
    
    def _validate_form(self) -> tuple[bool, str]:
        """
        Validate form inputs.
        
        Returns:
            Tuple (is_valid, error_message)
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username:
            return False, "Vui lòng nhập tên đăng nhập"
        
        if not password:
            return False, "Vui lòng nhập mật khẩu"
        
        if len(username) < 3:
            return False, "Tên đăng nhập phải có ít nhất 3 ký tự"
        
        return True, ""
    
    def _show_error(self, message: str):
        """Hiển thị error message."""
        self.error_label.configure(text=message)
    
    def _clear_error(self):
        """Xóa error message."""
        self.error_label.configure(text="")
    
    def _set_loading(self, loading: bool):
        """Set trạng thái loading."""
        if loading:
            self.login_btn.configure(text="Đang đăng nhập...", state="disabled")
        else:
            self.login_btn.configure(text="Đăng nhập", state="normal")
    
    def _handle_login(self):
        """Xử lý đăng nhập."""
        self._clear_error()
        
        # Validate form
        is_valid, error = self._validate_form()
        if not is_valid:
            self._show_error(error)
            return
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        remember = self.remember_var.get()
        
        # Nếu không có controller, hiển thị thông báo
        if not self.auth_controller:
            self._show_error("AuthController chưa được kết nối")
            print(f"[DEBUG] Login attempt: {username} / {'*' * len(password)}")
            print(f"[DEBUG] Remember me: {remember}")
            return
        
        # Set loading state
        self._set_loading(True)
        
        try:
            # Gọi auth controller
            result = self.auth_controller.handle_login(username, password)
            
            if result["success"]:
                print(f"✅ Login success: {result['user'].full_name} ({result['role']})")
                
                # Callback on success
                if self.on_login_success:
                    self.on_login_success(result["user"], remember)
            else:
                self._show_error(result.get("error", "Đăng nhập thất bại"))
        
        except Exception as e:
            self._show_error(f"Lỗi hệ thống: {str(e)}")
        
        finally:
            self._set_loading(False)
    
    def _handle_forgot_password(self):
        """Xử lý click Forgot Password."""
        if self.on_forgot_password:
            self.on_forgot_password()
        else:
            # Navigate to reset password page
            print("[DEBUG] Forgot password clicked - no handler assigned")
            self._show_error("Tính năng đang phát triển")
