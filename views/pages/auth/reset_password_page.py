"""
Reset Password Page - Trang khôi phục mật khẩu
==============================================

Trang cho phép user nhập email để reset password.
"""

import customtkinter as ctk
from typing import Optional, Callable
import re

from views.styles.theme import COLORS, FONTS, SPACING, RADIUS


class ResetPasswordPage(ctk.CTkFrame):
    """
    Trang khôi phục mật khẩu.
    
    Example:
        >>> reset_page = ResetPasswordPage(root, auth_controller, on_back_to_login)
    """
    
    def __init__(
        self, 
        master, 
        auth_controller=None,
        on_back_to_login: Optional[Callable] = None
    ):
        """
        Khởi tạo ResetPasswordPage.
        
        Args:
            master: Parent widget
            auth_controller: AuthController instance
            on_back_to_login: Callback khi click Back to Login
        """
        super().__init__(master, fg_color="transparent")
        self.pack(expand=True, fill="both")
        
        self.auth_controller = auth_controller
        self.on_back_to_login = on_back_to_login
        
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
        
        # Back button
        self.back_btn = ctk.CTkButton(
            self.center_frame,
            text="← Quay lại",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS.get("text_secondary", "#6B7280"),
            fg_color="transparent",
            hover_color=COLORS.get("bg_tertiary", "#374151"),
            width=100,
            height=30,
            anchor="w",
            command=self._handle_back
        )
        self.back_btn.pack(anchor="w", padx=SPACING["md"], pady=(SPACING["md"], 0))
        
        # Icon
        self.icon_label = ctk.CTkLabel(
            self.center_frame,
            text="🔐",
            font=(FONTS["family"], 48)
        )
        self.icon_label.pack(pady=(SPACING["md"], SPACING["sm"]))
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.center_frame,
            text="Quên mật khẩu?",
            font=(FONTS["family"], FONTS["size_2xl"], "bold"),
            text_color=COLORS.get("text_primary", "#F9FAFB")
        )
        self.title_label.pack(pady=(0, SPACING["sm"]))
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.center_frame,
            text="Nhập email đã đăng ký để nhận mật khẩu mới",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS.get("text_secondary", "#6B7280"),
            wraplength=280
        )
        self.subtitle_label.pack(pady=(0, SPACING["lg"]))
        
        # Form container
        self.form_frame = ctk.CTkFrame(
            self.center_frame,
            fg_color="transparent"
        )
        self.form_frame.pack(padx=SPACING["xl"], pady=SPACING["md"])
        
        # Email label
        self.email_label = ctk.CTkLabel(
            self.form_frame,
            text="Email",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS.get("text_secondary", "#6B7280"),
            anchor="w"
        )
        self.email_label.pack(fill="x", pady=(0, SPACING["xs"]))
        
        # Email entry
        self.email_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Nhập email của bạn...",
            width=300,
            height=40,
            corner_radius=RADIUS["md"],
            font=(FONTS["family"], FONTS["size_base"])
        )
        self.email_entry.pack(pady=(0, SPACING["md"]))
        self.email_entry.bind("<Return>", lambda e: self._handle_reset())
        
        # Message label (for success/error)
        self.message_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=(FONTS["family"], FONTS["size_sm"]),
            wraplength=280
        )
        self.message_label.pack(pady=(0, SPACING["sm"]))
        
        # Reset button
        self.reset_btn = ctk.CTkButton(
            self.form_frame,
            text="Gửi yêu cầu",
            font=(FONTS["family"], FONTS["size_base"], "bold"),
            fg_color=COLORS.get("primary", "#3B82F6"),
            hover_color=COLORS.get("primary_hover", "#2563EB"),
            width=300,
            height=44,
            corner_radius=RADIUS["md"],
            command=self._handle_reset
        )
        self.reset_btn.pack(pady=(SPACING["sm"], SPACING["xl"]))
        
        # Footer
        self.footer_label = ctk.CTkLabel(
            self.center_frame,
            text="Mật khẩu mới sẽ được gửi qua email",
            font=(FONTS["family"], FONTS["size_xs"]),
            text_color=COLORS.get("text_tertiary", "#9CA3AF")
        )
        self.footer_label.pack(pady=(0, SPACING["lg"]))
        
        # Focus on email entry
        self.email_entry.focus()
    
    def _validate_email(self, email: str) -> tuple[bool, str]:
        """
        Validate email format.
        
        Args:
            email: Email string to validate
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if not email:
            return False, "Vui lòng nhập email"
        
        # Basic email regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Email không hợp lệ"
        
        return True, ""
    
    def _show_message(self, message: str, is_error: bool = True):
        """Hiển thị message."""
        color = COLORS.get("error", "#EF4444") if is_error else COLORS.get("success", "#10B981")
        self.message_label.configure(text=message, text_color=color)
    
    def _clear_message(self):
        """Xóa message."""
        self.message_label.configure(text="")
    
    def _set_loading(self, loading: bool):
        """Set trạng thái loading."""
        if loading:
            self.reset_btn.configure(text="Đang xử lý...", state="disabled")
        else:
            self.reset_btn.configure(text="Gửi yêu cầu", state="normal")
    
    def _handle_reset(self):
        """Xử lý reset password."""
        self._clear_message()
        
        email = self.email_entry.get().strip()
        
        # Validate email
        is_valid, error = self._validate_email(email)
        if not is_valid:
            self._show_message(error, is_error=True)
            return
        
        # Nếu không có controller
        if not self.auth_controller:
            self._show_message("AuthController chưa được kết nối", is_error=True)
            print(f"[DEBUG] Reset password for: {email}")
            return
        
        # Set loading
        self._set_loading(True)
        
        try:
            # Gọi auth controller
            result = self.auth_controller.handle_reset_password(email)
            
            if result["success"]:
                self._show_message(result.get("message", "Mật khẩu mới đã được gửi!"), is_error=False)
                self.email_entry.delete(0, "end")
            else:
                self._show_message(result.get("message", "Không thể reset mật khẩu"), is_error=True)
        
        except Exception as e:
            self._show_message(f"Lỗi hệ thống: {str(e)}", is_error=True)
        
        finally:
            self._set_loading(False)
    
    def _handle_back(self):
        """Xử lý quay lại trang login."""
        if self.on_back_to_login:
            self.on_back_to_login()
        else:
            print("[DEBUG] Back to login clicked - no handler assigned")
