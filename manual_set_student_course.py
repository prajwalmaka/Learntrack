import sqlite3
import os

DB_PATH = os.path.join('instance', 'learntrack.db')

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Prompt for course_id
    course_id = input('Enter the course_id to assign to all students with NULL course_id: ').strip()
    if not course_id.isdigit():
        print('Invalid course_id. Must be an integer.')
        return
    course_id = int(course_id)

    # Update students
    cursor.execute('UPDATE user SET course_id = ? WHERE role = ? AND (course_id IS NULL OR course_id = "")', (course_id, 'student'))
    conn.commit()
    print(f'Updated all students with NULL course_id to course_id={course_id}.')

    # Show how many were updated
    cursor.execute('SELECT COUNT(*) FROM user WHERE role = ? AND course_id = ?', ('student', course_id))
    count = cursor.fetchone()[0]
    print(f'Total students with course_id={course_id}: {count}')

    conn.close()

if __name__ == '__main__':
    main() 