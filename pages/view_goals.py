import streamlit as st
from database.db import get_connection

def show():
    st.header("All Goals")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, type, progress, deadline FROM goals")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        st.write(f"**{row[1]}** ({row[2]}) - {row[3]}% complete - Deadline: {row[4]}")