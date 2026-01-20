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
    from services import SecurityService, EmailService, AuthService
    from controllers import AuthController
    
    # Initialize database
    db = Database()
    
    # Initialize repositories
    user_repo = UserRepository(db)
    
    # Initialize services
    security_service = SecurityService()
    email_service = EmailService()
    auth_service = AuthService(user_repo, security_service, email_service)
    
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
        
        # Placeholder label
        placeholder = ctk.CTkLabel(
            root,
            text="🎓 Student Attendance System\n\nGUI đang được phát triển...\n\n"
                 "Chạy 'python main.py --init-db --seed' để khởi tạo database.",
            font=("Segoe UI", 18),
        )
        placeholder.place(relx=0.5, rely=0.5, anchor="center")
        
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
