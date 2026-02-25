import streamlit as st
from services.career_service import add_certification, update_linkedin

def show():
    st.header("Career Goals Tracker")
    goal_id = st.number_input("Enter Goal ID", min_value=1)
    cert_name = st.text_input("Add Certification")
    issuer = st.text_input("Issuer")

    if st.button("Add Certification"):
        add_certification(goal_id, cert_name, issuer)
        st.success("Certification added!")

    target_connections = st.number_input("Target LinkedIn Connections", min_value=0)
    current_connections = st.number_input("Current Connections", min_value=0)

    if st.button("Update LinkedIn Stats"):
        update_linkedin(goal_id, target_connections, current_connections)
        st.success("LinkedIn stats updated!")