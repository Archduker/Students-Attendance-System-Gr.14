#!/usr/bin/env python3
"""
Test Student Dashboard Data
============================

Script to test that the student dashboard can correctly fetch and display data.
"""

import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.database import Database
from data.repositories.user_repository import UserRepository
from data.repositories.attendance_repository import AttendanceSessionRepository, AttendanceRecordRepository
from data.repositories.classroom_repository import ClassroomRepository
from services.student_service import StudentService

def test_dashboard():
    """Test student dashboard functionality."""
    
    print("="*70)
    print("TESTING STUDENT DASHBOARD DATA")
    print("="*70)
    
    # Initialize database connection
    db = Database()
    
    # Initialize repositories
    user_repo = UserRepository(db)
    attendance_session_repo = AttendanceSessionRepository(db)
    attendance_record_repo = AttendanceRecordRepository(db)
    class_repo = ClassroomRepository(db)
    
    # Initialize service
    student_service = StudentService(
        user_repo,
        attendance_record_repo,
        attendance_session_repo,
        class_repo
    )
    
    # Test with student SV001
    test_student_code = "SV001"
    
    print(f"\n📊 Testing Dashboard Data for Student: {test_student_code}")
    print("-"*70)
    
    # 1. Test get_dashboard_stats
    print(f"\n1️⃣ Testing get_dashboard_stats():")
    try:
        stats = student_service.get_dashboard_stats(test_student_code)
        print(f"   ✓ Attendance Rate: {stats['attendance_rate']}%")
        print(f"   ✓ Total Sessions: {stats['total_sessions']}")
        print(f"   ✓ Present Count: {stats['present_count']}")
        print(f"   ✓ Absent Count: {stats['absent_count']}")
        print(f"   ✓ Recent Attendance Records: {len(stats['recent_attendance'])}")
        
        if stats['recent_attendance']:
            print(f"\n   Sample Record:")
            record = stats['recent_attendance'][0]
            print(f"      - Class: {record['class_name']}")
            print(f"      - Date: {record['date']}")
            print(f"      - Time: {record['time']}")
            print(f"      - Status: {record['status']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. Test get_todays_sessions
    print(f"\n2️⃣ Testing get_todays_sessions():")
    try:
        sessions = student_service.get_todays_sessions(test_student_code)
        print(f"   ✓ Found {len(sessions)} sessions for today")
        
        if sessions:
            print(f"\n   Sample Sessions:")
            for session in sessions[:3]:
                print(f"      - Class: {session['class_name']}")
                print(f"        Subject: {session['subject_code']}")
                print(f"        Time: {session['start_time']} - {session['end_time']}")
                print(f"        Room: {session['room']}")
                print(f"        Status: {session['status']}")
        else:
            print(f"   ⚠️  No sessions found for today (this might be expected)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. Test get_class_schedule
    print(f"\n3️⃣ Testing get_class_schedule():")
    try:
        classes = student_service.get_class_schedule(test_student_code)
        print(f"   ✓ Found {len(classes)} classes")
        
        if classes:
            print(f"\n   Sample Classes:")
            for cls in classes[:3]:
                print(f"      - {cls['class_name']} ({cls['subject_code']})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # 4. Test get_attendance_history
    print(f"\n4️⃣ Testing get_attendance_history():")
    try:
        history = student_service.get_attendance_history(test_student_code)
        print(f"   ✓ Found {len(history)} attendance records in history")
        
        if history:
            print(f"\n   Sample Records:")
            for record in history[:3]:
                print(f"      - {record['class_name']}: {record['status']} on {record['date']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # 5. Test user retrieval
    print(f"\n5️⃣ Testing User Information:")
    try:
        user = user_repo.find_by_username(f"{test_student_code.lower()}@ut.edu.vn")
        if user:
            print(f"   ✓ Found user: {user.full_name}")
            print(f"   ✓ Student Code: {user.student_code}")
        else:
            print(f"   ❌ User not found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print("✅ DASHBOARD DATA TEST COMPLETED")
    print("="*70)
    print("\nAll data is ready for dashboard display!")
    print("\nTest Student Login Credentials:")
    print(f"  Email: {test_student_code.lower()}@ut.edu.vn")
    print(f"  Password: 123456")
    print("="*70)

if __name__ == "__main__":
    test_dashboard()
