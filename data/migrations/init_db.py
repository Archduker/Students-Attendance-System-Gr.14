"""
Database Initialization - Khởi tạo Database
============================================

Script để tạo database schema và seed data.

Cách sử dụng:
    python -m data.migrations.init_db
    
    hoặc trong code:
    from data.migrations.init_db import init_database
    init_database()
"""

import sqlite3
from pathlib import Path

from config.database import get_db_path, ensure_database_dir


def get_schema_path() -> Path:
    """Lấy đường dẫn đến file schema.sql."""
    return Path(__file__).parent / "schema.sql"


def init_database(reset: bool = False) -> None:
    """
    Khởi tạo database với schema.
    
    Args:
        reset: Nếu True, xóa database cũ và tạo mới
        
    Example:
        >>> init_database()  # Tạo mới nếu chưa có
        >>> init_database(reset=True)  # Reset hoàn toàn
    """
    ensure_database_dir()
    db_path = get_db_path()
    
    # Xóa database cũ nếu reset
    if reset and db_path.exists():
        db_path.unlink()
        print(f"🗑️  Đã xóa database cũ: {db_path}")
    
    # Đọc schema
    schema_path = get_schema_path()
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    
    # Tạo database và chạy schema
    conn = sqlite3.connect(str(db_path))
    try:
        conn.executescript(schema_sql)
        conn.commit()
        print(f"✅ Database đã được khởi tạo: {db_path}")
    except Exception as e:
        print(f"❌ Lỗi khi khởi tạo database: {e}")
        raise
    finally:
        conn.close()


def seed_demo_data() -> None:
    """
    Seed demo data cho testing/development.
    
    Tạo:
    - 1 Admin account
    - 2 Teacher accounts
    - 5 Student accounts
    - 2 Classes
    """
    import bcrypt
    from datetime import datetime
    
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    
    try:
        cursor = conn.cursor()
        
        # Hash password mặc định
        default_password = bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode()
        
        # === INSERT USERS ===
        users_data = [
            # Admin
            ("admin", default_password, "Admin System", "admin@school.edu.vn", "ADMIN", "AD001", None, None),
            # Teachers
            ("teacher1", default_password, "Nguyễn Văn A", "teacher1@school.edu.vn", "TEACHER", None, "GV001", None),
            ("teacher2", default_password, "Trần Thị B", "teacher2@school.edu.vn", "TEACHER", None, "GV002", None),
            # Students
            ("student1", default_password, "Lê Văn C", "student1@school.edu.vn", "STUDENT", None, None, "SV001"),
            ("student2", default_password, "Phạm Thị D", "student2@school.edu.vn", "STUDENT", None, None, "SV002"),
            ("student3", default_password, "Hoàng Văn E", "student3@school.edu.vn", "STUDENT", None, None, "SV003"),
            ("student4", default_password, "Ngô Thị F", "student4@school.edu.vn", "STUDENT", None, None, "SV004"),
            ("student5", default_password, "Vũ Văn G", "student5@school.edu.vn", "STUDENT", None, None, "SV005"),
        ]
        
        cursor.executemany("""
            INSERT INTO users (username, password_hash, full_name, email, role, admin_id, teacher_code, student_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, users_data)
        
        # === INSERT CLASSES ===
        classes_data = [
            ("CS101-2024", "Nhập môn Lập trình Python", "CS101", "GV001"),
            ("CS201-2024", "Cấu trúc Dữ liệu và Giải thuật", "CS201", "GV002"),
        ]
        
        cursor.executemany("""
            INSERT INTO classes (class_id, class_name, subject_code, teacher_code)
            VALUES (?, ?, ?, ?)
        """, classes_data)
        
        # === INSERT CLASSES_STUDENT ===
        classes_student_data = [
            ("CS101-2024", "SV001"),
            ("CS101-2024", "SV002"),
            ("CS101-2024", "SV003"),
            ("CS201-2024", "SV003"),
            ("CS201-2024", "SV004"),
            ("CS201-2024", "SV005"),
        ]
        
        cursor.executemany("""
            INSERT INTO classes_student (class_id, student_code)
            VALUES (?, ?)
        """, classes_student_data)
        
        conn.commit()
        print("✅ Demo data đã được seed thành công!")
        print("   📧 Admin: admin / 123456")
        print("   📧 Teacher: teacher1, teacher2 / 123456")
        print("   📧 Student: student1-5 / 123456")
        
    except Exception as e:
        print(f"❌ Lỗi khi seed data: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    import sys
    
    # Parse arguments
    reset = "--reset" in sys.argv
    seed = "--seed" in sys.argv
    
    print("🚀 Đang khởi tạo database...")
    init_database(reset=reset)
    
    if seed:
        print("🌱 Đang seed demo data...")
        seed_demo_data()
    
    print("✨ Hoàn tất!")
