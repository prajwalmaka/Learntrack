import sqlite3
import os

DB_PATH = os.path.join('instance', 'learntrack.db')

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print('List enrollments by:')
    print('1. class_id')
    print('2. student_id')
    choice = input('Enter 1 or 2: ').strip()
    if choice == '1':
        class_id = input('Enter class_id: ').strip()
        if not class_id.isdigit():
            print('Invalid class_id.')
            return
        class_id = int(class_id)
        cursor.execute('SELECT id, student_id, class_id, enrolled_at FROM enrollment WHERE class_id = ?', (class_id,))
        enrollments = cursor.fetchall()
        print(f'Enrollments for class_id={class_id}:')
        for e in enrollments:
            print(f'Enrollment ID: {e[0]}, Student ID: {e[1]}, Class ID: {e[2]}, Enrolled At: {e[3]}')
        print(f'Total: {len(enrollments)}')
    elif choice == '2':
        student_id = input('Enter student_id: ').strip()
        if not student_id.isdigit():
            print('Invalid student_id.')
            return
        student_id = int(student_id)
        cursor.execute('SELECT id, student_id, class_id, enrolled_at FROM enrollment WHERE student_id = ?', (student_id,))
        enrollments = cursor.fetchall()
        print(f'Enrollments for student_id={student_id}:')
        for e in enrollments:
            print(f'Enrollment ID: {e[0]}, Student ID: {e[1]}, Class ID: {e[2]}, Enrolled At: {e[3]}')
        print(f'Total: {len(enrollments)}')
    else:
        print('Invalid choice.')
    conn.close()

if __name__ == '__main__':
    main() 