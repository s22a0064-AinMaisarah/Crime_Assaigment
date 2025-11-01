import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Streamlit App ---
st.set_page_config(page_title="Crime Radar Chart by Age", layout="wide")
st.title("Average Crime Scores by Age Group and Crime Type")

# --- Load Dataset ---
CSV_URL = 'https://raw.githubusercontent.com/s22a0064-AinMaisarah/UrbanCrime/refs/heads/main/df_uber_cleaned.csv'
df = pd.read_csv(CSV_URL, encoding='cp1252')

# --- Define crime score columns ---
crime_cols = ['violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime']

# --- Calculate average crime scores per age group ---
age_group_crime_means = df.groupby('age', observed=True)[crime_cols].mean().reset_index()

# --- Radar chart ---
categories = crime_cols
fig = go.Figure()

for index, row in age_group_crime_means.iterrows():
    fig.add_trace(go.Scatterpolar(
        r=row[crime_cols].tolist(),
        theta=categories,
        fill='toself',
        name=f'Age Group {row["age"]}'
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, age_group_crime_means[crime_cols].values.max()]
        )
    ),
    showlegend=True,
    title='Interactive Radar Chart: Average Crime Scores by Age Group and Crime Type',
    template='plotly_white'
)

# --- Display in Streamlit ---
st.plotly_chart(fig, use_container_width=True)
