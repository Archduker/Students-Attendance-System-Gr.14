import sqlite3

DB_NAME = "database/attendance.db"

def get_connection():
    return sqlite3.connect(DB_NAME)
