import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
CSV_URL = 'https://raw.githubusercontent.com/s22a0064-AinMaisarah/Crime_Assaigment/refs/heads/main/df_uber_cleaned.csv'
ENCODING_TYPE = 'cp1252'

# --- APP TITLE ---
st.title("🚨 Crime Analytics Dashboard — Objective 1")
st.markdown("""
### 🧠 Objective 1  
**Analyze socio-economic indicators (income & poverty) and their relationship with crime patterns across city categories**
""")
st.markdown("---")

# --- LOAD DATA ---
@st.cache_data
def load_data(url, encoding):
    try:
        df = pd.read_csv(url, encoding=encoding)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df_uber_cleaned = load_data(CSV_URL, ENCODING_TYPE)

if not df_uber_cleaned.empty:

    # ✅ Scatter Plot 1: Income vs City Category
    st.subheader("1️⃣ Income vs City Category")
    fig_income_citycat = px.scatter(
        df_uber_cleaned,
        x='income',
        y='city_cat',
        color='city_cat',
        hover_data=['city_cat', 'income', 'offense_count', 'violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime'],
        title='Income vs. City Category'
    )
    st.plotly_chart(fig_income_citycat, use_container_width=True)
    st.write("""
    **Insight:**  
    Higher-income cities show different crime patterns compared to lower-income areas, 
    indicating socio-economic influence on crime levels.
    """)

    # ✅ Scatter Plot 2: Poverty vs City Category
    st.subheader("2️⃣ Poverty vs City Category")
    fig_poverty_citycat = px.scatter(
        df_uber_cleaned,
        x='poverty',
        y='city_cat',
        color='city_cat',
        hover_data=['city_cat', 'poverty', 'offense_count', 'violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime'],
        title='Poverty % vs. City Category'
    )
    st.plotly_chart(fig_poverty_citycat, use_container_width=True)
    st.write("""
    **Insight:**  
    Cities with higher poverty percentages tend to fall into categories with varying crime dynamics.  
    This suggests poverty may influence crime distribution.
    """)

    # ✅ Scatter Plot 3: Income vs Offense Count + Regression
    st.subheader("3️⃣ Income vs Offense Count (Trendline)")
    fig_income_offense = px.scatter(
        df_uber_cleaned,
        x='income',
        y='offense_count',
        color='city_cat',
        hover_data=['city_cat', 'income', 'offense_count', 'violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime', 'state', 'age'],
        title='Income vs Offense Count by City Category',
        trendline='ols'
    )
    st.plotly_chart(fig_income_offense, use_container_width=True)
    st.write("""
    **Insight:**  
    Trendline helps show correlation.  
    Crime may decrease slightly as income increases — supporting economic-crime theory.
    """)

    # ✅ Scatter Plot 4: Poverty vs Offense Count + Regression
    st.subheader("4️⃣ Poverty vs Offense Count (Trendline)")
    fig_poverty_offense = px.scatter(
        df_uber_cleaned,
        x='poverty',
        y='offense_count',
        color='city_cat',
        hover_data=['city_cat', 'poverty', 'offense_count', 'violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime', 'state', 'age'],
        title='Poverty % vs Offense Count by City Category',
        trendline='ols'
    )
    st.plotly_chart(fig_poverty_offense, use_container_width=True)
    st.write("""
    **Insight:**  
    Higher poverty may correlate with higher reported crimes — indicating socio-economic vulnerability.
    """)

else:
    st.error("❌ Failed to load dataset from GitHub.")
