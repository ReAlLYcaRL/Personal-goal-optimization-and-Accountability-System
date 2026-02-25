import streamlit as st
from services.fitness_service import log_weight, get_weights, get_weight_dates
from utils.analytics import calculate_streak, detect_stagnation

def show():
    st.header("Fitness Goals Tracker")
    goal_id = st.number_input("Enter Goal ID", min_value=1)
    new_weight = st.number_input("Log Today's Weight", min_value=0.0)

    if st.button("Log Weight"):
        log_weight(goal_id, new_weight)
        st.success("Weight logged!")

    weights = get_weights(goal_id)
    dates = get_weight_dates(goal_id)
    if weights:
        st.write(f"Weight History: {weights}")
        st.write(f"Current Streak: {calculate_streak(dates)} days")
        if detect_stagnation(weights):
            st.warning("Your weight has stagnated! Consider dietary adjustment.")