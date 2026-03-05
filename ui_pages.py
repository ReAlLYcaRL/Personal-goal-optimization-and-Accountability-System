import streamlit as st
import pandas as pd
import plotly.express as px
import calendar
from datetime import date, timedelta
from core_logic import YEAR, TAGS, get_iso_weeks_in_month, iso_week_start

# --- 🏗️ 1. SETUP PAGE ---
def render_setup(u_id, get_cursor, conn):
    st.header("🏗️ Strategy Setup")
    with st.form("add_goal"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Goal Name")
        tag = c2.selectbox("Category", TAGS)
        freq = c1.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Quarterly", "Semester", "Yearly"])
        if st.form_submit_button("Add Goal"):
            with get_cursor() as cur:
                cur.execute(
                    "INSERT INTO goals_catalog (user_id, name, category, frequency) VALUES (%s,%s,%s,%s)",
                    (u_id, name, tag, freq)
                )
            conn.commit()
            st.rerun()
    
    st.subheader("Current Catalog")
    with get_cursor() as cur:
        cur.execute("SELECT * FROM goals_catalog WHERE user_id=%s", (u_id,))
        catalog = cur.fetchall()
    
    if not catalog:
        st.info("Your catalog is empty. Add your first goal above.")
    
    for g in catalog:
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{g['name']}** [{g['category']}] - {g['frequency']}")
        if col2.button("🗑️", key=f"del_{g['id']}"):
            with get_cursor() as cur:
                cur.execute("DELETE FROM goals_catalog WHERE id=%s", (g['id'],))
            conn.commit()
            st.rerun()


# --- 📅 2. EXECUTION PAGE ---
def render_execution(u_id, get_cursor, conn):
    st.header("📅 Weekly Execution")
    today = date.today()
    m_names = list(calendar.month_name)[1:]
    sel_month = st.selectbox("Month", m_names, index=today.month-1)
    m_idx = m_names.index(sel_month) + 1

    tab_dw, tab_lt = st.tabs(["Daily/Weekly Grid", "Strategic Matrix"])

    # --- Daily/Weekly Grid ---
    with tab_dw:
        iso_weeks = get_iso_weeks_in_month(YEAR, m_idx)
        with get_cursor() as cur:
            cur.execute("SELECT id, name FROM goals_catalog WHERE user_id=%s AND frequency='Daily'", (u_id,))
            d_goals = cur.fetchall()
            cur.execute("SELECT id, name FROM goals_catalog WHERE user_id=%s AND frequency='Weekly'", (u_id,))
            w_goals = cur.fetchall()

        for wk in iso_weeks:
            monday = iso_week_start(YEAR, wk)
            with st.expander(f"ISO Week {wk} (Starts {monday.strftime('%b %d')})", expanded=(wk == today.isocalendar()[1])):
                with st.form(f"wk_form_{wk}"):
                    st.markdown("**Daily Habits**")
                    header = st.columns([3] + [1]*7)
                    header[0].write("Goal")
                    for i in range(7):
                        header[i+1].write((monday + timedelta(days=i)).strftime("%a %d"))

                    d_buffer = {}
                    for dg in d_goals:
                        row = st.columns([3] + [1]*7)
                        row[0].write(f"**{dg['name']}**")
                        for i in range(7):
                            d_dt = monday + timedelta(days=i)
                            with get_cursor() as cur:
                                cur.execute(
                                    "SELECT 1 FROM daily_tracking WHERE goal_id=%s AND f_date=%s AND user_id=%s",
                                    (dg['id'], d_dt, u_id)
                                )
                                exists = cur.fetchone() is not None
                            d_buffer[(dg['id'], d_dt)] = row[i+1].checkbox(
                                " ", value=exists, key=f"cb_{dg['id']}_{d_dt}", label_visibility="collapsed"
                            )

                    st.divider()
                    st.markdown("**Weekly Milestones**")
                    w_buffer = {}
                    for wg in w_goals:
                        with get_cursor() as cur:
                            cur.execute(
                                "SELECT 1 FROM weekly_tracking WHERE goal_id=%s AND f_week=%s AND f_year=%s AND user_id=%s",
                                (wg['id'], wk, YEAR, u_id)
                            )
                            exists = cur.fetchone() is not None
                        w_buffer[wg['id']] = st.checkbox(wg['name'], value=exists, key=f"wb_{wg['id']}_{wk}")

                    if st.form_submit_button(f"Commit Week {wk}"):
                        with get_cursor() as cur:
                            for (gid, d_dt), val in d_buffer.items():
                                cur.execute(
                                    "DELETE FROM daily_tracking WHERE goal_id=%s AND f_date=%s AND user_id=%s",
                                    (gid, d_dt, u_id)
                                )
                                if val:
                                    cur.execute(
                                        "INSERT INTO daily_tracking (goal_id, user_id, f_date) VALUES (%s,%s,%s)",
                                        (gid, u_id, d_dt)
                                    )
                            for gid, val in w_buffer.items():
                                cur.execute(
                                    "DELETE FROM weekly_tracking WHERE goal_id=%s AND f_week=%s AND f_year=%s AND user_id=%s",
                                    (gid, wk, YEAR, u_id)
                                )
                                if val:
                                    cur.execute(
                                        "INSERT INTO weekly_tracking (goal_id, user_id, f_year, f_week) VALUES (%s,%s,%s,%s)",
                                        (gid, u_id, YEAR, wk)
                                    )
                        conn.commit()
                        st.rerun()


    # --- Strategic Matrix ---
    with tab_lt:
        st.subheader("🏁 Strategic Reflection Matrix")
        lt_f = st.selectbox("Period", ["Monthly", "Quarterly", "Semester", "Yearly"])
        if lt_f == "Monthly": p_list = [{"l": m[:3], "v": i+1} for i, m in enumerate(m_names)]
        elif lt_f == "Quarterly": p_list = [{"l": f"Q{i}", "v": i} for i in range(1, 5)]
        elif lt_f == "Semester": p_list = [{"l": f"S{i}", "v": i} for i in range(1, 3)]
        else: p_list = [{"l": "2026", "v": 2026}]

        with get_cursor() as cur:
            cur.execute("SELECT id, name FROM goals_catalog WHERE user_id=%s AND frequency=%s", (u_id, lt_f))
            lt_goals = cur.fetchall()

        if lt_goals:
            with st.form(f"lt_form_{lt_f}"):
                h = st.columns([2] + [1]*len(p_list))
                h[0].write("Goal")
                for i, p in enumerate(p_list): h[i+1].write(p['l'])
                lt_buffer = {}
                for g in lt_goals:
                    r = st.columns([2] + [1]*len(p_list))
                    r[0].write(g['name'])
                    for i, p in enumerate(p_list):
                        with get_cursor() as cur:
                            cur.execute(
                                "SELECT 1 FROM long_term_tracking WHERE goal_id=%s AND f_period_value=%s AND f_period_type=%s AND f_year=%s AND user_id=%s",
                                (g['id'], p['v'], lt_f, YEAR, u_id)
                            )
                            exists = cur.fetchone() is not None
                        lt_buffer[(g['id'], p['v'])] = r[i+1].checkbox(
                            " ", value=exists, key=f"lt_{g['id']}_{p['v']}", label_visibility="collapsed"
                        )

                if st.form_submit_button("Save Matrix"):
                    with get_cursor() as cur:
                        for (gid, pv), val in lt_buffer.items():
                            cur.execute(
                                "DELETE FROM long_term_tracking WHERE goal_id=%s AND f_period_value=%s AND f_period_type=%s AND f_year=%s AND user_id=%s",
                                (gid, pv, lt_f, YEAR, u_id)
                            )
                            if val:
                                cur.execute(
                                    "INSERT INTO long_term_tracking (goal_id, user_id, f_year, f_period_type, f_period_value) VALUES (%s,%s,%s,%s,%s)",
                                    (gid, u_id, YEAR, lt_f, pv)
                                )
                    conn.commit()
                    st.rerun()


# --- 📊 3. REPORTS PAGE ---
def render_reports(u_id, get_cursor):
    st.header("📊 Performance Mirror")
    today = date.today()
    curr_wk = today.isocalendar()[1]

    # SECTION 1: DAILY TIMELINE
    st.subheader("Daily Consistency Timeline")
    with get_cursor() as cur:
        cur.execute("SELECT f_date, count(*) as count FROM daily_tracking WHERE user_id=%s GROUP BY f_date", (u_id,))
        df_d = pd.DataFrame(cur.fetchall())

        cur.execute("SELECT count(*) as total FROM goals_catalog WHERE user_id=%s AND frequency='Daily'", (u_id,))
        total_row = cur.fetchone()
        daily_total = total_row['total'] if total_row else 1

    all_dates = pd.date_range(start=date(YEAR, 1, 1), end=today)
    if not df_d.empty:
        plot_df = pd.DataFrame({'f_date': all_dates.date}).merge(df_d, on='f_date', how='left').fillna(0)
    else:
        plot_df = pd.DataFrame({'f_date': all_dates.date, 'count': 0})
    plot_df['rate'] = (plot_df['count'] / daily_total) * 100

    fig_line = px.line(plot_df, x='f_date', y='rate', title="Achievement Rate %")
    fig_line.add_hline(y=100, line_dash="dash", line_color="green", annotation_text="Ideal Standard")
    st.plotly_chart(fig_line, use_container_width=True)