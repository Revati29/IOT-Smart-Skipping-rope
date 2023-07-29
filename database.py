import sqlite3

# Database connection
def get_db():
    conn = sqlite3.connect('database.db')
    return conn

# Create a table to store practice session data
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jump_count INTEGER,
            set_count INTEGER,
            set_duration INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Add practice session data to the database
def add_session_data(jump_count, set_count, set_duration):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sessions (jump_count, set_count, set_duration) VALUES (?, ?, ?)',
                   (jump_count, set_count, set_duration))
    conn.commit()
    conn.close()

# Fetch previous practice sessions from the database
def get_previous_sessions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions ORDER BY timestamp DESC LIMIT 1')
    sessions = cursor.fetchall()
    conn.close()
    return sessions
