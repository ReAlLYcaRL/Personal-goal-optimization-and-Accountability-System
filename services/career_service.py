from database.db import get_connection

def add_certification(goal_id, cert, issuer, status="Completed"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO certifications (goal_id, cert_name, issuer, status)
    VALUES (?, ?, ?, ?)
    """, (goal_id, cert, issuer, status))
    conn.commit()
    conn.close()

def update_certification(cert_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE certifications
    SET status=?
    WHERE id=?
    """, (status, cert_id))
    conn.commit()
    conn.close()

def update_linkedin(goal_id, target_connections, current_connections):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM linkedin_stats WHERE goal_id=?", (goal_id,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("""
        UPDATE linkedin_stats
        SET target_connections=?, current_connections=?
        WHERE goal_id=?
        """, (target_connections, current_connections, goal_id))
    else:
        cursor.execute("""
        INSERT INTO linkedin_stats (goal_id, target_connections, current_connections)
        VALUES (?, ?, ?)
        """, (goal_id, target_connections, current_connections))
    conn.commit()
    conn.close()