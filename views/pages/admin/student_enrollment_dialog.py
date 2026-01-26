"""
Student Enrollment Dialog - Manage Students in Class
====================================================

Dialog để quản lý danh sách sinh viên trong lớp:
- Hiển thị danh sách sinh viên hiện tại
- Thêm sinh viên vào lớp
- Xóa sinh viên khỏi lớp
"""

import customtkinter as ctk
from typing import Optional, Dict, Any, List
from tkinter import messagebox


class StudentEnrollmentDialog(ctk.CTkToplevel):
    """
    Dialog quản lý danh sách sinh viên trong lớp.
    
    Features:
        - Hiển thị sinh viên đã enrolled
        - Search và thêm sinh viên available
        - Xóa sinh viên khỏi lớp
        - Lưu thay đổi
        
    Example:
        >>> dialog = StudentEnrollmentDialog(parent, admin_controller, class_data)
        >>> parent.wait_window(dialog)
        >>> if dialog.success:
        ...     print("Students updated successfully")
    """
    
    def __init__(
        self,
        parent,
        admin_controller,
        class_data: Dict[str, Any]
    ):
        """
        Khởi tạo Student Enrollment Dialog.
        
        Args:
            parent: Parent widget
            admin_controller: AdminController instance
            class_data: Class data dict
        """
        super().__init__(parent)
        
        self.admin_controller = admin_controller
        self.class_data = class_data
        self.success = False
        
        # Get current students and all available students
        self.enrolled_students: List[Dict[str, Any]] = []
        self.available_students: List[Dict[str, Any]] = []
        
        # Configure dialog
        self.title(f"Manage Students - {class_data.get('class_name', '')}")
        self.geometry("900x600")
        self.resizable(False, False)
        
        # Center dialog
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"900x600+{x}+{y}")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self._load_students()
        self._init_ui()
    
    def _load_students(self):
        """Load danh sách sinh viên."""
        try:
            # Get all students
            result = self.admin_controller.get_all_users(role_filter="STUDENT")
            if result.get("success"):
                all_students = result.get("users", [])
                
                # Split into enrolled and available
                enrolled_codes = set(self.class_data.get("student_codes", []))
                
                for student in all_students:
                    student_code = student.get("student_code") or student.get("username")
                    if student_code in enrolled_codes:
                        self.enrolled_students.append(student)
                    else:
                        self.available_students.append(student)
        except Exception as e:
            print(f"Error loading students: {e}")
    
    def _init_ui(self):
        """Khởi tạo UI components."""
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text=f"📚 {self.class_data.get('class_name', 'Class')} - Student Enrollment",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Two-column layout
        columns_frame = ctk.CTkFrame(container, fg_color="transparent")
        columns_frame.pack(fill="both", expand=True)
        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_columnconfigure(1, weight=1)
        
        # Left column: Available students
        self._create_available_students_panel(columns_frame)
        
        # Right column: Enrolled students
        self._create_enrolled_students_panel(columns_frame)
        
        # Buttons
        self._create_buttons(container)
    
    def _create_available_students_panel(self, parent):
        """Tạo panel danh sách sinh viên available."""
        panel = ctk.CTkFrame(parent, corner_radius=10)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Header
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(
            header,
            text="Available Students",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text=f"{len(self.available_students)} students",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(side="right")
        
        # Search
        search_frame = ctk.CTkFrame(panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.available_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search students...",
            height=30
        )
        self.available_search.pack(fill="x")
        self.available_search.bind("<KeyRelease>", self._on_available_search)
        
        # List
        self.available_list = ctk.CTkScrollableFrame(
            panel,
            fg_color="transparent"
        )
        self.available_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self._update_available_list()
    
    def _create_enrolled_students_panel(self, parent):
        """Tạo panel danh sách sinh viên enrolled."""
        panel = ctk.CTkFrame(parent, corner_radius=10)
        panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Header
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(
            header,
            text="Enrolled Students",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        self.enrolled_count_label = ctk.CTkLabel(
            header,
            text=f"{len(self.enrolled_students)} students",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.enrolled_count_label.pack(side="right")
        
        # Search
        search_frame = ctk.CTkFrame(panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.enrolled_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search enrolled...",
            height=30
        )
        self.enrolled_search.pack(fill="x")
        self.enrolled_search.bind("<KeyRelease>", self._on_enrolled_search)
        
        # List
        self.enrolled_list = ctk.CTkScrollableFrame(
            panel,
            fg_color="transparent"
        )
        self.enrolled_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self._update_enrolled_list()
    
    def _update_available_list(self, search_query: str = ""):
        """Update available students list."""
        # Clear existing
        for widget in self.available_list.winfo_children():
            widget.destroy()
        
        # Filter students
        filtered = self.available_students
        if search_query:
            query = search_query.lower()
            filtered = [
                s for s in self.available_students
                if query in s.get("full_name", "").lower() or
                   query in s.get("username", "").lower() or
                   query in (s.get("student_code") or "").lower()
            ]
        
        # Add student items
        for student in filtered:
            self._create_available_student_item(student)
    
    def _update_enrolled_list(self, search_query: str = ""):
        """Update enrolled students list."""
        # Clear existing
        for widget in self.enrolled_list.winfo_children():
            widget.destroy()
        
        # Filter students
        filtered = self.enrolled_students
        if search_query:
            query = search_query.lower()
            filtered = [
                s for s in self.enrolled_students
                if query in s.get("full_name", "").lower() or
                   query in s.get("username", "").lower() or
                   query in (s.get("student_code") or "").lower()
            ]
        
        # Add student items
        for student in filtered:
            self._create_enrolled_student_item(student)
        
        # Update count
        self.enrolled_count_label.configure(text=f"{len(self.enrolled_students)} students")
    
    def _create_available_student_item(self, student: Dict[str, Any]):
        """Create student item in available list."""
        item = ctk.CTkFrame(self.available_list, fg_color="gray20", corner_radius=8)
        item.pack(fill="x", pady=3, padx=5)
        
        # Info
        info = ctk.CTkFrame(item, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=10, pady=8)
        
        ctk.CTkLabel(
            info,
            text=student.get("full_name", "N/A"),
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        ).pack(anchor="w")
        
        student_code = student.get("student_code") or student.get("username")
        ctk.CTkLabel(
            info,
            text=f"Code: {student_code}",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w")
        
        # Add button
        add_btn = ctk.CTkButton(
            item,
            text="➕ Add",
            width=70,
            height=28,
            command=lambda s=student: self._add_student(s)
        )
        add_btn.pack(side="right", padx=10)
    
    def _create_enrolled_student_item(self, student: Dict[str, Any]):
        """Create student item in enrolled list."""
        item = ctk.CTkFrame(self.enrolled_list, fg_color="gray20", corner_radius=8)
        item.pack(fill="x", pady=3, padx=5)
        
        # Info
        info = ctk.CTkFrame(item, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=10, pady=8)
        
        ctk.CTkLabel(
            info,
            text=student.get("full_name", "N/A"),
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        ).pack(anchor="w")
        
        student_code = student.get("student_code") or student.get("username")
        ctk.CTkLabel(
            info,
            text=f"Code: {student_code}",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w")
        
        # Remove button
        remove_btn = ctk.CTkButton(
            item,
            text="✕ Remove",
            width=80,
            height=28,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=lambda s=student: self._remove_student(s)
        )
        remove_btn.pack(side="right", padx=10)
    
    def _add_student(self, student: Dict[str, Any]):
        """Add student to enrolled list."""
        # Move from available to enrolled
        if student in self.available_students:
            self.available_students.remove(student)
            self.enrolled_students.append(student)
            
            # Update lists
            self._update_available_list(self.available_search.get())
            self._update_enrolled_list(self.enrolled_search.get())
    
    def _remove_student(self, student: Dict[str, Any]):
        """Remove student from enrolled list."""
        # Move from enrolled to available
        if student in self.enrolled_students:
            self.enrolled_students.remove(student)
            self.available_students.append(student)
            
            # Update lists
            self._update_available_list(self.available_search.get())
            self._update_enrolled_list(self.enrolled_search.get())
    
    def _on_available_search(self, event):
        """Handle available search."""
        query = self.available_search.get()
        self._update_available_list(query)
    
    def _on_enrolled_search(self, event):
        """Handle enrolled search."""
        query = self.enrolled_search.get()
        self._update_enrolled_list(query)
    
    def _create_buttons(self, parent):
        """Tạo action buttons."""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", pady=(20, 0))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=150,
            height=40,
            fg_color="gray40",
            hover_color="gray30",
            command=self._on_cancel
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        # Save button
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Save Changes",
            width=150,
            height=40,
            command=self._on_save
        )
        save_btn.pack(side="right")
    
    def _on_save(self):
        """Handle save button."""
        try:
            class_id = self.class_data.get("class_id")
            
            # Get original student codes
            original_codes = set(self.class_data.get("student_codes", []))
            
            # Get new student codes
            new_codes = set()
            for student in self.enrolled_students:
                student_code = student.get("student_code") or student.get("username")
                new_codes.add(student_code)
            
            # Find students to add and remove
            to_add = new_codes - original_codes
            to_remove = original_codes - new_codes
            
            # Perform operations
            errors = []
            
            # Add students
            for student_code in to_add:
                result = self.admin_controller.add_student_to_class(class_id, student_code)
                if not result.get("success"):
                    errors.append(f"Failed to add {student_code}: {result.get('error')}")
            
            # Remove students
            for student_code in to_remove:
                result = self.admin_controller.remove_student_from_class(class_id, student_code)
                if not result.get("success"):
                    errors.append(f"Failed to remove {student_code}: {result.get('error')}")
            
            if errors:
                messagebox.showwarning(
                    "Partial Success",
                    "Some operations failed:\n\n" + "\n".join(errors)
                )
            else:
                self.success = True
                messagebox.showinfo("Success", "Student enrollment updated successfully!")
                self.destroy()
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _on_cancel(self):
        """Handle cancel button."""
        self.destroy()
