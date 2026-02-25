import streamlit as st
from database.db import create_tables
from pages import dashboard, create_goal, view_goals, fitness, career, vision_board

create_tables()

st.set_page_config(page_title="Personal Goal Optimization", layout="wide")

menu = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Create Goal",
    "View Goals",
    "Fitness",
    "Career",
    "Vision Board"
])

if menu == "Dashboard":
    dashboard.show()
elif menu == "Create Goal":
    create_goal.show()
elif menu == "View Goals":
    view_goals.show()
elif menu == "Fitness":
    fitness.show()
elif menu == "Career":
    career.show()
elif menu == "Vision Board":
    vision_board.show()