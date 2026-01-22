"""
Class Management Page - Quản lý lớp học
========================================

Page quản lý classes:
- Hiển thị danh sách classes
- CRUD operations
- Gán teacher
- Quản lý students
"""

import customtkinter as ctk
from typing import List, Optional, Dict, Any
from tkinter import messagebox


class ClassManagementPage(ctk.CTkFrame):
    """
    Class Management Page - Quản lý lớp học.
    
    Features:
        - List all classes
        - Search and filter classes
        - Create/Edit/Delete classes
        - Assign teacher to class
        - Add/remove students
        - View class details
        
    Example:
        >>> page = ClassManagementPage(parent, admin_controller)
        >>> page.pack(fill="both", expand=True)
    """
    
    def __init__(
        self, 
        parent, 
        admin_controller,
        **kwargs
    ):
        """
        Khởi tạo Class Management Page.
        
        Args:
            parent: Parent widget
            admin_controller: AdminController instance
        """
        super().__init__(parent, **kwargs)
        
        self.admin_controller = admin_controller
        self.classes_data: List[Dict[str, Any]] = []
        self.filtered_classes: List[Dict[str, Any]] = []
        self.selected_class: Optional[Dict[str, Any]] = None
        
        # Filter state
        self.search_query = ""
        
        self._init_ui()
        self._load_classes()
    
    def _init_ui(self):
        """Khởi tạo UI components."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header with search and actions
        self._create_header()
        
        # Class list
        self._create_class_list()
        
        # Action buttons
        self._create_action_buttons()
    
    def _create_header(self):
        """Tạo header với search."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📚 Class Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Search bar
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search by class ID, name, subject...",
            height=35
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        
        # Add class button
        add_btn = ctk.CTkButton(
            search_frame,
            text="➕ Add Class",
            width=120,
            height=35,
            command=self._on_add_class
        )
        add_btn.grid(row=0, column=1)
    
    def _create_class_list(self):
        """Tạo class list table."""
        list_frame = ctk.CTkFrame(self, corner_radius=10)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)
        
        # Table header
        header = ctk.CTkFrame(list_frame, fg_color="gray25", height=40)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        header.grid_propagate(False)
        
        headers = ["Class ID", "Class Name", "Subject", "Teacher", "Students"]
        for i, text in enumerate(headers):
            label = ctk.CTkLabel(
                header,
                text=text,
                font=ctk.CTkFont(size=13, weight="bold")
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="w")
        
        # Scrollable class list
        self.class_list_frame = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="transparent"
        )
        self.class_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.class_list_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
    
    def _create_action_buttons(self):
        """Tạo action buttons."""
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Edit button
        self.edit_btn = ctk.CTkButton(
            action_frame,
            text="✏️ Edit Selected",
            width=140,
            command=self._on_edit_class,
            state="disabled"
        )
        self.edit_btn.pack(side="left", padx=(0, 10))
        
        # Manage Students button
        self.students_btn = ctk.CTkButton(
            action_frame,
            text="👥 Manage Students",
            width=160,
            command=self._on_manage_students,
            state="disabled"
        )
        self.students_btn.pack(side="left", padx=(0, 10))
        
        # Delete button
        self.delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ Delete Selected",
            width=140,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=self._on_delete_class,
            state="disabled"
        )
        self.delete_btn.pack(side="left")
        
        # Info label
        self.info_label = ctk.CTkLabel(
            action_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.info_label.pack(side="right")
    
    def _load_classes(self):
        """Load danh sách classes từ controller."""
        try:
            result = self.admin_controller.get_all_classes()
            
            if result.get("success"):
                self.classes_data = result.get("classes", [])
                self.filtered_classes = self.classes_data.copy()
                self._update_class_list()
            else:
                self._show_error(result.get("error", "Failed to load classes"))
                
        except Exception as e:
            self._show_error(f"Error loading classes: {str(e)}")
    
    def _update_class_list(self):
        """Update class list display."""
        # Clear existing items
        for widget in self.class_list_frame.winfo_children():
            widget.destroy()
        
        # Add class rows
        for idx, class_data in enumerate(self.filtered_classes):
            self._create_class_row(idx, class_data)
        
        # Update info label
        total = len(self.classes_data)
        filtered = len(self.filtered_classes)
        self.info_label.configure(
            text=f"Showing {filtered} of {total} classes"
        )
    
    def _create_class_row(self, idx: int, class_data: Dict[str, Any]):
        """
        Tạo một row trong class list.
        
        Args:
            idx: Row index
            class_data: Class data
        """
        # Alternating row colors
        bg_color = "gray20" if idx % 2 == 0 else "transparent"
        
        row_frame = ctk.CTkFrame(
            self.class_list_frame,
            fg_color=bg_color,
            height=50
        )
        row_frame.grid(row=idx, column=0, sticky="ew", pady=1)
        row_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        row_frame.grid_propagate(False)
        
        # Make row clickable
        row_frame.bind("<Button-1>", lambda e, c=class_data: self._on_class_select(c))
        
        # Columns
        student_count = len(class_data.get("student_codes", []))
        columns = [
            class_data.get("class_id", ""),
            class_data.get("class_name", ""),
            class_data.get("subject_code", ""),
            class_data.get("teacher_code", "") or "Not assigned",
            f"{student_count} students"
        ]
        
        for i, text in enumerate(columns):
            label = ctk.CTkLabel(
                row_frame,
                text=text,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="w")
            label.bind("<Button-1>", lambda e, c=class_data: self._on_class_select(c))
    
    def _on_search_change(self, event):
        """Handle search input change."""
        self.search_query = self.search_entry.get().lower()
        self._apply_filters()
    
    def _apply_filters(self):
        """Apply search filter."""
        self.filtered_classes = []
        
        for class_data in self.classes_data:
            # Search filter
            if self.search_query:
                searchable = f"{class_data.get('class_id', '')} {class_data.get('class_name', '')} {class_data.get('subject_code', '')}".lower()
                if self.search_query not in searchable:
                    continue
            
            self.filtered_classes.append(class_data)
        
        self._update_class_list()
    
    def _on_class_select(self, class_data: Dict[str, Any]):
        """
        Handle class selection.
        
        Args:
            class_data: Selected class data
        """
        self.selected_class = class_data
        
        # Enable action buttons
        self.edit_btn.configure(state="normal")
        self.students_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")
    
    def _on_add_class(self):
        """Handle add class button."""
        # Import here to avoid circular import
        from .class_dialog import ClassDialog
        
        dialog = ClassDialog(
            self,
            self.admin_controller,
            mode="create"
        )
        self.wait_window(dialog)
        
        # Refresh list if class was added
        if hasattr(dialog, 'success') and dialog.success:
            self._load_classes()
    
    def _on_edit_class(self):
        """Handle edit class button."""
        if not self.selected_class:
            return
        
        # Import here to avoid circular import
        from .class_dialog import ClassDialog
        
        dialog = ClassDialog(
            self,
            self.admin_controller,
            mode="edit",
            class_data=self.selected_class
        )
        self.wait_window(dialog)
        
        # Refresh list if class was updated
        if hasattr(dialog, 'success') and dialog.success:
            self._load_classes()
            self.selected_class = None
    
    def _on_manage_students(self):
        """Handle manage students button."""
        if not self.selected_class:
            return
        
        # TODO: Implement student management dialog
        messagebox.showinfo(
            "Manage Students",
            f"Student management for class '{self.selected_class.get('class_name')}'\n\n"
            "This feature will be implemented in the next phase."
        )
    
    def _on_delete_class(self):
        """Handle delete class button."""
        if not self.selected_class:
            return
        
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete class '{self.selected_class.get('class_id')}'?\n\n"
            "This action cannot be undone."
        )
        
        if not result:
            return
        
        # Delete class
        try:
            delete_result = self.admin_controller.delete_class(
                self.selected_class.get("class_id")
            )
            
            if delete_result.get("success"):
                messagebox.showinfo("Success", "Class deleted successfully")
                self._load_classes()
                self.selected_class = None
                
                # Disable action buttons
                self.edit_btn.configure(state="disabled")
                self.students_btn.configure(state="disabled")
                self.delete_btn.configure(state="disabled")
            else:
                self._show_error(delete_result.get("error", "Failed to delete class"))
                
        except Exception as e:
            self._show_error(f"Error deleting class: {str(e)}")
    
    def _show_error(self, message: str):
        """
        Hiển thị error message.
        
        Args:
            message: Error message
        """
        messagebox.showerror("Error", message)
    
    def refresh(self):
        """Public method để refresh class list."""
        self._load_classes()
