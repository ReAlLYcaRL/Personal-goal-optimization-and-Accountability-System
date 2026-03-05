import streamlit as st
from db_utils import get_db_connection, get_cursor
from core_logic import YEAR, TAGS
import ui_pages


# PAGE CONFIG

st.set_page_config(
    page_title="Vision 2026",
    layout="wide"
)

# SHARED SESSION STATE

if "user" not in st.session_state:
    st.session_state.user = None


# DATABASE CONNECTION

conn = get_db_connection()  # Cached connection


# ENSURE ALL TABLES EXIST

def create_tables():
    with get_cursor() as cur:
        # USERS
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # GOALS CATALOG
        cur.execute("""
        CREATE TABLE IF NOT EXISTS goals_catalog (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            category TEXT,
            frequency TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # DAILY TRACKING
        cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_tracking (
            id SERIAL PRIMARY KEY,
            goal_id INTEGER REFERENCES goals_catalog(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            f_date DATE NOT NULL
        );
        """)

        # WEEKLY TRACKING
        cur.execute("""
        CREATE TABLE IF NOT EXISTS weekly_tracking (
            id SERIAL PRIMARY KEY,
            goal_id INTEGER REFERENCES goals_catalog(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            f_year INTEGER NOT NULL,
            f_week INTEGER NOT NULL
        );
        """)

        # LONG TERM TRACKING
        cur.execute("""
        CREATE TABLE IF NOT EXISTS long_term_tracking (
            id SERIAL PRIMARY KEY,
            goal_id INTEGER REFERENCES goals_catalog(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            f_year INTEGER NOT NULL,
            f_period_type TEXT NOT NULL,
            f_period_value INTEGER NOT NULL
        );
        """)
    conn.commit()

# Create tables on app start
create_tables()

# LANDING PAGE (LOGIN / REGISTER)

if st.session_state.user is None:

    col_img, col_text = st.columns([1.2, 1], gap="large")

    # LEFT IMAGE
    with col_img:
        st.image(
            "https://images.unsplash.com/photo-1493612276216-ee3925520721?q=80&w=2000&auto=format&fit=crop",
            caption="Strategy is the art of closing the gap between vision and reality."
        )

    # RIGHT CONTENT
    with col_text:
        st.title("~Personal goal optimization and Accountability System")
        st.subheader("A simple system to stay consistent with your goals")

        st.markdown("""
        helps you focus on **what really matters**:  
        showing up consistently — day after day, week after week.

        Instead of tracking tasks, you track **habits, commitments, and long-term intentions**.

        **What you can do:**
        - Track your daily and weekly habits in one clear place
        - Keep sight of your monthly, quarterly, and yearly goals
        - See where you’re consistent — and where you need to adjust
        - Reflect and improve without guilt or pressure

        This is not a productivity hack.  
        It’s a **clarity and accountability system**.
        """)

        st.divider()

        # ---------------- LOGIN / REGISTER TABS ----------------
        auth_tab1, auth_tab2 = st.tabs(
            ["🔒 Secure Login", "✨ Join Vision 2026"]
        )

        # LOGIN
        with auth_tab1:
            email = st.text_input("Email", key="login_email")
            pw = st.text_input("Password", type="password", key="login_pw")

            if st.button(
                "Enter Workspace",
                use_container_width=True,
                type="primary"
            ):
                with get_cursor() as cur:
                    cur.execute(
                        "SELECT id, email FROM users WHERE email=%s AND password_hash=%s",
                        (email, pw)
                    )
                    u = cur.fetchone()

                if u:
                    st.session_state.user = {
                        "id": u["id"],
                        "email": u["email"]
                    }
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        # REGISTER
        with auth_tab2:
            reg_email = st.text_input("New Email", key="reg_email")
            reg_pw = st.text_input(
                "New Password",
                type="password",
                key="reg_pw"
            )

            if st.button(
                "Create My System",
                use_container_width=True
            ):
                try:
                    with get_cursor() as cur:
                        cur.execute(
                            "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                            (reg_email, reg_pw)
                        )
                    conn.commit()
                    st.success("Account created! Log in above.")
                except Exception:
                    conn.rollback()
                    st.error("Email already exists.")

    st.markdown("---")
    st.caption(
        "“We are what we repeatedly do. Excellence, then, is not an act, but a habit.” — Aristotle"
    )


# MAIN APPLICATION UI

else:

    u_id = st.session_state.user["id"]

    # SIDEBAR
    with st.sidebar:
        st.write(f"Logged in: **{st.session_state.user['email']}**")

        nav = st.radio(
            "Menu",
            ["🏗️ Setup", "📅 Execution", "📊 Reports"]
        )

        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

    # PAGE ROUTING
    if nav == "🏗️ Setup":
        ui_pages.render_setup(u_id, get_cursor, conn)

    elif nav == "📅 Execution":
        ui_pages.render_execution(u_id, get_cursor, conn)

    elif nav == "📊 Reports":
        ui_pages.render_reports(u_id, get_cursor)