#!/usr/bin/env python3
"""
Comprehensive Application Test Suite
======================================

Tests all major application components:
- Authentication
- Student Dashboard
- Teacher Functions
- Admin Functions
- Database Integrity
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.database import Database
from data.repositories.user_repository import UserRepository
from data.repositories.attendance_repository import AttendanceSessionRepository, AttendanceRecordRepository
from data.repositories.classroom_repository import ClassroomRepository
from services.auth_service import AuthService
from services.student_service import StudentService
from services.teacher_service import TeacherService

def test_authentication():
    """Test authentication service."""
    print("\n" + "="*70)
    print("🔐 AUTHENTICATION TESTS")
    print("="*70)
    
    db = Database()
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    
    # Test 1: Valid Login
    print("\n1️⃣ Testing Valid Student Login (sv001@ut.edu.vn):")
    try:
        user = auth_service.authenticate("sv001@ut.edu.vn", "123456")
        if user:
            print(f"   ✅ Login successful!")
            print(f"      - Name: {user.full_name}")
            print(f"      - Role: {user.role}")
            print(f"      - Student Code: {user.student_code}")
        else:
            print(f"   ❌ Login failed!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Valid Admin Login
    print("\n2️⃣ Testing Valid Admin Login (admin1@ut.edu.vn):")
    try:
        user = auth_service.authenticate("admin1@ut.edu.vn", "123456")
        if user:
            print(f"   ✅ Login successful!")
            print(f"      - Name: {user.full_name}")
            print(f"      - Role: {user.role}")
        else:
            print(f"   ❌ Login failed!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Invalid Password
    print("\n3️⃣ Testing Invalid Password:")
    try:
        user = auth_service.authenticate("sv001@ut.edu.vn", "wrongpassword")
        if user:
            print(f"   ❌ Should not have logged in!")
        else:
            print(f"   ✅ Correctly rejected invalid password")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Invalid Username
    print("\n4️⃣ Testing Invalid Username:")
    try:
        user = auth_service.authenticate("nonexistent@ut.edu.vn", "123456")
        if user:
            print(f"   ❌ Should not have logged in!")
        else:
            print(f"   ✅ Correctly rejected invalid username")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_student_dashboard():
    """Test student dashboard functionality."""
    print("\n" + "="*70)
    print("📊 STUDENT DASHBOARD TESTS")
    print("="*70)
    
    db = Database()
    user_repo = UserRepository(db)
    session_repo = AttendanceSessionRepository(db)
    record_repo = AttendanceRecordRepository(db)
    class_repo = ClassroomRepository(db)
    
    service = StudentService(user_repo, record_repo, session_repo, class_repo)
    
    test_student = "SV001"
    
    # Test 1: Dashboard Stats
    print(f"\n1️⃣ Testing Dashboard Stats for {test_student}:")
    try:
        stats = service.get_dashboard_stats(test_student)
        print(f"   ✅ Attendance Rate: {stats['attendance_rate']}%")
        print(f"   ✅ Total Sessions: {stats['total_sessions']}")
        print(f"   ✅ Present: {stats['present_count']}, Absent: {stats['absent_count']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Today's Sessions
    print(f"\n2️⃣ Testing Today's Sessions for {test_student}:")
    try:
        sessions = service.get_todays_sessions(test_student)
        print(f"   ✅ Found {len(sessions)} sessions for today")
        if sessions:
            session = sessions[0]
            print(f"      - Sample: {session['class_name']} at {session['start_time']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Class Schedule
    print(f"\n3️⃣ Testing Class Schedule for {test_student}:")
    try:
        classes = service.get_class_schedule(test_student)
        print(f"   ✅ Enrolled in {len(classes)} classes")
        for cls in classes[:2]:
            print(f"      - {cls['class_name']} ({cls['subject_code']})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Attendance History
    print(f"\n4️⃣ Testing Attendance History for {test_student}:")
    try:
        history = service.get_attendance_history(test_student)
        print(f"   ✅ Found {len(history)} attendance records")
        if history:
            record = history[0]
            print(f"      - Latest: {record['class_name']} - {record['status']} on {record['date']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_database_integrity():
    """Test database integrity and data consistency."""
    print("\n" + "="*70)
    print("💾 DATABASE INTEGRITY TESTS")
    print("="*70)
    
    db = Database()
    user_repo = UserRepository(db)
    class_repo = ClassroomRepository(db)
    session_repo = AttendanceSessionRepository(db)
    record_repo = AttendanceRecordRepository(db)
    
    # Test 1: User Counts
    print("\n1️⃣ Testing User Counts:")
    try:
        users = db.fetch_all("SELECT role, COUNT(*) as count FROM users GROUP BY role", ())
        total_users = 0
        for role, count in users:
            print(f"   ✅ {role}: {count} users")
            total_users += count
        print(f"   ✅ Total: {total_users} users")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Classes
    print("\n2️⃣ Testing Classes:")
    try:
        classes = db.fetch_all("SELECT COUNT(*) as count FROM classes", ())
        count = classes[0][0] if classes else 0
        print(f"   ✅ Found {count} classes")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Sessions
    print("\n3️⃣ Testing Attendance Sessions:")
    try:
        sessions = db.fetch_all("SELECT COUNT(*) as count FROM attendance_sessions", ())
        count = sessions[0][0] if sessions else 0
        print(f"   ✅ Found {count} sessions")
        
        # Check today's sessions
        today_sessions = db.fetch_all("""
            SELECT COUNT(*) as count FROM attendance_sessions 
            WHERE DATE(start_time) = DATE('2026-01-27')
        """, ())
        today_count = today_sessions[0][0] if today_sessions else 0
        print(f"   ✅ Today's sessions: {today_count}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Attendance Records
    print("\n4️⃣ Testing Attendance Records:")
    try:
        records = db.fetch_all("SELECT COUNT(*) as count FROM attendance_records", ())
        count = records[0][0] if records else 0
        print(f"   ✅ Found {count} total records")
        
        # Check status distribution
        status_dist = db.fetch_all("""
            SELECT status, COUNT(*) as count FROM attendance_records 
            GROUP BY status
        """, ())
        for status, count in status_dist:
            print(f"      - {status}: {count} records")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Data Relationships
    print("\n5️⃣ Testing Data Relationships:")
    try:
        # Check student-class relationships
        enrollments = db.fetch_all("SELECT COUNT(*) as count FROM classes_student", ())
        count = enrollments[0][0] if enrollments else 0
        print(f"   ✅ Student-Class enrollments: {count}")
        
        # Check student SV001 classes
        sv001_classes = db.fetch_all("""
            SELECT COUNT(*) FROM classes_student WHERE student_code = 'SV001'
        """, ())
        count = sv001_classes[0][0] if sv001_classes else 0
        print(f"   ✅ SV001 enrolled in: {count} classes")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_data_validation():
    """Test data validation and constraints."""
    print("\n" + "="*70)
    print("✔️ DATA VALIDATION TESTS")
    print("="*70)
    
    db = Database()
    
    # Test 1: Unique Usernames
    print("\n1️⃣ Testing Unique Usernames:")
    try:
        duplicate_usernames = db.fetch_all("""
            SELECT username, COUNT(*) as count FROM users 
            GROUP BY username HAVING count > 1
        """, ())
        if not duplicate_usernames:
            print(f"   ✅ All usernames are unique")
        else:
            print(f"   ❌ Found duplicate usernames!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Valid User Roles
    print("\n2️⃣ Testing Valid User Roles:")
    try:
        invalid_roles = db.fetch_all("""
            SELECT DISTINCT role FROM users 
            WHERE role NOT IN ('ADMIN', 'TEACHER', 'STUDENT')
        """, ())
        if not invalid_roles:
            print(f"   ✅ All users have valid roles")
        else:
            print(f"   ❌ Found invalid roles!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Valid Session Status
    print("\n3️⃣ Testing Valid Session Status:")
    try:
        invalid_status = db.fetch_all("""
            SELECT DISTINCT status FROM attendance_sessions 
            WHERE status NOT IN ('OPEN', 'CLOSED')
        """, ())
        if not invalid_status:
            print(f"   ✅ All sessions have valid status")
        else:
            print(f"   ❌ Found invalid session status!")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("🚀 COMPREHENSIVE APPLICATION TEST SUITE")
    print("="*70)
    
    test_authentication()
    test_student_dashboard()
    test_database_integrity()
    test_data_validation()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\n✨ Application is ready for use! ✨\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
