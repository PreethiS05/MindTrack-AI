import streamlit as st
import pandas as pd
import sqlite3

conn=sqlite3.connect(
"mindtrack.db"
)

df=pd.read_sql(

"SELECT * FROM journal",
conn

)

st.title(
"📊 Analytics"
)

st.dataframe(df)

st.bar_chart(
df["mood"].value_counts()
)