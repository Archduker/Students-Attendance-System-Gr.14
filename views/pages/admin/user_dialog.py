"""
User Dialog - Create/Edit User Dialog
=====================================

Dialog để tạo mới hoặc chỉnh sửa user:
- Input validation
- Role selection
- Password generation
"""

import customtkinter as ctk
from typing import Optional, Dict, Any
from tkinter import messagebox

from core.enums import UserRole


class UserDialog(ctk.CTkToplevel):
    """
    Dialog tạo mới hoặc chỉnh sửa user.
    
    Modes:
        - create: Tạo user mới
        - edit: Chỉnh sửa user hiện có
        
    Features:
        - Input fields: username, full_name, email, role
        - Password generation (for new users)
        - Validation
        - Save/Cancel actions
        
    Example:
        >>> dialog = UserDialog(parent, admin_controller, mode="create")
        >>> parent.wait_window(dialog)
        >>> if dialog.success:
        ...     print("User created successfully")
    """
    
    def __init__(
        self,
        parent,
        admin_controller,
        mode: str = "create",
        user_data: Optional[Dict[str, Any]] = None
    ):
        """
        Khởi tạo User Dialog.
        
        Args:
            parent: Parent widget
            admin_controller: AdminController instance
            mode: "create" hoặc "edit"
            user_data: User data (nếu mode = "edit")
        """
        super().__init__(parent)
        
        self.admin_controller = admin_controller
        self.mode = mode
        self.user_data = user_data or {}
        self.success = False
        
        # Configure dialog
        self.title("Add New User" if mode == "create" else "Edit User")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Center dialog
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"500x600+{x}+{y}")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self._init_ui()
        
        if mode == "edit":
            self._populate_fields()
    
    def _init_ui(self):
        """Khởi tạo UI components."""
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title_text = "Create New User" if self.mode == "create" else "Edit User"
        title_label = ctk.CTkLabel(
            container,
            text=title_text,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Form fields
        self._create_form(container)
        
        # Buttons
        self._create_buttons(container)
    
    def _create_form(self, parent):
        """Tạo form fields."""
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="both", expand=True)
        
        # Username
        self._create_field(
            form_frame,
            "Username",
            "username_entry",
            "Enter username",
            row=0
        )
        
        # Full Name
        self._create_field(
            form_frame,
            "Full Name",
            "fullname_entry",
            "Enter full name",
            row=1
        )
        
        # Email
        self._create_field(
            form_frame,
            "Email",
            "email_entry",
            "Enter email address",
            row=2
        )
        
        # Role (dropdown)
        label = ctk.CTkLabel(
            form_frame,
            text="Role",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label.grid(row=3, column=0, sticky="w", pady=(15, 5))
        
        self.role_var = ctk.StringVar(
            value=self.user_data.get("role", "STUDENT")
        )
        self.role_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["ADMIN", "TEACHER", "STUDENT"],
            variable=self.role_var,
            width=440,
            height=35
        )
        self.role_menu.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        
        # Additional fields based on role
        self._create_role_specific_fields(form_frame)
        
        # Password section (only for create mode)
        if self.mode == "create":
            self._create_password_section(form_frame)
    
    def _create_field(
        self,
        parent,
        label_text: str,
        entry_name: str,
        placeholder: str,
        row: int
    ):
        """
        Tạo một form field.
        
        Args:
            parent: Parent widget
            label_text: Text cho label
            entry_name: Tên attribute cho entry
            placeholder: Placeholder text
            row: Grid row
        """
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label.grid(row=row*2, column=0, sticky="w", pady=(15, 5))
        
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            width=440,
            height=35
        )
        entry.grid(row=row*2+1, column=0, sticky="ew", pady=(0, 10))
        
        setattr(self, entry_name, entry)
    
    def _create_role_specific_fields(self, parent):
        """Tạo fields đặc thù cho từng role."""
        # Teacher Code (for teachers)
        label = ctk.CTkLabel(
            parent,
            text="Teacher Code (for Teachers)",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label.grid(row=10, column=0, sticky="w", pady=(15, 5))
        
        self.teacher_code_entry = ctk.CTkEntry(
            parent,
            placeholder_text="e.g., GV001 (optional)",
            width=440,
            height=35
        )
        self.teacher_code_entry.grid(row=11, column=0, sticky="ew", pady=(0, 10))
        
        # Student Code (for students)
        label = ctk.CTkLabel(
            parent,
            text="Student Code (for Students)",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label.grid(row=12, column=0, sticky="w", pady=(15, 5))
        
        self.student_code_entry = ctk.CTkEntry(
            parent,
            placeholder_text="e.g., SV001 (optional)",
            width=440,
            height=35
        )
        self.student_code_entry.grid(row=13, column=0, sticky="ew", pady=(0, 10))
    
    def _create_password_section(self, parent):
        """Tạo password section."""
        # Info label
        info_label = ctk.CTkLabel(
            parent,
            text="💡 A random password will be generated and shown after creation",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        info_label.grid(row=14, column=0, sticky="w", pady=(10, 0))
    
    def _create_buttons(self, parent):
        """Tạo action buttons."""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", pady=(20, 0))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=200,
            height=40,
            fg_color="gray40",
            hover_color="gray30",
            command=self._on_cancel
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        # Save button
        save_text = "Create User" if self.mode == "create" else "Update User"
        save_btn = ctk.CTkButton(
            btn_frame,
            text=save_text,
            width=200,
            height=40,
            command=self._on_save
        )
        save_btn.pack(side="right")
    
    def _populate_fields(self):
        """Populate fields với user data (edit mode)."""
        self.username_entry.insert(0, self.user_data.get("username", ""))
        self.fullname_entry.insert(0, self.user_data.get("full_name", ""))
        
        if self.user_data.get("email"):
            self.email_entry.insert(0, self.user_data.get("email", ""))
        
        # Disable username in edit mode
        self.username_entry.configure(state="disabled")
    
    def _validate_inputs(self) -> tuple[bool, str]:
        """
        Validate input fields.
        
        Returns:
            Tuple (is_valid, error_message)
        """
        username = self.username_entry.get().strip()
        full_name = self.fullname_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not username:
            return False, "Username is required"
        
        if not full_name:
            return False, "Full name is required"
        
        if email and "@" not in email:
            return False, "Invalid email format"
        
        if self.mode == "create" and len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        return True, ""
    
    def _on_save(self):
        """Handle save button."""
        # Validate inputs
        is_valid, error_msg = self._validate_inputs()
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        # Collect form data
        user_info = {
            "username": self.username_entry.get().strip(),
            "full_name": self.fullname_entry.get().strip(),
            "email": self.email_entry.get().strip() or None,
            "role": self.role_var.get()
        }
        
        # Add role-specific fields
        teacher_code = self.teacher_code_entry.get().strip()
        student_code = self.student_code_entry.get().strip()
        
        if teacher_code:
            user_info["teacher_code"] = teacher_code
        if student_code:
            user_info["student_code"] = student_code
        
        try:
            if self.mode == "create":
                result = self.admin_controller.create_user(user_info)
            else:
                user_info["user_id"] = self.user_data.get("user_id")
                result = self.admin_controller.update_user(user_info)
            
            if result.get("success"):
                self.success = True
                
                # Show success message
                if self.mode == "create" and result.get("password"):
                    messagebox.showinfo(
                        "Success",
                        f"User created successfully!\n\n"
                        f"Username: {user_info['username']}\n"
                        f"Password: {result.get('password')}\n\n"
                        f"Please save this password!"
                    )
                else:
                    messagebox.showinfo("Success", "User updated successfully!")
                
                self.destroy()
            else:
                messagebox.showerror("Error", result.get("error", "Operation failed"))
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _on_cancel(self):
        """Handle cancel button."""
        self.destroy()
