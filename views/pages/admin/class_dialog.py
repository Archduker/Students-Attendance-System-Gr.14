"""
Class Dialog - Create/Edit Class Dialog
=======================================

Dialog để tạo mới hoặc chỉnh sửa class:
- Input validation
- Teacher assignment
- Student management
"""

import customtkinter as ctk
from typing import Optional, Dict, Any, List
from tkinter import messagebox


class ClassDialog(ctk.CTkToplevel):
    """
    Dialog tạo mới hoặc chỉnh sửa class.
    
    Modes:
        - create: Tạo class mới
        - edit: Chỉnh sửa class hiện có
        
    Features:
        - Input fields: class_id, class_name, subject_code
        - Teacher selection
        - Student list management
        - Validation
        - Save/Cancel actions
        
    Example:
        >>> dialog = ClassDialog(parent, admin_controller, mode="create")
        >>> parent.wait_window(dialog)
        >>> if dialog.success:
        ...     print("Class created successfully")
    """
    
    def __init__(
        self,
        parent,
        admin_controller,
        mode: str = "create",
        class_data: Optional[Dict[str, Any]] = None
    ):
        """
        Khởi tạo Class Dialog.
        
        Args:
            parent: Parent widget
            admin_controller: AdminController instance
            mode: "create" hoặc "edit"
            class_data: Class data (nếu mode = "edit")
        """
        super().__init__(parent)
        
        self.admin_controller = admin_controller
        self.mode = mode
        self.class_data = class_data or {}
        self.success = False
        
        # Available teachers list
        self.teachers = []
        
        # Configure dialog
        self.title("Add New Class" if mode == "create" else "Edit Class")
        self.geometry("500x550")
        self.resizable(False, False)
        
        # Center dialog
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (550 // 2)
        self.geometry(f"500x550+{x}+{y}")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self._load_teachers()
        self._init_ui()
        
        if mode == "edit":
            self._populate_fields()
    
    def _load_teachers(self):
        """Load danh sách teachers."""
        try:
            result = self.admin_controller.get_teachers()
            if result.get("success"):
                self.teachers = result.get("teachers", [])
        except Exception as e:
            print(f"Warning: Could not load teachers: {e}")
            self.teachers = []
    
    def _init_ui(self):
        """Khởi tạo UI components."""
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title_text = "Create New Class" if self.mode == "create" else "Edit Class"
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
        
        # Class ID
        self._create_field(
            form_frame,
            "Class ID",
            "class_id_entry",
            "e.g., CS101-2024",
            row=0
        )
        
        # Class Name
        self._create_field(
            form_frame,
            "Class Name",
            "class_name_entry",
            "e.g., Introduction to Programming",
            row=1
        )
        
        # Subject Code
        self._create_field(
            form_frame,
            "Subject Code",
            "subject_code_entry",
            "e.g., CS101",
            row=2
        )
        
        # Teacher selection
        label = ctk.CTkLabel(
            form_frame,
            text="Assigned Teacher",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label.grid(row=6, column=0, sticky="w", pady=(15, 5))
        
        # Prepare teacher options
        teacher_options = ["Not assigned"]
        teacher_map = {"Not assigned": None}
        
        for teacher in self.teachers:
            display_name = f"{teacher.get('teacher_code', '')} - {teacher.get('full_name', '')}"
            teacher_options.append(display_name)
            teacher_map[display_name] = teacher.get("teacher_code")
        
        self.teacher_map = teacher_map
        
        self.teacher_var = ctk.StringVar(value="Not assigned")
        self.teacher_menu = ctk.CTkOptionMenu(
            form_frame,
            values=teacher_options,
            variable=self.teacher_var,
            width=440,
            height=35
        )
        self.teacher_menu.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        
        # Student count info (read-only in edit mode)
        if self.mode == "edit":
            student_count = len(self.class_data.get("student_codes", []))
            info_label = ctk.CTkLabel(
                form_frame,
                text=f"💡 Current students: {student_count}",
                font=ctk.CTkFont(size=11),
                text_color="gray"
            )
            info_label.grid(row=8, column=0, sticky="w", pady=(10, 0))
    
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
        save_text = "Create Class" if self.mode == "create" else "Update Class"
        save_btn = ctk.CTkButton(
            btn_frame,
            text=save_text,
            width=200,
            height=40,
            command=self._on_save
        )
        save_btn.pack(side="right")
    
    def _populate_fields(self):
        """Populate fields với class data (edit mode)."""
        self.class_id_entry.insert(0, self.class_data.get("class_id", ""))
        self.class_name_entry.insert(0, self.class_data.get("class_name", ""))
        self.subject_code_entry.insert(0, self.class_data.get("subject_code", ""))
        
        # Set teacher if assigned
        teacher_code = self.class_data.get("teacher_code")
        if teacher_code:
            # Find teacher in map
            for display_name, code in self.teacher_map.items():
                if code == teacher_code:
                    self.teacher_var.set(display_name)
                    break
        
        # Disable class_id in edit mode
        self.class_id_entry.configure(state="disabled")
    
    def _validate_inputs(self) -> tuple[bool, str]:
        """
        Validate input fields.
        
        Returns:
            Tuple (is_valid, error_message)
        """
        class_id = self.class_id_entry.get().strip()
        class_name = self.class_name_entry.get().strip()
        subject_code = self.subject_code_entry.get().strip()
        
        if not class_id:
            return False, "Class ID is required"
        
        if not class_name:
            return False, "Class name is required"
        
        if not subject_code:
            return False, "Subject code is required"
        
        return True, ""
    
    def _on_save(self):
        """Handle save button."""
        # Validate inputs
        is_valid, error_msg = self._validate_inputs()
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        # Collect form data
        class_info = {
            "class_id": self.class_id_entry.get().strip(),
            "class_name": self.class_name_entry.get().strip(),
            "subject_code": self.subject_code_entry.get().strip(),
            "teacher_code": self.teacher_map.get(self.teacher_var.get())
        }
        
        # Preserve student codes in edit mode
        if self.mode == "edit":
            class_info["student_codes"] = self.class_data.get("student_codes", [])
        
        try:
            if self.mode == "create":
                result = self.admin_controller.create_class(class_info)
            else:
                result = self.admin_controller.update_class(class_info)
            
            if result.get("success"):
                self.success = True
                
                # Show success message
                action = "created" if self.mode == "create" else "updated"
                messagebox.showinfo("Success", f"Class {action} successfully!")
                
                self.destroy()
            else:
                messagebox.showerror("Error", result.get("error", "Operation failed"))
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _on_cancel(self):
        """Handle cancel button."""
        self.destroy()
