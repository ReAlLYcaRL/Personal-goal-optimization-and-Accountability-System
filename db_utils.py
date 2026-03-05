import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

# -----------------------------------
# Get or cache DB connection
# -----------------------------------
@st.cache_resource
def get_db_connection():
    """
    Creates and returns a cached PostgreSQL connection.
    Uses Streamlit secrets (DATABASE_URL).
    """
    return psycopg2.connect(st.secrets["DATABASE_URL"])

# -----------------------------------
# Get a live cursor
# -----------------------------------
def get_cursor():
    """
    Returns a RealDictCursor from an active connection.
    Reconnects automatically if the connection is closed.
    """
    conn = get_db_connection()

    # Reconnect if closed
    if conn.closed != 0:
        conn = get_db_connection()

    return conn.cursor(cursor_factory=RealDictCursor)