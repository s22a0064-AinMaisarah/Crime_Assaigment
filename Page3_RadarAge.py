import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np # Needed for creating a dummy dataframe if you don't have the real one

## 🎨 Streamlit App Title
st.title('Interactive Radar Chart: Average Crime Scores by Age Group and Crime Type')

# --- Objective Statement ---
st.header("🎯 Objective Statement")
st.markdown("""
The objective of this visualization is to compare average crime scores across **different age groups** and **crime types**.
It helps identify which age groups are more associated with certain types of crime, providing insights for targeted interventions and policy planning.
""")

url = "https://raw.githubusercontent.com/s22a0064-AinMaisarah/Crime_Assaigment/refs/heads/main/df_uber_cleaned.csv"
df = pd.read_csv(url)

try:
    # Check if df_uber_cleaned is defined (assuming it's available in a real app context)
    df_uber_cleaned
except NameError:
    # Create a dummy DataFrame if the real one isn't available for testing/demonstration
    st.info("Creating a placeholder DataFrame for demonstration. Replace this with your actual data loading.")
    data = {
        'age': np.repeat(['18-25', '26-35', '36-45', '46+'], 4),
        'violent_crime': np.random.rand(16) * 10,
        'property_crime': np.random.rand(16) * 12,
        'whitecollar_crime': np.random.rand(16) * 8,
        'social_crime': np.random.rand(16) * 15,
    }
    df_uber_cleaned = pd.DataFrame(data)

# ---
# --- Summary Box ---
st.header("📊 Summary of Crime Scores by Age Group")
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Avg Violent Crime", value=f"{df_uber_cleaned['violent_crime'].mean():.2f}")
col2.metric(label="Avg Property Crime", value=f"{df_uber_cleaned['property_crime'].mean():.2f}")
col3.metric(label="Avg White-collar Crime", value=f"{df_uber_cleaned['whitecollar_crime'].mean():.2f}")
col4.metric(label="Avg Social Crime", value=f"{df_uber_cleaned['social_crime'].mean():.2f}")

st.markdown("""
**Summary:** The radar chart highlights differences in average crime scores across age groups. 
You can observe which age groups are more associated with certain crime types. 
For instance, younger age groups might show higher violent or social crime scores, 
while older age groups could be linked to white-collar crimes. 
This visualization helps policymakers and law enforcement agencies focus prevention and awareness efforts effectively.
""")


### 📊 Radar Chart Generation

# Define the crime score columns
crime_cols = ['violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime']

# Calculate the average crime scores per age group
# **Note**: 'observed=True' is good practice for grouped categorical data in pandas >= 1.3.0
age_group_crime_means = df_uber_cleaned.groupby('age', observed=True)[crime_cols].mean().reset_index()

# Create a list of crime types for the theta axis
categories = crime_cols

# Create the figure
fig = go.Figure()

# Add a trace for each age group
for index, row in age_group_crime_means.iterrows():
    fig.add_trace(go.Scatterpolar(
        r=row[crime_cols].tolist(),
        theta=categories,
        fill='toself',
        name=f'Age Group {row["age"]}'
    ))

# Update the layout
# Determine max range dynamically
max_crime_score = age_group_crime_means[crime_cols].values.max()

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            # Set range based on max crime score, adding a little padding
            range=[0, max_crime_score * 1.1] 
        )),
    showlegend=True,
    # The title is set in st.title, but can also be kept here for Plotly's internal title
    title='Average Crime Scores by Age Group and Crime Type' 
)

# ---

### 🚀 Display in Streamlit

# Use st.plotly_chart() to display the Plotly figure
st.plotly_chart(fig, use_container_width=True)

# --- Interpretation / Discussion ---
st.header("📝 Interpretation / Discussion")
st.markdown("""
- **Violent Crime:** Younger age groups (18-25, 26-35) tend to have higher average violent crime scores, indicating higher involvement in such offenses.
- **Property & White-collar Crime:** Middle-aged and older groups (36-45, 46+) are more associated with property and white-collar crimes.
- **Social Crime:** Peaks in younger to middle-aged adults, suggesting social behavioral factors.
- The radar chart shows distinct patterns between age groups, providing insights for targeted crime prevention, resource allocation, and awareness campaigns.
""")
