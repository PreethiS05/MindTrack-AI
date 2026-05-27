import streamlit as st

st.title("🎯 Habit Tracker")

water=st.checkbox("Drink 2L water")
exercise=st.checkbox("Exercise")
study=st.checkbox("Study")
sleep=st.checkbox("Sleep 8h")

score=sum([water,exercise,study,sleep])

st.progress(score/4)

st.write(
f"Today's Score: {score}/4"
)