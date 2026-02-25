import streamlit as st
from database.db import get_connection

def show():
    st.header("Create a New Goal")
    title = st.text_input("Goal Title")
    type_choice = st.selectbox("Goal Type", ["Fitness", "Career"])
    description = st.text_area("Description")
    deadline = st.date_input("Deadline")

    if type_choice == "Fitness":
        start_weight = st.number_input("Start Weight (kg)", min_value=0.0)
        target_weight = st.number_input("Target Weight (kg)", min_value=0.0)
    else:
        start_weight = target_weight = 0.0

    if st.button("Add Goal"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO goals (title, type, description, start_weight, target_weight, deadline)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (title, type_choice, description, start_weight, target_weight, str(deadline)))
        conn.commit()
        conn.close()
        st.success(f"Goal '{title}' added!")