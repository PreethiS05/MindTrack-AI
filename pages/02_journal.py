import streamlit as st
from textblob import TextBlob

st.title("📝 AI Journal")

mood = st.select_slider(

    "How do you feel today?",

    options=[
        "😭",
        "😔",
        "😐",
        "😊",
        "🤩"
    ]

)

entry = st.text_area(

    "Write your thoughts..."

)


if st.button(

    "Analyze Mood"

):

    sentiment = TextBlob(

        entry

    ).sentiment.polarity


    if sentiment > 0:

        detected = "😊 Positive"


    elif sentiment < 0:

        detected = "😔 Negative"


    else:

        detected = "😐 Neutral"



    st.success(

        f"Detected mood: {detected}"

    )


    st.write(

        "Selected mood:",

        mood

    )