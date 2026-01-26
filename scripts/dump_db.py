
import sqlite3
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'attendance.db')

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def print_table(cursor, table_name):
    print(f"\n{'='*20} TABLE: {table_name} {'='*20}")
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            print("(Empty)")
            return

        # Get column names
        names = [description[0] for description in cursor.description]
        
        # Simple straightforward printing
        # Print Header
        header = " | ".join(f"{name:<15}" for name in names)
        print(header)
        print("-" * len(header))
        
        for row in rows:
            # Convert each item to string and truncate if too long
            formatted_row = []
            for item in row:
                s = str(item)
                if len(s) > 20:
                    s = s[:17] + "..."
                formatted_row.append(s)
            
            print(" | ".join(f"{item:<15}" for item in formatted_row))
            
    except Exception as e:
        print(f"Error reading {table_name}: {e}")

def dump_all():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    tables = ["users", "classes", "classes_student", "attendance_sessions", "attendance_records"]
    
    for table in tables:
        print_table(cursor, table)
        
    conn.close()

if __name__ == "__main__":
    dump_all()
