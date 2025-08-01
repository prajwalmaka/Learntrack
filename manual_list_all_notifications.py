import sqlite3
import os

DB_PATH = os.path.join('instance', 'learntrack.db')

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, user_id, message, link, is_read, timestamp, type FROM notification ORDER BY timestamp DESC')
    notifications = cursor.fetchall()
    if not notifications:
        print('No notifications found in the database.')
    else:
        print('All notifications:')
        for n in notifications:
            print(f'ID: {n[0]}, User ID: {n[1]}, Message: {n[2]}, Link: {n[3]}, Read: {n[4]}, Time: {n[5]}, Type: {n[6]}')
    conn.close()

if __name__ == '__main__':
    main() 