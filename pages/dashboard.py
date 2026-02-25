import streamlit as st
from database.db import get_connection

def show():
    st.title("📊 Dashboard")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM goals")
    total_goals = cursor.fetchone()[0]
    conn.close()
    st.metric("Total Goals", total_goals)