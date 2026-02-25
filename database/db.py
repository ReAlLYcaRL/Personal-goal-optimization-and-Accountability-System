import sqlite3

DB_NAME = "vision_board.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Goals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        type TEXT,
        description TEXT,
        start_weight REAL,
        target_weight REAL,
        deadline TEXT,
        progress INTEGER DEFAULT 0,
        calorie_target INTEGER,
        image_path TEXT,
        extension_count INTEGER DEFAULT 0
    )
    """)

    # Weight logs for fitness goals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weight_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_id INTEGER,
        date TEXT,
        weight REAL
    )
    """)

    # Certifications for career goals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_id INTEGER,
        cert_name TEXT,
        issuer TEXT,
        status TEXT
    )
    """)

    # LinkedIn stats for job landing goals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS linkedin_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_id INTEGER,
        target_connections INTEGER,
        current_connections INTEGER
    )
    """)

    conn.commit()
    conn.close()