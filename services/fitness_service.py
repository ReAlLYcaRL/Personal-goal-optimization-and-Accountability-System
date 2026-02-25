from database.db import get_connection
from datetime import datetime

def log_weight(goal_id, weight):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO weight_logs (goal_id, date, weight)
    VALUES (?, ?, ?)
    """, (goal_id, str(datetime.today().date()), weight))
    conn.commit()
    conn.close()

def get_weights(goal_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT weight FROM weight_logs WHERE goal_id=?", (goal_id,))
    data = [row[0] for row in cursor.fetchall()]
    conn.close()
    return data

def get_weight_dates(goal_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date FROM weight_logs WHERE goal_id=?", (goal_id,))
    data = [row[0] for row in cursor.fetchall()]
    conn.close()
    return data