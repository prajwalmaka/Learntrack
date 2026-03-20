import sqlite3
import os

DB_PATH = os.path.join('instance', 'learntrack.db')

def table_exists(cursor, table):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cursor.fetchone() is not None

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create notification table if not exists
    if not table_exists(cursor, 'notification'):
        print('Creating notification table...')
        cursor.execute('''
            CREATE TABLE notification (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message VARCHAR(255) NOT NULL,
                link VARCHAR(255),
                is_read BOOLEAN DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                type VARCHAR(20),
                FOREIGN KEY(user_id) REFERENCES user(id)
            )
        ''')
        conn.commit()
        print('Notification table created.')
    else:
        print('notification table already exists.')

    # Create message table if not exists
    if not table_exists(cursor, 'message'):
        print('Creating message table...')
        cursor.execute('''
            CREATE TABLE message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT 0,
                FOREIGN KEY(sender_id) REFERENCES user(id),
                FOREIGN KEY(receiver_id) REFERENCES user(id)
            )
        ''')
        conn.commit()
        print('Message table created.')
    else:
        print('message table already exists.')

    conn.close()

if __name__ == '__main__':
    main() 