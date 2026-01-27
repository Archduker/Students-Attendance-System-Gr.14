
import sqlite3
import random
from datetime import datetime, timedelta
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from services.security_service import SecurityService
    security = SecurityService()
    default_password_hash = security.hash_password("123456")
except ImportError:
    # Fallback: use bcrypt directly with try-except
    try:
        import bcrypt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw("123456".encode("utf-8"), salt)
        default_password_hash = hashed.decode("utf-8")
    except ImportError:
        # Last resort: use a pre-hashed password (for testing purposes)
        # This is a bcrypt hash of "123456" 
        default_password_hash = "$2b$12$HJnLZ1osgra9tZ4i7J/aPun5LEFzg7tzkp7W84z8xEeGrOlGljUBy"

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'attendance.db')

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def seed_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Default password for all users: "123456" (pre-hashed with bcrypt)
    # Hash of "123456" using bcrypt

    print(f"Connecting to database at {DB_PATH}")
    
    # Vietnamese names for realistic data
    last_names = ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Huynh", "Phan", "Vu", "Vo", "Dang", "Bui", "Do"]
    first_names = ["An", "Binh", "Chi", "Dung", "Giang", "Hieu", "Khanh", "Lan", "Minh", "Nam", "Phuong", "Quan"]

    # ============================================================================
    # 1. SEED ADMINS (3 admins)
    # ============================================================================
    print("Creating 3 Admins...")
    admins = [
        {
            "admin_id": "AD001",
            "username": "admin1@ut.edu.vn",
            "email": "admin1@ut.edu.vn",
            "full_name": "Tran Admin One"
        },
        {
            "admin_id": "AD002",
            "username": "admin2@ut.edu.vn",
            "email": "admin2@ut.edu.vn",
            "full_name": "Nguyen Admin Two"
        },
        {
            "admin_id": "AD003",
            "username": "admin3@ut.edu.vn",
            "email": "admin3@ut.edu.vn",
            "full_name": "Le Admin Three"
        }
    ]
    
    admin_ids = []
    for i, admin in enumerate(admins, start=1):
        cursor.execute("""
            INSERT OR REPLACE INTO users 
            (username, password_hash, full_name, email, role, admin_id, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (admin["username"], default_password_hash, admin["full_name"], admin["email"], "ADMIN", admin["admin_id"], 1))
        print(f"  ✓ Created Admin: {admin['username']} (password: 123456)")

    # ============================================================================
    # 2. SEED TEACHERS (3 teachers)
    # ============================================================================
    print("\nCreating 3 Teachers...")
    teachers = [
        {
            "teacher_code": "GV001",
            "username": "gv1@ut.edu.vn",
            "email": "gv1@ut.edu.vn",
            "full_name": "Tran Minh Teacher"
        },
        {
            "teacher_code": "GV002",
            "username": "gv2@ut.edu.vn",
            "email": "gv2@ut.edu.vn",
            "full_name": "Hoang Nam Teacher"
        },
        {
            "teacher_code": "GV003",
            "username": "gv3@ut.edu.vn",
            "email": "gv3@ut.edu.vn",
            "full_name": "Nguyen Khanh Teacher"
        }
    ]
    
    for i, teacher in enumerate(teachers, start=1):
        cursor.execute("""
            INSERT OR REPLACE INTO users 
            (username, password_hash, full_name, email, role, teacher_code, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (teacher["username"], default_password_hash, teacher["full_name"], teacher["email"], "TEACHER", teacher["teacher_code"], 1))
        print(f"  ✓ Created Teacher: {teacher['username']} (password: 123456)")

    # ============================================================================
    # 3. SEED STUDENTS (12 students - shared across all 3 classrooms)
    # ============================================================================
    print("\nCreating 12 Students...")
    students = []
    student_codes = []
    
    for i in range(1, 13):
        student_code = f"SV{i:03d}"
        full_name = f"{random.choice(last_names)} {random.choice(first_names)}"
        email = f"sv{i:03d}@ut.edu.vn"
        username = f"sv{i:03d}@ut.edu.vn"
        
        cursor.execute("""
            INSERT OR REPLACE INTO users 
            (username, password_hash, full_name, email, role, student_code, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, default_password_hash, full_name, email, "STUDENT", student_code, 1))
        
        students.append({"student_code": student_code, "full_name": full_name})
        student_codes.append(student_code)
        print(f"  ✓ Created Student: {username} ({full_name}) - password: 123456")

    # ============================================================================
    # 4. SEED CLASSES (3 classes - 1 per teacher)
    # ============================================================================
    print("\nCreating 3 Classes...")
    classes = [
        {
            "class_id": "CS001",
            "class_name": "Introduction to Python",
            "subject_code": "CS101",
            "teacher_code": "GV001"
        },
        {
            "class_id": "CS002",
            "class_name": "Web Development Basics",
            "subject_code": "CS102",
            "teacher_code": "GV002"
        },
        {
            "class_id": "CS003",
            "class_name": "Database Design",
            "subject_code": "CS103",
            "teacher_code": "GV003"
        },
        {
            "class_id": "CS004",
            "class_name": "Advanced Python",
            "subject_code": "CS104",
            "teacher_code": "GV001"
        }
    ]
    
    for cls in classes:
        cursor.execute("""
            INSERT OR REPLACE INTO classes 
            (class_id, class_name, subject_code, teacher_code)
            VALUES (?, ?, ?, ?)
        """, (cls["class_id"], cls["class_name"], cls["subject_code"], cls["teacher_code"]))
        print(f"  ✓ Created Class: {cls['class_name']} ({cls['class_id']}) - Teacher: {cls['teacher_code']}")

    # ============================================================================
    # 5. ENROLL STUDENTS IN CLASSES (all 12 students in each class)
    # ============================================================================
    print("\nEnrolling Students in Classes...")
    for cls in classes:
        for student_code in student_codes:
            cursor.execute("""
                INSERT OR REPLACE INTO classes_student 
                (class_id, student_code)
                VALUES (?, ?)
            """, (cls["class_id"], student_code))
        print(f"  ✓ Enrolled 12 students in {cls['class_id']}")

    # ============================================================================
    # 6. SEED ATTENDANCE SESSIONS (10 sessions per class)
    # ============================================================================
    print("\nCreating 10 Attendance Sessions per Class...")
    today = datetime.now()
    
    all_sessions = []
    
    for cls in classes:
        for week in range(10):
            # Create sessions going back in time (10 weeks ago to today)
            session_date = today - timedelta(weeks=(9 - week))
            
            session_id = f"SESS_{cls['class_id']}_W{week+1:02d}"
            start_time = session_date.replace(hour=8, minute=0, second=0, microsecond=0)
            end_time = session_date.replace(hour=11, minute=0, second=0, microsecond=0)
            
            cursor.execute("""
                INSERT OR REPLACE INTO attendance_sessions 
                (session_id, class_id, start_time, end_time, attendance_method, status, qr_window_minutes, late_window_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (session_id, cls["class_id"], start_time.isoformat(), end_time.isoformat(), "QR", "CLOSED", 15, 30))
            
            all_sessions.append({
                "session_id": session_id,
                "class_id": cls["class_id"],
                "start_time": start_time
            })
        
        print(f"  ✓ Created 10 sessions for {cls['class_id']}")

    # ============================================================================
    # 7. SEED ATTENDANCE RECORDS (90% present, 10% absent)
    # ============================================================================
    print("\nCreating Attendance Records (90% present, 10% absent)...")
    
    attendance_count = 0
    for session in all_sessions:
        for student_code in student_codes:
            # Random status: 90% present, 10% absent
            is_present = random.random() < 0.9
            
            if is_present:
                # Check in time: random time within the session (0-30 minutes after start)
                attendance_time = session["start_time"] + timedelta(minutes=random.randint(0, 30))
                status = "PRESENT"
            else:
                attendance_time = None
                status = "ABSENT"
            
            record_id = f"REC_{session['session_id']}_{student_code}"
            
            cursor.execute("""
                INSERT OR REPLACE INTO attendance_records
                (record_id, session_id, student_code, status, attendance_time)
                VALUES (?, ?, ?, ?, ?)
            """, (record_id, session["session_id"], student_code, status, attendance_time.isoformat() if attendance_time else None))
            
            attendance_count += 1

    print(f"  ✓ Created {attendance_count} attendance records")

    # ============================================================================
    # COMMIT AND SUMMARY
    # ============================================================================
    conn.commit()
    conn.close()
    
    print("\n" + "="*70)
    print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\nSummary:")
    print(f"  • 3 Admins (with email login)")
    print(f"  • 3 Teachers (with email login)")
    print(f"  • 12 Students (with email login)")
    print(f"  • 3 Classes (1 per teacher)")
    print(f"  • 30 Attendance Sessions (10 per class)")
    print(f"  • 360 Attendance Records (12 students × 30 sessions)")
    print(f"\nDefault Login Credentials:")
    print(f"  • Username: Email (user@domain.edu.vn)")
    print(f"  • Password: 123456")
    print(f"\nTest Accounts:")
    print(f"  Admin 1: admin1@ut.edu.vn")
    print(f"  Teacher 1: gv1@ut.edu.vn")
    print(f"  Student 1: sv001@ut.edu.vn")
    print("="*70)

if __name__ == "__main__":
    seed_data()
