import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💰 Economic Factors vs Crime")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/s22a0064-AinMaisarah/Crime_Assaigment/refs/heads/main/df_uber_cleaned.csv"
    return pd.read_csv(url, encoding="cp1252")

df = load_data()

st.subheader("Income vs Offense Count")
fig1 = px.scatter(
    df, x="income", y="offense_count", color="city_cat",
    trendline="ols",
    title="Income vs Offense Count"
)
st.plotly_chart(fig1)

st.subheader("Poverty vs Offense Count")
fig2 = px.scatter(
    df, x="poverty", y="offense_count", color="city_cat",
    trendline="ols",
    title="Poverty vs Offense Count"
)
st.plotly_chart(fig2)
