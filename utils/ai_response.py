from openai import OpenAI
import streamlit as st


client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],

    base_url="https://openrouter.ai/api/v1"
)


def ask_ai(prompt):

    try:

        completion = client.chat.completions.create(

            model="deepseek/deepseek-chat",

            messages=[

                {
                    "role":"system",

                    "content":"""
You are MindTrack AI.

Help users with:

- stress
- productivity
- habits
- journaling
- motivation

Avoid medical advice.
Be supportive.
"""
                },

                {
                    "role":"user",

                    "content":prompt
                }

            ]

        )

        return completion.choices[0].message.content


    except Exception as e:

        return f"Error: {str(e)}"