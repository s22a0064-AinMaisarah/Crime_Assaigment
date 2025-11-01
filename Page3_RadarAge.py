import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🧭 Crime Radar by Age Group")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/s22a0064-AinMaisarah/Crime_Assaigment/refs/heads/main/df_uber_cleaned.csv"
    return pd.read_csv(url, encoding="cp1252")

df = load_data()

crime_cols = ['violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime']
age_groups = df.groupby("age")[crime_cols].mean().reset_index()

fig = go.Figure()

for _, row in age_groups.iterrows():
    fig.add_trace(go.Scatterpolar(
        r=row[crime_cols].tolist(),
        theta=crime_cols,
        fill="toself",
        name=f"Age {row['age']}"
    ))

fig.update_layout(title="Crime Patterns by Age Group")
st.plotly_chart(fig)
