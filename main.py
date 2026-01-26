#!/usr/bin/env python3
"""
Student Attendance System - Entry Point
========================================

Main entry point cho ứng dụng điểm danh sinh viên.

Cách chạy:
    python main.py              # Chạy ứng dụng GUI
    python main.py --init-db    # Khởi tạo database
    python main.py --seed       # Seed demo data

Author: Group 14
Version: 1.0.0
"""

import sys
import argparse
from pathlib import Path

# Thêm project root vào path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def init_database(seed: bool = False):
    """Khởi tạo database."""
    print("🚀 Đang khởi tạo database...")
    
    from data.migrations.init_db import init_database as init_db, seed_demo_data
    
    init_db(reset=True)
    
    if seed:
        print("🌱 Đang seed demo data...")
        seed_demo_data()
    
    print("✨ Hoàn tất!")


def create_app():
    """
    Khởi tạo và cấu hình ứng dụng.
    
    Returns:
        Configured application instance
    """
    # Import dependencies
    from data.database import Database
    from data.repositories import UserRepository
    from services import SecurityService, EmailService, AuthService, SessionService
    from controllers import AuthController
    
    # Initialize database
    db = Database()
    
    # Initialize repositories
    user_repo = UserRepository(db)
    
    # Initialize services
    security_service = SecurityService()
    session_service = SessionService(security_service)
    email_service = EmailService()
    auth_service = AuthService(user_repo, security_service, session_service, email_service)
    
    # Initialize controllers
    auth_controller = AuthController(auth_service)
    
    # Return app configuration
    return {
        "db": db,
        "repositories": {
            "user": user_repo,
        },
        "services": {
            "security": security_service,
            "email": email_service,
            "auth": auth_service,
        },
        "controllers": {
            "auth": auth_controller,
        }
    }


def run_gui(app_config: dict):
    """
    Chạy ứng dụng GUI.
    
    Args:
        app_config: Application configuration từ create_app()
    """
    try:
        import customtkinter as ctk
        
        from config.settings import (
            APP_NAME, 
            DEFAULT_WINDOW_WIDTH, 
            DEFAULT_WINDOW_HEIGHT,
            APPEARANCE_MODE,
            COLOR_THEME
        )
        
        # Configure CustomTkinter
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(COLOR_THEME)
        
        # Create main window
        root = ctk.CTk()
        root.title(APP_NAME)
        root.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        
        # Center window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (DEFAULT_WINDOW_WIDTH // 2)
        y = (root.winfo_screenheight() // 2) - (DEFAULT_WINDOW_HEIGHT // 2)
        root.geometry(f"+{x}+{y}")
        
        # TODO: Initialize views and routing
        # from views.app import App
        # app = App(root, app_config["controllers"])
        
        from views.pages.auth.login_page import LoginPage
        from views.pages.auth.reset_password_page import ResetPasswordPage
        
        # Student Views
        from views.layouts.student_layout import StudentLayout
        from views.pages.student import StudentDashboard, SubmitAttendancePage, AttendanceHistoryPage, ProfilePage
        
        # Teacher Views
        from views.layouts.teacher_layout import TeacherLayout
        from views.pages.teacher import TeacherDashboardPage, SessionManagementPage, SessionDetailPage, HistoryPage
        from views.pages.teacher import ProfilePage as TeacherProfilePage
        
        # Get auth controller from app config
        auth_controller = app_config["controllers"]["auth"]
        
        # Current page container
        current_page = [None]
        
        def show_login():
            """Hiển thị trang login."""
            if current_page[0]:
                current_page[0].destroy()
            current_page[0] = LoginPage(
                root, 
                auth_controller=auth_controller,
                on_login_success=on_login_success,
                on_forgot_password=show_reset_password
            )
        
        def show_reset_password():
            """Hiển thị trang reset password."""
            if current_page[0]:
                current_page[0].destroy()
            current_page[0] = ResetPasswordPage(
                root,
                auth_controller=auth_controller,
                on_back_to_login=show_login
            )
        
        def show_student_app(user):
            """Hiển thị giao diện sinh viên."""
            if current_page[0]:
                current_page[0].destroy()
            

            # Initialize student controller dependencies
            from controllers.student_controller import StudentController
            from services.student_service import StudentService
            from data.repositories import AttendanceRecordRepository, AttendanceSessionRepository, ClassroomRepository
            
            # Get database and repos
            db = app_config["db"]
            user_repo = app_config["repositories"]["user"]
            # Initialize repositories
            record_repo = AttendanceRecordRepository(db)
            session_repo = AttendanceSessionRepository(db)
            class_repo = ClassroomRepository(db)
            
            # Initialize service
            student_service = StudentService(
                user_repo=user_repo,
                attendance_record_repo=record_repo,
                attendance_session_repo=session_repo,
                class_repo=class_repo
            )
            
            # Initialize controller
            student_controller = StudentController(student_service)
                
            # Define navigation handler
            def navigate(page_key):
                # Clear content area
                for child in layout.content_area.winfo_children():
                    child.destroy()
                
                # Update layout state (but don't rebuild sidebar)
                layout.current_path = page_key
                
                # Instantiate Page
                if page_key == "dashboard":
                    StudentDashboard(
                        layout.content_area, 
                        on_navigate=navigate, 
                        user=user,
                        student_service=student_service,
                        student_controller=student_controller
                    )
                elif page_key == "submit_attendance":
                    SubmitAttendancePage(
                        layout.content_area, 
                        on_navigate=navigate,
                        user=user,
                        student_service=student_service,
                        student_controller=student_controller
                    )
                elif page_key == "history":
                    AttendanceHistoryPage(
                        layout.content_area, 
                        on_navigate=navigate,
                        user=user,
                        student_service=student_service
                    )
                elif page_key == "profile":
                    ProfilePage(layout.content_area, on_navigate=navigate, user=user)
                elif page_key == "logout":
                    auth_controller.handle_logout()
                    show_login()

            # Create Layout
            layout = StudentLayout(root, on_navigate=navigate, user=user)
            current_page[0] = layout
            
            # Show Dashboard
            navigate("dashboard")

        def show_teacher_app(user):
            """Hiển thị giao diện giáo viên."""
            if current_page[0]:
                current_page[0].destroy()
            
            # Initialize teacher controller once
            from controllers.teacher_controller import TeacherController
            from data.repositories import ClassroomRepository, AttendanceRecordRepository
            from services.attendance_session_service import AttendanceSessionService
            from services.qr_service import QRService
            
            # Get database and repos
            db = app_config["db"]
            classroom_repo = ClassroomRepository(db)
            record_repo = AttendanceRecordRepository(db)
            
            # Session repository
            from data.repositories import AttendanceSessionRepository
            session_repo = AttendanceSessionRepository(db)
            
            # Initialize services
            qr_service = QRService(security_service=app_config["services"]["security"])
            session_service = AttendanceSessionService(
                session_repo=session_repo,
                record_repo=record_repo,
                classroom_repo=classroom_repo,
                security_service=app_config["services"]["security"],
                qr_service=qr_service
            )
            
            # Initialize teacher controller
            teacher_controller = TeacherController(
                session_service=session_service,
                auth_service=app_config["services"]["auth"],
                classroom_repo=classroom_repo,
                record_repo=record_repo
            )
                
            # Define navigation handler
            def navigate(page_key):
                # Clear content area
                for child in layout.content_area.winfo_children():
                    child.destroy()
                
                # Update layout state (but don't rebuild sidebar)
                layout.current_path = page_key 
                
                # Instantiate Page
                if page_key == "dashboard":
                    TeacherDashboardPage(layout.content_area, teacher=user, controller=teacher_controller)
                elif page_key == "session_management":
                    SessionManagementPage(layout.content_area, teacher=user, controller=teacher_controller)
                elif page_key == "session_detail":
                    SessionDetailPage(layout.content_area, session_id=None)
                elif page_key == "history":
                    HistoryPage(layout.content_area, teacher=user, controller=teacher_controller)
                elif page_key == "profile":
                    TeacherProfilePage(layout.content_area, teacher=user)
                elif page_key == "logout":
                    auth_controller.handle_logout()
                    show_login()

            # Create Layout
            layout = TeacherLayout(root, on_navigate=navigate, user=user)
            current_page[0] = layout
            
            # Show Dashboard
            navigate("dashboard")

        def show_admin_app(user):
            """Hiển thị giao diện admin."""
            if current_page[0]:
                current_page[0].destroy()
            
            # Import admin components
            from views.layouts.admin_layout import AdminLayout
            from views.pages.admin import AdminDashboard, SystemReportsPage, UserManagementPage, ClassManagementPage
            
            # Initialize admin controller dependencies
            from controllers.admin_controller import AdminController
            from services.admin_service import AdminService
            from data.repositories import ClassroomRepository, AttendanceSessionRepository
            
            # Get database and repos
            db = app_config["db"]
            user_repo = app_config["repositories"]["user"]
            classroom_repo = ClassroomRepository(db)
            session_repo = AttendanceSessionRepository(db)
            
            # Initialize service
            admin_service = AdminService(
                user_repo=user_repo,
                classroom_repo=classroom_repo,
                attendance_repo=session_repo,
                security_service=app_config["services"]["security"]
            )
            
            # Initialize controller
            admin_controller = AdminController(admin_service)
            
            # Define navigation handler
            def navigate(page_key):
                # Clear content area
                for child in layout.content_area.winfo_children():
                    child.destroy()
                
                # Update layout state
                layout.current_path = page_key
                
                # Refresh sidebar buttons to update active state
                layout._refresh_menu_buttons()
                
                # Instantiate and pack pages
                if page_key == "dashboard":
                    page = AdminDashboard(layout.content_area, admin_user=user, controller=admin_controller)
                    page.pack(fill="both", expand=True)
                elif page_key == "reports":
                    page = SystemReportsPage(layout.content_area, admin_user=user, controller=admin_controller)
                    page.pack(fill="both", expand=True)
                elif page_key == "user_management":
                    page = UserManagementPage(layout.content_area, admin_controller=admin_controller)
                    page.pack(fill="both", expand=True)
                elif page_key == "class_management":
                    page = ClassManagementPage(layout.content_area, admin_controller=admin_controller)
                    page.pack(fill="both", expand=True)
                elif page_key == "logout":
                    auth_controller.handle_logout()
                    show_login()

            # Create Layout
            layout = AdminLayout(root, on_navigate=navigate, user=user)
            current_page[0] = layout
            
            # Show Dashboard
            navigate("dashboard")

        def on_login_success(user, remember_me):
            """Callback khi login thành công."""
            print(f"✅ Đăng nhập thành công: {user.full_name} ({user.role.value})")
            
            if user.role.value == "STUDENT":
                show_student_app(user)
            elif user.role.value == "TEACHER":
                show_teacher_app(user)
            elif user.role.value == "ADMIN":
                show_admin_app(user)
            else:
                import tkinter.messagebox as messagebox
                messagebox.showinfo(
                    "Đăng nhập thành công", 
                    f"Chào mừng {user.full_name}!\nRole: {user.role.value}\n(Vai trò không được hỗ trợ)"
                )
        
        # Show login page
        show_login()
        
        # Run main loop
        print(f"🎓 {APP_NAME} đang chạy...")
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        print("📦 Vui lòng cài đặt dependencies: pip install -r requirements.txt")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Student Attendance System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              Chạy ứng dụng GUI
  python main.py --init-db    Khởi tạo database
  python main.py --seed       Khởi tạo database với demo data
        """
    )
    
    parser.add_argument(
        "--init-db",
        action="store_true",
        help="Khởi tạo database (xóa data cũ)"
    )
    
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Seed demo data vào database"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Student Attendance System v1.0.0"
    )
    
    args = parser.parse_args()
    
    # Handle database initialization
    if args.init_db or args.seed:
        init_database(seed=args.seed)
        return
    
    # Run GUI application
    try:
        app_config = create_app()
        run_gui(app_config)
    except KeyboardInterrupt:
        print("\n👋 Đã thoát ứng dụng.")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        if "--debug" in sys.argv:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()

