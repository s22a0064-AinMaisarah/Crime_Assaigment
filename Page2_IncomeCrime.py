import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np # Used for placeholder data

st.set_page_config(layout="wide")
st.title('📊 Crime Analysis: Socioeconomic Factors vs. Offense Count')
st.markdown("Exploring the relationship between **Income**, **Poverty**, and total **Offense Count** across different City Categories.")

st.header("🎯 Objective Statement")
st.markdown("""
The objective of this visualization is to explore the relationship between socioeconomic factors — **Income** and **Poverty Percentage** — 
and total **Offense Count** across different city categories. 
This helps identify patterns linking wealth, poverty, and crime incidence.
""")

url = "https://raw.githubusercontent.com/s22a0064-AinMaisarah/Crime_Assaigment/refs/heads/main/df_uber_cleaned.csv"
df = pd.read_csv(url)

st.header("📊 Summary of Analysis")

col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Average Income", value=f"${df_uber_cleaned['income'].mean():,.0f}")
col2.metric(label="Average Poverty %", value=f"{df_uber_cleaned['poverty'].mean():.2f}%")
col3.metric(label="Average Offense Count", value=f"{df_uber_cleaned['offense_count'].mean():.0f}")
col4.metric(label="Number of Cities", value=f"{df_uber_cleaned['city_cat'].nunique()}")

st.markdown("""
**Summary:** The scatter plots indicate that higher income areas generally have slightly lower offense counts, 
while regions with higher poverty tend to experience more offenses. City categories show distinct clusters, 
indicating that urban socioeconomic characteristics influence crime patterns. 
Trendlines (OLS) highlight these correlations, providing insights for policy planning and resource allocation.
""")

## 📈 Interactive Scatter Plots

# Create two columns to display the plots side-by-side
col1, col2 = st.columns(2)

# ---
# Plot 1: Income vs. Offense Count
# ---
with col1:
    st.header("Income vs. Offense Count")
    
    # Interactive Scatter Plot: Income vs. Offense Count with hover information and City Category color
    fig_income_offense = px.scatter(
        df_uber_cleaned,
        x='income',
        y='offense_count',
        color='city_cat',
        hover_data=['city_cat', 'income', 'offense_count', 'violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime', 'state', 'age'],
        title='Income vs. Offense Count by City Category',
        labels={'city_cat': 'City Category (0: Group II, 1: Group I)'},
        trendline='ols', # Add OLS trendline
        height=600
    )
    
    # Update legend title to be more informative
    fig_income_offense.update_layout(legend_title_text='City Category')

    # Use st.plotly_chart() to display the Plotly figure
    st.plotly_chart(fig_income_offense, use_container_width=True)

# ---
# Plot 2: Poverty % vs. Offense Count
# ---
with col2:
    st.header("Poverty % vs. Offense Count")

    # Interactive Scatter Plot: Poverty % vs. Offense Count with hover information and City Category color
    fig_poverty_offense = px.scatter(
        df_uber_cleaned,
        x='poverty',
        y='offense_count',
        color='city_cat',
        hover_data=['city_cat', 'poverty', 'offense_count', 'violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime', 'state', 'age'],
        title='Poverty % vs. Offense Count by City Category',
        labels={'city_cat': 'City Category (0: Group II, 1: Group I)'},
        trendline='ols', # Add OLS trendline
        height=600
    )
    
    # Update legend title to be more informative
    fig_poverty_offense.update_layout(legend_title_text='City Category')

    # Use st.plotly_chart() to display the Plotly figure
    st.plotly_chart(fig_poverty_offense, use_container_width=True) 
    st.header("📝 Interpretation / Discussion")
st.markdown("""
- **Income vs. Offense Count:** There is a weak negative correlation between income and offense count; higher-income areas tend to have slightly fewer offenses.
- **Poverty % vs. Offense Count:** Areas with higher poverty levels generally experience more offenses, consistent with socioeconomic crime theories.
- **City Category Differences:** City Category I (1) shows slightly higher offense counts at lower income levels, while Category II (0) clusters differently, indicating demographic and structural variations.
- These patterns suggest targeted interventions based on city socioeconomic profiles could improve crime prevention strategies.
""")

