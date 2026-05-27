import streamlit as st
st.image(
"assets/ai_avatar.png",
width=120
)

st.title(
"MindTrack Companion"
)

st.title(
"🤖 AI Companion"
)

if "messages" not in st.session_state:

    st.session_state.messages=[]


for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.markdown(
            msg["content"]
        )