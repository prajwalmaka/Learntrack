import sqlite3
import os

DB_PATH = os.path.join('instance', 'learntrack.db')

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM course')
    courses = cursor.fetchall()
    if not courses:
        print('No courses found.')
    else:
        print('Course IDs and Names:')
        for course in courses:
            print(f'ID: {course[0]}, Name: {course[1]}')
    conn.close()

if __name__ == '__main__':
    main() 