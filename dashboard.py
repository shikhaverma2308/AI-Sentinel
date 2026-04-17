import streamlit as st
import pandas as pd
import os
import glob
import sqlite3
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="AI Sentinel Dashboard", layout="wide")
st_autorefresh(interval=2000, key="refresh")
st.markdown("---")

st.title("🚨 AI Sentinel: Real-Time Crowd Monitoring System")

@st.cache_data(ttl=2)
def load_data():
    with sqlite3.connect("crowd.db") as conn:
        df = pd.read_sql_query("SELECT * FROM crowd_log", conn)
    return df

df = load_data()

# ===== METRICS ROW =====
if not df.empty:
    latest = df["person_count"].iloc[-1]
    avg = df["person_count"].tail(10).mean()
    peak = df["person_count"].max()

    col1, col2, col3 = st.columns(3)

    col1.metric("👤 Current People", latest)
    col2.metric("📊 Avg Crowd", round(avg, 2))
    col3.metric("🚀 Peak Crowd", peak)

    # ===== STATUS =====
    if latest >= 5:
        st.error("🔴 HIGH RISK")
    elif latest >= 3:
        st.warning("🟠 WARNING")
    else:
        st.success("🟢 NORMAL")

# ===== MAIN LAYOUT =====
col1, col2 = st.columns(2)

# LEFT SIDE
with col1:
    st.subheader("📈 Real-Time Crowd Trend")
    st.line_chart(df["person_count"].rolling(3).mean())

    st.subheader("📊 Recent Data")
    st.dataframe(df.tail(10), use_container_width=True)

# RIGHT SIDE
with col2:
    st.subheader("🚨 Alert History")
    alerts = df[df["person_count"] >= 2]
    st.dataframe(alerts.tail(5), use_container_width=True)

    st.subheader("📸 Latest Evidence")
    images = glob.glob("evidence/*.jpg")
    if images:
        latest_img = max(images, key=os.path.getctime)
        st.image(latest_img, width=400)
    else:
        st.info("No images yet")