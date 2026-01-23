"""
User Management Page - Quản lý người dùng
=========================================

Page quản lý users:
- Hiển thị danh sách users
- Tìm kiếm, filter
- CRUD operations
- Phân quyền role
"""

import customtkinter as ctk
from typing import List, Optional, Dict, Any
from tkinter import messagebox

from core.enums import UserRole


class UserManagementPage(ctk.CTkFrame):
    """
    User Management Page - Quản lý người dùng.
    
    Features:
        - List all users with pagination
        - Search and filter users
        - Create/Edit/Delete users
        - Assign roles
        - View user details
        
    Example:
        >>> page = UserManagementPage(parent, admin_controller)
        >>> page.pack(fill="both", expand=True)
    """
    
    def __init__(
        self, 
        parent, 
        admin_controller,
        **kwargs
    ):
        """
        Khởi tạo User Management Page.
        
        Args:
            parent: Parent widget
            admin_controller: AdminController instance
        """
        super().__init__(parent, **kwargs)
        
        self.admin_controller = admin_controller
        self.users_data: List[Dict[str, Any]] = []
        self.filtered_users: List[Dict[str, Any]] = []
        self.selected_user: Optional[Dict[str, Any]] = None
        
        # Filter state
        self.search_query = ""
        self.role_filter = "All"
        
        self._init_ui()
        self._load_users()
    
    def _init_ui(self):
        """Khởi tạo UI components."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header with search and actions
        self._create_header()
        
        # User list
        self._create_user_list()
        
        # Action buttons
        self._create_action_buttons()
    
    def _create_header(self):
        """Tạo header với search và filters."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="👥 User Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Search bar
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search by name, username, email...",
            height=35
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        
        # Role filter
        self.role_filter_var = ctk.StringVar(value="All")
        role_menu = ctk.CTkOptionMenu(
            search_frame,
            values=["All", "Admin", "Teacher", "Student"],
            variable=self.role_filter_var,
            command=self._on_filter_change,
            width=150
        )
        role_menu.grid(row=0, column=1, padx=(0, 10))
        
        # Add user button
        add_btn = ctk.CTkButton(
            search_frame,
            text="➕ Add User",
            width=120,
            height=35,
            command=self._on_add_user
        )
        add_btn.grid(row=0, column=2)
    
    def _create_user_list(self):
        """Tạo user list table."""
        list_frame = ctk.CTkFrame(self, corner_radius=10)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)
        
        # Table header
        header = ctk.CTkFrame(list_frame, fg_color="gray25", height=40)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        header.grid_propagate(False)
        
        headers = ["ID", "Username", "Full Name", "Role", "Email"]
        for i, text in enumerate(headers):
            label = ctk.CTkLabel(
                header,
                text=text,
                font=ctk.CTkFont(size=13, weight="bold")
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="w")
        
        # Scrollable user list
        self.user_list_frame = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="transparent"
        )
        self.user_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.user_list_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
    
    def _create_action_buttons(self):
        """Tạo action buttons."""
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Edit button
        self.edit_btn = ctk.CTkButton(
            action_frame,
            text="✏️ Edit Selected",
            width=140,
            command=self._on_edit_user,
            state="disabled"
        )
        self.edit_btn.pack(side="left", padx=(0, 10))
        
        # Delete button
        self.delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ Delete Selected",
            width=140,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=self._on_delete_user,
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
    
    def _load_users(self):
        """Load danh sách users từ controller."""
        try:
            result = self.admin_controller.get_all_users()
            
            if result.get("success"):
                self.users_data = result.get("users", [])
                self.filtered_users = self.users_data.copy()
                self._update_user_list()
            else:
                self._show_error(result.get("error", "Failed to load users"))
                
        except Exception as e:
            self._show_error(f"Error loading users: {str(e)}")
    
    def _update_user_list(self):
        """Update user list display."""
        # Clear existing items
        for widget in self.user_list_frame.winfo_children():
            widget.destroy()
        
        # Add user rows
        for idx, user in enumerate(self.filtered_users):
            self._create_user_row(idx, user)
        
        # Update info label
        total = len(self.users_data)
        filtered = len(self.filtered_users)
        self.info_label.configure(
            text=f"Showing {filtered} of {total} users"
        )
    
    def _create_user_row(self, idx: int, user: Dict[str, Any]):
        """
        Tạo một row trong user list.
        
        Args:
            idx: Row index
            user: User data
        """
        # Alternating row colors
        bg_color = "gray20" if idx % 2 == 0 else "transparent"
        
        row_frame = ctk.CTkFrame(
            self.user_list_frame,
            fg_color=bg_color,
            height=50
        )
        row_frame.grid(row=idx, column=0, sticky="ew", pady=1)
        row_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        row_frame.grid_propagate(False)
        
        # Make row clickable
        row_frame.bind("<Button-1>", lambda e, u=user: self._on_user_select(u))
        
        # Columns
        columns = [
            str(user.get("user_id", "")),
            user.get("username", ""),
            user.get("full_name", ""),
            user.get("role", ""),
            user.get("email", "") or "N/A"
        ]
        
        for i, text in enumerate(columns):
            label = ctk.CTkLabel(
                row_frame,
                text=text,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="w")
            label.bind("<Button-1>", lambda e, u=user: self._on_user_select(u))
    
    def _on_search_change(self, event):
        """Handle search input change."""
        self.search_query = self.search_entry.get().lower()
        self._apply_filters()
    
    def _on_filter_change(self, choice):
        """Handle role filter change."""
        self.role_filter = choice
        self._apply_filters()
    
    def _apply_filters(self):
        """Apply search and filters."""
        self.filtered_users = []
        
        for user in self.users_data:
            # Search filter
            if self.search_query:
                searchable = f"{user.get('username', '')} {user.get('full_name', '')} {user.get('email', '')}".lower()
                if self.search_query not in searchable:
                    continue
            
            # Role filter
            if self.role_filter != "All":
                if user.get("role", "").upper() != self.role_filter.upper():
                    continue
            
            self.filtered_users.append(user)
        
        self._update_user_list()
    
    def _on_user_select(self, user: Dict[str, Any]):
        """
        Handle user selection.
        
        Args:
            user: Selected user data
        """
        self.selected_user = user
        
        # Enable action buttons
        self.edit_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")
    
    def _on_add_user(self):
        """Handle add user button."""
        # Import here to avoid circular import
        from .user_dialog import UserDialog
        
        dialog = UserDialog(
            self,
            self.admin_controller,
            mode="create"
        )
        self.wait_window(dialog)
        
        # Refresh list if user was added
        if hasattr(dialog, 'success') and dialog.success:
            self._load_users()
    
    def _on_edit_user(self):
        """Handle edit user button."""
        if not self.selected_user:
            return
        
        # Import here to avoid circular import
        from .user_dialog import UserDialog
        
        dialog = UserDialog(
            self,
            self.admin_controller,
            mode="edit",
            user_data=self.selected_user
        )
        self.wait_window(dialog)
        
        # Refresh list if user was updated
        if hasattr(dialog, 'success') and dialog.success:
            self._load_users()
            self.selected_user = None
    
    def _on_delete_user(self):
        """Handle delete user button."""
        if not self.selected_user:
            return
        
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete user '{self.selected_user.get('username')}'?\n\n"
            "This action cannot be undone."
        )
        
        if not result:
            return
        
        # Delete user
        try:
            delete_result = self.admin_controller.delete_user(
                self.selected_user.get("user_id")
            )
            
            if delete_result.get("success"):
                messagebox.showinfo("Success", "User deleted successfully")
                self._load_users()
                self.selected_user = None
                
                # Disable action buttons
                self.edit_btn.configure(state="disabled")
                self.delete_btn.configure(state="disabled")
            else:
                self._show_error(delete_result.get("error", "Failed to delete user"))
                
        except Exception as e:
            self._show_error(f"Error deleting user: {str(e)}")
    
    def _show_error(self, message: str):
        """
        Hiển thị error message.
        
        Args:
            message: Error message
        """
        messagebox.showerror("Error", message)
    
    def refresh(self):
        """Public method để refresh user list."""
        self._load_users()
