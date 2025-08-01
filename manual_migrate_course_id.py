import sqlite3
import os

DB_PATH = os.path.join('instance', 'learntrack.db')

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Add course_id column to user table if it doesn't exist
    if not column_exists(cursor, 'user', 'course_id'):
        print('Adding course_id column to user table...')
        cursor.execute('ALTER TABLE user ADD COLUMN course_id INTEGER')
        conn.commit()
        print('course_id column added.')
    else:
        print('course_id column already exists in user table.')

    conn.close()

if __name__ == '__main__':
    main() 