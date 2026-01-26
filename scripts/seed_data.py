
import sqlite3
import random
from datetime import datetime, timedelta
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.enums import UserRole, AttendanceMethod, AttendanceStatus
from core.models.attendance_session import SessionStatus

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'attendance.db')

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def seed_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    print(f"Connecting to database at {DB_PATH}")

    # 1. Classes
    classes = [
        {"id": "SE_001", "name": "Software Engineer", "subject": "SE101"},
        {"id": "ML_001", "name": "Machine Learning", "subject": "AI101"},
        {"id": "BDA_001", "name": "Big Data Analyst", "subject": "DA101"}
    ]
    
    # Teacher (ensure at least one teacher exists to own these classes)
    teacher_code = "GV001"
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, password_hash, full_name, role, teacher_code) VALUES (?, ?, ?, ?, ?, ?)",
                   (999, "teacher1", "hash", "Teacher One", "TEACHER", teacher_code))

    print("Seeding Classes...")
    for cls in classes:
        cursor.execute("INSERT OR REPLACE INTO classes (class_id, class_name, subject_code, teacher_code) VALUES (?, ?, ?, ?)",
                       (cls["id"], cls["name"], cls["subject"], teacher_code))

    # 2. Students & Enrollments
    print("Seeding Students and Enrollments...")
    # Clean up existing students for these classes to avoid messy duplicates if re-run (optional strategy)
    # For now, we just insert or ignore.

    first_names = ["An", "Binh", "Chi", "Dung", "Giang", "Hieu", "Khanh", "Lan", "Minh", "Nam", "Phuong", "Quan", "Son", "Thao", "Tuan", "Vy", "Yen"]
    last_names = ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Huynh", "Phan", "Vu", "Vo", "Dang", "Bui", "Do"]
    
    student_ids = []

    start_id = 1000
    for cls in classes:
        for i in range(12):
            s_id = f"SV_{cls['id']}_{i+1:02d}"
            name = f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(first_names)}"
            
            # Create User/Student
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO users (user_id, username, password_hash, full_name, role, student_code) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (start_id, s_id, "hash", name, "STUDENT", s_id))
            except Exception as e:
                pass # ID might conflict if randomized, but here we are sequential
            
            # Enroll
            cursor.execute("INSERT OR IGNORE INTO classes_student (class_id, student_code) VALUES (?, ?)",
                           (cls["id"], s_id))
            
            student_ids.append(s_id)
            start_id += 1

    # 3. Sessions (10 weeks back)
    print("Seeding Sessions and Attendance...")
    today = datetime.now()
    
    for cls in classes:
        # Create 10 sessions, 1 per week, going back
        for w in range(10):
            # Session date: today minus w weeks
            session_date = today - timedelta(weeks=w)
            # Make sure it's a weekday? Simplified.
            
            session_id = f"SESS_{cls['id']}_W{w+1}"
            start_time = session_date.replace(hour=8, minute=0, second=0, microsecond=0)
            end_time = session_date.replace(hour=11, minute=0, second=0, microsecond=0)
            
            # Latest session might be OPEN, older are CLOSED
            status = "CLOSED" 
            
            cursor.execute("""
                INSERT OR REPLACE INTO attendance_sessions 
                (session_id, class_id, start_time, end_time, attendance_method, status, qr_window_minutes, late_window_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (session_id, cls["id"], start_time.isoformat(), end_time.isoformat(), "QR", status, 15, 30))

            # 4. Attendance Records (for 9 weeks past, skip the very recent one or just do all 9)
            # Request says: "đã điểm danh trong 9 tuần vừa gòi" (attended in the past 9 weeks)
            if w > 0: # Skip current week (week 0) or do 1-9? "tuần này đếm ngược 10 tuần... điểm danh 9 tuần" -> Latest week might be empty?
                # Let's seed w=1 to w=9. w=0 is "this week", maybe no data yet?
                # Or just seed all 10. Request says "already attended in past 9 weeks".
                
                # Get students for this class
                cursor.execute("SELECT student_code FROM classes_student WHERE class_id = ?", (cls["id"],))
                students_in_class = [row[0] for row in cursor.fetchall()]
                
                for s_code in students_in_class:
                    # Random status
                    rand = random.random()
                    ATTENDANCE_STATUS_PRESENT = "PRESENT"
                    ATTENDANCE_STATUS_ABSENT = "ABSENT"
                    
                    if rand < 0.9:
                        att_status = ATTENDANCE_STATUS_PRESENT
                        check_in = start_time + timedelta(minutes=random.randint(0, 30))
                    else:
                        att_status = ATTENDANCE_STATUS_ABSENT
                        check_in = None
                    
                    rec_id = f"REC_{session_id}_{s_code}"
                    
                    cursor.execute("""
                        INSERT OR REPLACE INTO attendance_records
                        (record_id, session_id, student_code, status, attendance_time)
                        VALUES (?, ?, ?, ?, ?)
                    """, (rec_id, session_id, s_code, att_status, check_in.isoformat() if check_in else None))

    conn.commit()
    conn.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_data()
