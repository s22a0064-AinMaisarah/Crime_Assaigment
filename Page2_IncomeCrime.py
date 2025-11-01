import streamlit as st
import pandas as pd
import plotly.express as px

# --- Streamlit App ---
st.set_page_config(page_title="Income & Poverty vs. Crime Analysis", layout="wide")
st.title("Income, Poverty, and Crime Analysis by City Category")

# --- Load Dataset ---
CSV_URL = 'https://raw.githubusercontent.com/s22a0064-AinMaisarah/UrbanCrime/refs/heads/main/df_uber_cleaned.csv'
df = pd.read_csv(CSV_URL, encoding='cp1252')

# --- Scatter Plot: Income vs. Offense Count ---
st.subheader("Income vs. Offense Count by City Category")
fig_income_offense = px.scatter(
    df,
    x='income',
    y='offense_count',
    color='city_cat',
    hover_data=['city_cat', 'income', 'offense_count', 'violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime', 'state', 'age'],
    title='Income vs. Offense Count by City Category',
    labels={'city_cat': 'City Category (0: Group II, 1: Group I)'},
    trendline='ols',
    template='plotly_white'
)
st.plotly_chart(fig_income_offense, use_container_width=True)

# --- Scatter Plot: Poverty % vs. Offense Count ---
st.subheader("Poverty % vs. Offense Count by City Category")
fig_poverty_offense = px.scatter(
    df,
    x='poverty',
    y='offense_count',
    color='city_cat',
    hover_data=['city_cat', 'poverty', 'offense_count', 'violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime', 'state', 'age'],
    title='Poverty % vs. Offense Count by City Category',
    labels={'city_cat': 'City Category (0: Group II, 1: Group I)'},
    trendline='ols',
    template='plotly_white'
)
st.plotly_chart(fig_poverty_offense, use_container_width=True)
