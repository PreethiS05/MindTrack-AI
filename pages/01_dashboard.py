import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🧠 MindTrack Dashboard")

col1,col2,col3 = st.columns(3)

col1.metric(
    "Mood Score",
    "78%",
    "+5%"
)

col2.metric(
    "Habit Streak",
    "12 days",
    "+2"
)

col3.metric(
    "Journal Entries",
    "34",
    "+4"
)

data = pd.DataFrame({
    "Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
    "Mood":[5,7,6,8,9,7,8]
})

fig = px.line(
    data,
    x="Day",
    y="Mood",
    markers=True,
    title="Weekly Mood Trend"
)

st.plotly_chart(fig,use_container_width=True)

st.subheader("AI Insight")

st.success(
"""
You felt happiest on Friday.
Stress increased midweek.
Sleep may affect mood.
"""
)
st.markdown("""

# 🧠 MindTrack AI

### Your personal AI wellness companion

Track mood • Build habits • Improve life

""")