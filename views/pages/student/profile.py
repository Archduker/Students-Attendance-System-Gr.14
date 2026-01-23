"""
Profile Page - Student profile editing
======================================

Cho phép sinh viên:
- Xem thông tin cá nhân
- Cập nhật thông tin
- Đổi mật khẩu
"""

import customtkinter as ctk
from typing import Optional, Dict, Any
from tkinter import messagebox

from views.styles.theme import COLORS, FONTS, SPACING, RADIUS
from controllers import StudentController, AuthController


class ProfilePage(ctk.CTkFrame):
    """
    Page để sinh viên xem và chỉnh sửa profile.
    
    Features:
    - View student info
    - Edit profile (name, email, class)
    - Change password
    """
    
    def __init__(
        self,
        parent,
        student_controller: StudentController,
        auth_controller: AuthController,
        student_code: str,
        **kwargs
    ):
        """
        Khởi tạo Profile Page.
        
        Args:
            parent: Parent widget
            student_controller: StudentController instance
            auth_controller: AuthController instance
            student_code: Mã sinh viên
        """
        super().__init__(parent, **kwargs)
        
        self.student_controller = student_controller
        self.auth_controller = auth_controller
        self.student_code = student_code
        self.student_info = None
        
        self._setup_ui()
        self._load_profile()
    
    def _setup_ui(self):
        """Thiết lập UI components."""
        self.configure(fg_color=COLORS["bg_secondary"])
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["lg"])
        
        # Header
        self._create_header(main_container)
        
        # Content với scroll
        scroll = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, pady=(SPACING["md"], 0))
        
        # Profile info section
        self.profile_section = ctk.CTkFrame(
            scroll,
            fg_color=COLORS["bg_primary"],
            corner_radius=RADIUS["lg"]
        )
        self.profile_section.pack(fill="x", pady=(0, SPACING["md"]))
        
        # Change password section
        self.password_section = ctk.CTkFrame(
            scroll,
            fg_color=COLORS["bg_primary"],
            corner_radius=RADIUS["lg"]
        )
        self.password_section.pack(fill="x")
        
        self._create_profile_form()
        self._create_password_form()
    
    def _create_header(self, parent):
        """Tạo header section."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACING["lg"]))
        
        # Title
        title = ctk.CTkLabel(
            header,
            text="👤 Thông tin cá nhân",
            font=(FONTS["family"], FONTS["size_3xl"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title.pack(side="left")
    
    def _create_profile_form(self):
        """Tạo form chỉnh sửa profile."""
        content = ctk.CTkFrame(self.profile_section, fg_color="transparent")
        content.pack(fill="x", padx=SPACING["lg"], pady=SPACING["lg"])
        
        # Section title
        title = ctk.CTkLabel(
            content,
            text="📝 Thông tin sinh viên",
            font=(FONTS["family"], FONTS["size_xl"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]))
        
        # Student code (readonly)
        code_label = ctk.CTkLabel(
            content,
            text="Mã sinh viên:",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_secondary"]
        )
        code_label.pack(anchor="w", pady=(0, SPACING["xs"]))
        
        self.code_display = ctk.CTkLabel(
            content,
            text=self.student_code,
            font=(FONTS["family"], FONTS["size_lg"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        self.code_display.pack(anchor="w", pady=(0, SPACING["md"]))
        
        # Full name
        name_label = ctk.CTkLabel(
            content,
            text="Họ và tên:",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_secondary"]
        )
        name_label.pack(anchor="w", pady=(0, SPACING["xs"]))
        
        self.name_entry = ctk.CTkEntry(
            content,
            height=40,
            corner_radius=RADIUS["md"],
            placeholder_text="Nhập họ tên..."
        )
        self.name_entry.pack(fill="x", pady=(0, SPACING["md"]))
        
        # Email
        email_label = ctk.CTkLabel(
            content,
            text="Email:",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_secondary"]
        )
        email_label.pack(anchor="w", pady=(0, SPACING["xs"]))
        
        self.email_entry = ctk.CTkEntry(
            content,
            height=40,
            corner_radius=RADIUS["md"],
            placeholder_text="email@example.com"
        )
        self.email_entry.pack(fill="x", pady=(0, SPACING["md"]))
        
        # Class name
        class_label = ctk.CTkLabel(
            content,
            text="Lớp:",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_secondary"]
        )
        class_label.pack(anchor="w", pady=(0, SPACING["xs"]))
        
        self.class_entry = ctk.CTkEntry(
            content,
            height=40,
            corner_radius=RADIUS["md"],
            placeholder_text="Nhập lớp..."
        )
        self.class_entry.pack(fill="x", pady=(0, SPACING["lg"]))
        
        # Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Lưu thay đổi",
            width=150,
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["success"],
            hover_color=COLORS["success"],
            command=self._save_profile
        )
        save_btn.pack(side="left", padx=(0, SPACING["sm"]))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="↩️ Hủy",
            width=100,
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["secondary"],
            hover_color=COLORS["secondary_hover"],
            command=self._load_profile
        )
        cancel_btn.pack(side="left")
        
        # Message label
        self.profile_message = ctk.CTkLabel(
            content,
            text="",
            font=(FONTS["family"], FONTS["size_sm"])
        )
        self.profile_message.pack(pady=(SPACING["sm"], 0))
    
    def _create_password_form(self):
        """Tạo form đổi mật khẩu."""
        content = ctk.CTkFrame(self.password_section, fg_color="transparent")
        content.pack(fill="x", padx=SPACING["lg"], pady=SPACING["lg"])
        
        # Section title
        title = ctk.CTkLabel(
            content,
            text="🔒 Đổi mật khẩu",
            font=(FONTS["family"], FONTS["size_xl"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]))
        
        # Old password
        old_label = ctk.CTkLabel(
            content,
            text="Mật khẩu cũ:",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_secondary"]
        )
        old_label.pack(anchor="w", pady=(0, SPACING["xs"]))
        
        self.old_password_entry = ctk.CTkEntry(
            content,
            height=40,
            corner_radius=RADIUS["md"],
            placeholder_text="Nhập mật khẩu cũ...",
            show="•"
        )
        self.old_password_entry.pack(fill="x", pady=(0, SPACING["md"]))
        
        # New password
        new_label = ctk.CTkLabel(
            content,
            text="Mật khẩu mới:",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_secondary"]
        )
        new_label.pack(anchor="w", pady=(0, SPACING["xs"]))
        
        self.new_password_entry = ctk.CTkEntry(
            content,
            height=40,
            corner_radius=RADIUS["md"],
            placeholder_text="Nhập mật khẩu mới...",
            show="•"
        )
        self.new_password_entry.pack(fill="x", pady=(0, SPACING["md"]))
        
        # Confirm password
        confirm_label = ctk.CTkLabel(
            content,
            text="Xác nhận mật khẩu:",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_secondary"]
        )
        confirm_label.pack(anchor="w", pady=(0, SPACING["xs"]))
        
        self.confirm_password_entry = ctk.CTkEntry(
            content,
            height=40,
            corner_radius=RADIUS["md"],
            placeholder_text="Nhập lại mật khẩu mới...",
            show="•"
        )
        self.confirm_password_entry.pack(fill="x", pady=(0, SPACING["lg"]))
        
        # Change password button
        change_btn = ctk.CTkButton(
            content,
            text="🔑 Đổi mật khẩu",
            width=150,
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["warning"],
            hover_color=COLORS["warning"],
            command=self._change_password
        )
        change_btn.pack(anchor="w")
        
        # Message label
        self.password_message = ctk.CTkLabel(
            content,
            text="",
            font=(FONTS["family"], FONTS["size_sm"])
        )
        self.password_message.pack(pady=(SPACING["sm"], 0))
    
    def _load_profile(self):
        """Load profile data."""
        result = self.student_controller.handle_get_student_info(self.student_code)
        
        if result["success"]:
            self.student_info = result["data"]
            
            # Fill form
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, self.student_info.get("full_name", ""))
            
            self.email_entry.delete(0, "end")
            self.email_entry.insert(0, self.student_info.get("email", ""))
            
            self.class_entry.delete(0, "end")
            self.class_entry.insert(0, self.student_info.get("class_name", ""))
        else:
            self._show_profile_message(
                result.get("error", "Không thể tải thông tin"),
                "error"
            )
    
    def _save_profile(self):
        """Lưu thay đổi profile."""
        profile_data = {
            "full_name": self.name_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "class_name": self.class_entry.get().strip()
        }
        
        result = self.student_controller.handle_update_profile(
            self.student_code,
            profile_data
        )
        
        if result["success"]:
            self._show_profile_message(result["message"], "success")
        else:
            self._show_profile_message(result["message"], "error")
    
    def _change_password(self):
        """Đổi mật khẩu."""
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        result = self.auth_controller.handle_change_password(
            old_password,
            new_password,
            confirm_password
        )
        
        if result["success"]:
            self._show_password_message(result["message"], "success")
            # Clear password fields
            self.old_password_entry.delete(0, "end")
            self.new_password_entry.delete(0, "end")
            self.confirm_password_entry.delete(0, "end")
        else:
            self._show_password_message(result["message"], "error")
    
    def _show_profile_message(self, message: str, msg_type: str):
        """Hiển thị message cho profile section."""
        if msg_type == "success":
            color = COLORS["success"]
            icon = "✅"
        else:
            color = COLORS["error"]
            icon = "❌"
        
        self.profile_message.configure(
            text=f"{icon} {message}",
            text_color=color
        )
    
    def _show_password_message(self, message: str, msg_type: str):
        """Hiển thị message cho password section."""
        if msg_type == "success":
            color = COLORS["success"]
            icon = "✅"
        else:
            color = COLORS["error"]
            icon = "❌"
        
        self.password_message.configure(
            text=f"{icon} {message}",
            text_color=color
        )
