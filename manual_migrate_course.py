import sqlite3
import os

DB_PATH = os.path.join('instance', 'learntrack.db')

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())

def table_exists(cursor, table):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cursor.fetchone() is not None

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create course table if not exists
    if not table_exists(cursor, 'course'):
        print('Creating course table...')
        cursor.execute('''
            CREATE TABLE course (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE
            )
        ''')
        conn.commit()
    else:
        print('course table already exists.')

    # 2. Add course_id column to class table if not exists
    if not column_exists(cursor, 'class', 'course_id'):
        print('Adding course_id column to class table...')
        cursor.execute("ALTER TABLE class ADD COLUMN course_id INTEGER NOT NULL DEFAULT 1")
        conn.commit()
    else:
        print('course_id column already exists in class table.')

    # 3. Insert default course if not exists
    cursor.execute("SELECT id FROM course WHERE name=?", ('Default Course',))
    row = cursor.fetchone()
    if row:
        default_course_id = row[0]
        print('Default Course already exists.')
    else:
        print('Inserting Default Course...')
        cursor.execute("INSERT INTO course (name) VALUES (?)", ('Default Course',))
        default_course_id = cursor.lastrowid
        conn.commit()

    # 4. Update all classes to use the default course
    print('Updating all classes to use Default Course...')
    cursor.execute("UPDATE class SET course_id = ?", (default_course_id,))
    conn.commit()

    print('Migration complete.')
    conn.close()

if __name__ == '__main__':
    main() 