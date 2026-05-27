import streamlit as st

st.title(
"Welcome back Preethi 🌸"
)

c1,c2,c3,c4=st.columns(4)

c1.metric(
"😊 Mood",
"82%",
"+4%"
)

c2.metric(
"🔥 Streak",
"12",
"+1"
)

c3.metric(
"📝 Journals",
"44"
)

c4.metric(
"🎯 Habits",
"76%"
)