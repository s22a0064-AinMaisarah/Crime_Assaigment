import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np # Used for placeholder data

st.set_page_config(layout="wide")
st.title('📊 Crime Analysis: Socioeconomic Factors vs. Offense Count')
st.markdown("Exploring the relationship between **Income**, **Poverty**, and total **Offense Count** across different City Categories.")

# ---
## ⚙️ Data Preparation (Example/Placeholder)

# **NOTE:** Replace this placeholder with your actual data loading:
# e.g., 'df_uber_cleaned = pd.read_csv("your_data.csv")'

try:
    # Check if df_uber_cleaned is defined
    df_uber_cleaned
except NameError:
    st.info("Creating a placeholder DataFrame for demonstration. **Replace this with your actual data loading.**")
    N = 200
    np.random.seed(42)
    data = {
        'income': np.random.normal(70000, 25000, N),
        'poverty': np.random.normal(15, 5, N),
        # Offense count slightly correlated with poverty and inversely with income
        'offense_count': np.random.randint(50, 200, N) + (30 - np.random.normal(10, 5, N) / 2) * 5, 
        'city_cat': np.random.choice([0, 1], N, p=[0.6, 0.4]).astype(str), # Convert to string for color
        'violent_crime': np.random.rand(N) * 10,
        'property_crime': np.random.rand(N) * 15,
        'whitecollar_crime': np.random.rand(N) * 5,
        'social_crime': np.random.rand(N) * 8,
        'state': np.random.choice(['NY', 'CA', 'TX', 'FL'], N),
        'age': np.random.choice(['18-25', '26-35', '36-45', '46+'], N),
    }
    df_uber_cleaned = pd.DataFrame(data)

# Ensure 'city_cat' is string for discrete coloring
df_uber_cleaned['city_cat'] = df_uber_cleaned['city_cat'].astype(str)

# ---
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
