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
            # Admin (1 user)
            ("admin", default_password, "Nguyễn Quản Trị", "admin@ut.edu.vn", "ADMIN", "AD001", None, None),
            
            # Teachers (3 users)
            ("teacher1", default_password, "TS. Phạm Xuân Thương", "thuongpx@ut.edu.vn", "TEACHER", None, "GV001", None),
            ("teacher2", default_password, "Th5. Nguyễn Phương Trâm", "tramnp@ut.edu.vn", "TEACHER", None, "GV002", None),
            ("teacher3", default_password, "TS. Lê Văn Hùng", "hunglv@ut.edu.vn", "TEACHER", None, "GV003", None),
            
            # Students (12 users)
            # Special student - Trần Thanh Thuận
            ("thuantt", default_password, "Trần Thanh Thuận", "thuantt0354@ut.edu.vn", "STUDENT", None, None, "SV001"),
            
            # 11 other students
            ("student2", default_password, "Phan Nhật Tài", "taipn@ut.edu.vn", "STUDENT", None, None, "SV002"),
            ("student3", default_password, "Hoàng Thuỳ Linh", "linhht@ut.edu.vn", "STUDENT", None, None, "SV003"),
            ("student4", default_password, "Đàm Vĩnh Hưng", "hungdv@ut.edu.vn", "STUDENT", None, None, "SV004"),
            ("student5", default_password, "Trần Thị Bích Phương", "phuongtb@ut.edu.vn", "STUDENT", None, None, "SV005"),
            ("student6", default_password, "Hồ Ngọc Hà", "hahn@ut.edu.vn", "STUDENT", None, None, "SV006"),
            ("student7", default_password, "Phan Thị Thuỳ Quyên", "quyenpt@ut.edu.vn", "STUDENT", None, None, "SV007"),
            ("student8", default_password, "Lê Minh Tâm", "tamlm@ut.edu.vn", "STUDENT", None, None, "SV008"),
            ("student9", default_password, "Nguyễn Văn An", "annv@ut.edu.vn", "STUDENT", None, None, "SV009"),
            ("student10", default_password, "Trương Thị Mai", "maitt@ut.edu.vn", "STUDENT", None, None, "SV010"),
            ("student11", default_password, "Vũ Đức Thắng", "thangvd@ut.edu.vn", "STUDENT", None, None, "SV011"),
            ("student12", default_password, "Phạm Hồng Nhung", "nhungph@ut.edu.vn", "STUDENT", None, None, "SV012"),
        ]
        
        cursor.executemany("""
            INSERT INTO users (username, password_hash, full_name, email, role, admin_id, teacher_code, student_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, users_data)
        
        # === INSERT CLASSES ===
        classes_data = [
            ("CS101-2024", "Nhập môn Lập trình Python", "CS101", "GV001"),
            ("CS201-2024", "Cấu trúc Dữ liệu và Giải thuật", "CS201", "GV002"),
            ("AI301-2024", "Trí tuệ Nhân tạo Cơ bản", "AI301", "GV003"),
        ]
        
        cursor.executemany("""
            INSERT INTO classes (class_id, class_name, subject_code, teacher_code)
            VALUES (?, ?, ?, ?)
        """, classes_data)
        
        # === INSERT CLASSES_STUDENT ===
        # Distribute 12 students across 3 classes (4 students per class)
        classes_student_data = [
            # Class CS101 (4 students)
            ("CS101-2024", "SV001"),  # Trần Thanh Thuận
            ("CS101-2024", "SV002"),
            ("CS101-2024", "SV003"),
            ("CS101-2024", "SV004"),
            
            # Class CS201 (4 students)
            ("CS201-2024", "SV005"),
            ("CS201-2024", "SV006"),
            ("CS201-2024", "SV007"),
            ("CS201-2024", "SV008"),
            
            # Class AI301 (4 students)
            ("AI301-2024", "SV009"),
            ("AI301-2024", "SV010"),
            ("AI301-2024", "SV011"),
            ("AI301-2024", "SV012"),
        ]
        
        cursor.executemany("""
            INSERT INTO classes_student (class_id, student_code)
            VALUES (?, ?)
        """, classes_student_data)
        
        conn.commit()
        print("✅ Demo data đã được seed thành công!")
        print("   📧 Admin: admin@ut.edu.vn / 123456")
        print("   📧 Teachers: thuongpx@ut.edu.vn, tramnp@ut.edu.vn, hunglv@ut.edu.vn / 123456")
        print("   📧 Students: thuantt0354@ut.edu.vn (Trần Thanh Thuận) + 11 others / 123456")
        print("   👥 Total: 1 Admin, 3 Teachers, 12 Students")
        
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
