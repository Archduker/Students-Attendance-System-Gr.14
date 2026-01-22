#!/usr/bin/env python3
"""
Demo Admin Module UI
====================

Script để chạy và test giao diện admin module.
"""

import customtkinter as ctk
from unittest.mock import Mock

# Import admin pages
from views.pages.admin import AdminLoginPage, AdminDashboard, UserManagementPage, ClassManagementPage
from views.pages.admin.reports import SystemReportsPage


class AdminModuleDemo(ctk.CTk):
    """Demo application cho admin module với login authentication."""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Admin Module - Student Attendance System")
        self.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create mock controllers
        self.auth_controller = self._create_mock_auth_controller()
        self.admin_controller = self._create_mock_admin_controller()
        
        # Current user (will be set after login)
        self.current_user = None
        self.is_authenticated = False
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Show login page first
        self.show_login_page()
    
    def show_login_page(self):
        """Show login page."""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Create login page
        login_page = AdminLoginPage(
            self,
            self.auth_controller,
            on_login_success=self._on_login_success
        )
        login_page.grid(row=0, column=0, sticky="nsew")
    
    def _on_login_success(self, user):
        """Handle successful login."""
        self.current_user = user
        self.is_authenticated = True
        
        # Clear window and show admin panel
        for widget in self.winfo_children():
            widget.destroy()
        
        # Initialize admin panel
        self._init_admin_panel()
    
    def _create_mock_auth_controller(self):
        """Tạo mock auth controller."""
        controller = Mock()
        
        # Mock login - accept admin/admin123
        def mock_login(username, password):
            if username == "admin" and password == "admin123":
                return {
                    "success": True,
                    "user": {
                        "user_id": 1,
                        "username": "admin",
                        "full_name": "Administrator",
                        "email": "admin@school.edu"
                    },
                    "role": "ADMIN"
                }
            else:
                return {
                    "success": False,
                    "error": "Invalid username or password"
                }
        
        controller.handle_login = mock_login
        return controller
    
    def _create_mock_admin_controller(self):
        """Tạo mock controller với sample data."""
        controller = Mock()
        
        # Mock dashboard stats
        controller.get_dashboard_stats.return_value = {
            "success": True,
            "data": {
                "total_users": 125,
                "total_admins": 3,
                "total_teachers": 15,
                "total_students": 107,
                "total_classes": 8,
                "total_sessions": 45
            }
        }
        
        # Mock users data
        sample_users = [
            {"user_id": 1, "username": "admin", "full_name": "Admin User", "role": "ADMIN", "email": "admin@school.edu"},
            {"user_id": 2, "username": "gv001", "full_name": "Nguyễn Văn A", "role": "TEACHER", "email": "vana@school.edu"},
            {"user_id": 3, "username": "gv002", "full_name": "Trần Thị B", "role": "TEACHER", "email": "thib@school.edu"},
            {"user_id": 4, "username": "sv001", "full_name": "Lê Văn C", "role": "STUDENT", "email": "vanc@student.edu"},
            {"user_id": 5, "username": "sv002", "full_name": "Phạm Thị D", "role": "STUDENT", "email": "thid@student.edu"},
            {"user_id": 6, "username": "sv003", "full_name": "Hoàng Văn E", "role": "STUDENT", "email": "vane@student.edu"},
        ]
        controller.get_all_users.return_value = {
            "success": True,
            "users": sample_users
        }
        
        # Mock classes data
        sample_classes = [
            {"class_id": "CS101", "class_name": "Introduction to Programming", "subject_code": "CS101", 
             "teacher_code": "GV001", "student_codes": ["SV001", "SV002", "SV003"]},
            {"class_id": "CS102", "class_name": "Data Structures", "subject_code": "CS102", 
             "teacher_code": "GV002", "student_codes": ["SV001", "SV002"]},
            {"class_id": "MAT101", "class_name": "Calculus I", "subject_code": "MAT101", 
             "teacher_code": "GV001", "student_codes": ["SV001", "SV003"]},
        ]
        controller.get_all_classes.return_value = {
            "success": True,
            "classes": sample_classes
        }
        
        # Mock teachers
        sample_teachers = [
            {"user_id": 2, "username": "gv001", "full_name": "Nguyễn Văn A", "teacher_code": "GV001"},
            {"user_id": 3, "username": "gv002", "full_name": "Trần Thị B", "teacher_code": "GV002"},
        ]
        controller.get_teachers.return_value = {
            "success": True,
            "teachers": sample_teachers
        }
        
        # Mock create/update/delete operations
        controller.create_user.return_value = {
            "success": True,
            "message": "User created successfully",
            "password": "temp1234"
        }
        controller.update_user.return_value = {
            "success": True,
            "message": "User updated successfully"
        }
        controller.delete_user.return_value = {
            "success": True,
            "message": "User deleted successfully"
        }
        
        controller.create_class.return_value = {
            "success": True,
            "message": "Class created successfully"
        }
        controller.update_class.return_value = {
            "success": True,
            "message": "Class updated successfully"
        }
        controller.delete_class.return_value = {
            "success": True,
            "message": "Class deleted successfully"
        }
        
        # Mock reports
        controller.generate_report.return_value = {
            "success": True,
            "data": {
                "summary": {
                    "Total Records": 150,
                    "Present": 135,
                    "Absent": 15,
                    "Attendance Rate": "90%"
                },
                "details": [
                    "2026-01-20: Class CS101 - 25/28 students present (89%)",
                    "2026-01-21: Class CS102 - 30/32 students present (94%)",
                    "2026-01-22: Class MAT101 - 22/25 students present (88%)"
                ]
            }
        }
        
        controller.export_report.return_value = {
            "success": True,
            "message": "Report exported successfully"
        }
        
        return controller
    
    def _init_admin_panel(self):
        """Initialize admin panel after successful login."""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create UI
        self._create_sidebar()
        self._create_main_content()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def _create_sidebar(self):
        """Tạo sidebar navigation."""
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(6, weight=1)
        
        # Logo/Title
        title_label = ctk.CTkLabel(
            sidebar,
            text="Admin Panel",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Navigation buttons
        self.nav_buttons = []
        
        # Dashboard button
        dashboard_btn = ctk.CTkButton(
            sidebar,
            text="📊 Dashboard",
            command=self.show_dashboard,
            height=40,
            anchor="w"
        )
        dashboard_btn.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons.append(dashboard_btn)
        
        # Users button
        users_btn = ctk.CTkButton(
            sidebar,
            text="👥 User Management",
            command=self.show_users,
            height=40,
            anchor="w"
        )
        users_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons.append(users_btn)
        
        # Classes button
        classes_btn = ctk.CTkButton(
            sidebar,
            text="📚 Class Management",
            command=self.show_classes,
            height=40,
            anchor="w"
        )
        classes_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons.append(classes_btn)
        
        # Reports button
        reports_btn = ctk.CTkButton(
            sidebar,
            text="📊 Reports",
            command=self.show_reports,
            height=40,
            anchor="w"
        )
        reports_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons.append(reports_btn)
        
        # Separator
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="gray30")
        separator.grid(row=5, column=0, sticky="ew", padx=20, pady=20)
        
        # User info
        if self.current_user:
            user_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
            user_frame.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
            
            user_label = ctk.CTkLabel(
                user_frame,
                text=f"👤 {self.current_user.get('full_name', 'Admin')}",
                font=ctk.CTkFont(size=11),
                anchor="w"
            )
            user_label.pack(fill="x")
            
            role_label = ctk.CTkLabel(
                user_frame,
                text="Administrator",
                font=ctk.CTkFont(size=9),
                text_color="gray",
                anchor="w"
            )
            role_label.pack(fill="x")
        
        # Logout button
        logout_btn = ctk.CTkButton(
            sidebar,
            text="🚪 Logout",
            height=35,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=self._on_logout
        )
        logout_btn.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
        
        # Info label
        info_label = ctk.CTkLabel(
            sidebar,
            text="Demo Mode\nMock Data Only",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_label.grid(row=8, column=0, padx=20, pady=20)
    
    def _on_logout(self):
        """Handle logout."""
        from tkinter import messagebox
        
        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )
        
        if result:
            self.current_user = None
            self.is_authenticated = False
            self.show_login_page()
    
    def _create_main_content(self):
        """Tạo main content area."""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Content container (will hold different pages)
        self.content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_container.grid(row=0, column=0, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)
    
    def _clear_content(self):
        """Clear current content."""
        for widget in self.content_container.winfo_children():
            widget.destroy()
    
    def _highlight_button(self, active_index):
        """Highlight active navigation button."""
        for i, btn in enumerate(self.nav_buttons):
            if i == active_index:
                btn.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            else:
                btn.configure(fg_color=("gray75", "gray25"))
    
    def show_dashboard(self):
        """Show dashboard page."""
        self._clear_content()
        self._highlight_button(0)
        
        dashboard = AdminDashboard(self.content_container, self.admin_controller)
        dashboard.grid(row=0, column=0, sticky="nsew")
    
    def show_users(self):
        """Show user management page."""
        self._clear_content()
        self._highlight_button(1)
        
        users_page = UserManagementPage(self.content_container, self.admin_controller)
        users_page.grid(row=0, column=0, sticky="nsew")
    
    def show_classes(self):
        """Show class management page."""
        self._clear_content()
        self._highlight_button(2)
        
        classes_page = ClassManagementPage(self.content_container, self.admin_controller)
        classes_page.grid(row=0, column=0, sticky="nsew")
    
    def show_reports(self):
        """Show reports page."""
        self._clear_content()
        self._highlight_button(3)
        
        reports_page = SystemReportsPage(self.content_container, self.admin_controller)
        reports_page.grid(row=0, column=0, sticky="nsew")


def main():
    """Main entry point."""
    print("🚀 Starting Admin Module Demo...")
    print("=" * 50)
    print("Demo mode: Using mock data")
    print("")
    print("🔐 LOGIN CREDENTIALS:")
    print("   Username: admin")
    print("   Password: admin123")
    print("")
    print("Note: Only admin role can access the panel")
    print("=" * 50)
    
    app = AdminModuleDemo()
    app.mainloop()


if __name__ == "__main__":
    main()
