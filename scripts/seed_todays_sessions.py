#!/usr/bin/env python3
"""
Seed Today's Sessions
=====================

Script to add attendance sessions for today to test dashboard functionality.
This allows the student dashboard to display live sessions.
"""

import sqlite3
import random
from datetime import datetime, timedelta
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'attendance.db')

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def seed_todays_sessions():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print(f"Connecting to database at {DB_PATH}")
    
    # Get all classes
    cursor.execute("SELECT class_id, class_name, subject_code FROM classes")
    classes = cursor.fetchall()
    
    # Get all student codes
    cursor.execute("SELECT student_code FROM users WHERE role = 'STUDENT'")
    students = [row[0] for row in cursor.fetchall()]
    
    today = datetime.now().date()
    print(f"\n✓ Adding sessions for today: {today}")
    
    # ============================================================================
    # Create Today's Sessions (3 sessions spread throughout the day)
    # ============================================================================
    print("\nCreating Today's Attendance Sessions...")
    
    session_times = [
        (8, 0, 9, 0),      # 8:00 AM - 9:00 AM
        (10, 0, 11, 30),   # 10:00 AM - 11:30 AM
        (13, 0, 14, 30),   # 1:00 PM - 2:30 PM
    ]
    
    all_todays_sessions = []
    
    for idx, (class_id, class_name, subject_code) in enumerate(classes):
        # Create 1-3 sessions for each class today
        num_sessions = random.randint(1, 3)
        selected_times = random.sample(session_times, min(num_sessions, len(session_times)))
        
        for time_idx, (start_h, start_m, end_h, end_m) in enumerate(selected_times):
            session_id = f"SESS_{class_id}_TODAY_{time_idx+1:02d}"
            
            start_time = datetime.combine(today, datetime.min.time()).replace(hour=start_h, minute=start_m, second=0)
            end_time = datetime.combine(today, datetime.min.time()).replace(hour=end_h, minute=end_m, second=0)
            
            cursor.execute("""
                INSERT OR REPLACE INTO attendance_sessions 
                (session_id, class_id, start_time, end_time, attendance_method, status, qr_window_minutes, late_window_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (session_id, class_id, start_time.isoformat(), end_time.isoformat(), "QR", "OPEN", 15, 30))
            
            all_todays_sessions.append({
                "session_id": session_id,
                "class_id": class_id,
                "start_time": start_time
            })
            
            print(f"  ✓ Created session: {session_id} ({class_name}) at {start_h:02d}:{start_m:02d}")
    
    # ============================================================================
    # Create Attendance Records for Today's Sessions
    # ============================================================================
    print(f"\nCreating Attendance Records for {len(all_todays_sessions)} sessions...")
    
    attendance_count = 0
    for session in all_todays_sessions:
        for student_code in students:
            # Random status: 90% present, 10% absent
            is_present = random.random() < 0.9
            
            if is_present:
                # Check in time: random time within the session (0-15 minutes after start)
                attendance_time = session["start_time"] + timedelta(minutes=random.randint(0, 15))
                status = "PRESENT"
            else:
                attendance_time = None
                status = "ABSENT"
            
            record_id = f"REC_TODAY_{session['session_id']}_{student_code}"
            
            # Check if record already exists
            cursor.execute(
                "SELECT record_id FROM attendance_records WHERE session_id = ? AND student_code = ?",
                (session["session_id"], student_code)
            )
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO attendance_records
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
    print("TODAY'S SESSIONS SEEDING COMPLETED!")
    print("="*70)
    print(f"\nSummary:")
    print(f"  • {len(all_todays_sessions)} Attendance Sessions created for today")
    print(f"  • {attendance_count} Attendance Records created")
    print(f"\nToday's Date: {today}")
    print("="*70)

if __name__ == "__main__":
    seed_todays_sessions()
