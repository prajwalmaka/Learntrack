import sqlite3
import os

DB_PATH = os.path.join('instance', 'learntrack.db')

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    user_id = input('Enter user_id (student): ').strip()
    if not user_id.isdigit():
        print('Invalid user_id.')
        return
    user_id = int(user_id)
    cursor.execute('SELECT id, message, link, is_read, timestamp, type FROM notification WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
    notifications = cursor.fetchall()
    if not notifications:
        print(f'No notifications found for user_id={user_id}.')
    else:
        print(f'Notifications for user_id={user_id}:')
        for n in notifications:
            print(f'ID: {n[0]}, Message: {n[1]}, Link: {n[2]}, Read: {n[3]}, Time: {n[4]}, Type: {n[5]}')
    conn.close()

if __name__ == '__main__':
    main() 