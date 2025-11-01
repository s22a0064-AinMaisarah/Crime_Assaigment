import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(page_title="Income & Poverty vs. Crime Analysis", layout="wide")
st.title("Income, Poverty, and Crime Analysis by City Category")

# =====================================================
# OBJECTIVE STATEMENT
# =====================================================
st.header("🎯 Objective Statement")
st.markdown("""
The objective of this visualization is to explore how **income levels** and **poverty rates** influence 
**crime occurrences** across different **city categories**.  
By examining these socio-economic indicators, we can identify correlations that help explain how 
economic disparities contribute to varying crime rates in urban settings.
""")

# =====================================================
# LOAD DATASET
# =====================================================
CSV_URL = 'https://raw.githubusercontent.com/s22a0064-AinMaisarah/UrbanCrime/refs/heads/main/df_uber_cleaned.csv'
df = pd.read_csv(CSV_URL, encoding='cp1252')

# =====================================================
# SCATTER PLOT: INCOME VS OFFENSE COUNT
# =====================================================
st.subheader("💰 Income vs. Offense Count by City Category")
fig_income_offense = px.scatter(
    df,
    x='income',
    y='offense_count',
    color='city_cat',
    hover_data=['city_cat', 'income', 'offense_count', 'violent_crime', 'property_crime',
                'whitecollar_crime', 'social_crime', 'state', 'age'],
    title='Income vs. Offense Count by City Category',
    labels={'city_cat': 'City Category (0: Group II, 1: Group I)'},
    trendline='ols',
    template='plotly_white'
)
st.plotly_chart(fig_income_offense, use_container_width=True)

# =====================================================
# SCATTER PLOT: POVERTY VS OFFENSE COUNT
# =====================================================
st.subheader("📉 Poverty % vs. Offense Count by City Category")
fig_poverty_offense = px.scatter(
    df,
    x='poverty',
    y='offense_count',
    color='city_cat',
    hover_data=['city_cat', 'poverty', 'offense_count', 'violent_crime', 'property_crime',
                'whitecollar_crime', 'social_crime', 'state', 'age'],
    title='Poverty % vs. Offense Count by City Category',
    labels={'city_cat': 'City Category (0: Group II, 1: Group I)'},
    trendline='ols',
    template='plotly_white'
)
st.plotly_chart(fig_poverty_offense, use_container_width=True)

# =====================================================
# SUMMARY METRICS
# =====================================================
st.subheader("📊 Summary Metrics")

# Calculate some meaningful insights
avg_income = df['income'].mean()
avg_poverty = df['poverty'].mean()
avg_offense = df['offense_count'].mean()
max_city = df.groupby('city_cat')['offense_count'].mean().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Average Income (USD)", value=f"${avg_income:,.0f}", help="Average income across all cities")
col2.metric(label="Average Poverty Rate (%)", value=f"{avg_poverty:.1f}%", help="Average poverty percentage across cities")
col3.metric(label="Average Offense Count", value=f"{avg_offense:.0f}", help="Mean number of recorded offenses")
col4.metric(label="Highest Crime Category", value=f"Group {int(max_city)}", help="City category with the highest average offenses")

# =====================================================
# SUMMARY OF FINDINGS
# =====================================================
st.header("🧭 Summary of Findings")
st.markdown("""
The analysis indicates a **clear relationship between socio-economic status and crime levels**.  
Cities with **lower income and higher poverty rates** tend to have **higher offense counts**, suggesting that 
economic hardship may be a driving factor for increased criminal activity.  
Group I cities (typically larger urban areas) generally exhibit **higher income but still notable crime rates**, 
implying that urban density and opportunity also play a role.  
The regression trendlines confirm a **negative correlation between income and offenses** 
and a **positive correlation between poverty and offenses**.  
These findings support the notion that economic well-being is a key determinant of urban safety.
""")

# =====================================================
# INTERPRETATION & DISCUSSION
# =====================================================
st.header("💡 Interpretation & Discussion")
st.markdown("""
The scatter plots reveal that as **income increases**, the **number of offenses decreases**, 
demonstrating an inverse relationship between wealth and crime prevalence.  
Conversely, higher **poverty rates** are associated with increased criminal activity, 
likely due to economic strain and limited access to resources.  
Group II (smaller or less developed cities) tend to show higher crime concentration at lower income levels, 
while Group I cities show diverse patterns due to urban complexity.  
Overall, the results highlight the **importance of targeted economic and social programs** to reduce poverty-driven crime.
""")
