import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np # Needed for creating a dummy dataframe if you don't have the real one

## 🎨 Streamlit App Title
st.title('Interactive Radar Chart: Average Crime Scores by Age Group and Crime Type')

# ---
### ⚙️ Data Preparation (Example/Placeholder)

# **NOTE:** Replace this section with your actual data loading and cleaning, 
# for instance: 'df_uber_cleaned = pd.read_csv("your_data.csv")'

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
