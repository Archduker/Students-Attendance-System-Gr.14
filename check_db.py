import sqlite3

conn = sqlite3.connect('database/attendance.db')
cursor = conn.cursor()

# Check total users
cursor.execute('SELECT COUNT(*) FROM users')
print('Total users:', cursor.fetchone()[0])

# Show sample users
cursor.execute('SELECT username, full_name, role FROM users LIMIT 5')
print('\nSample users:')
for row in cursor.fetchall():
    print(f'  {row[0]} - {row[1]} ({row[2]})')

conn.close()
