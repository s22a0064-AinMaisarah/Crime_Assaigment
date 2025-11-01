import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(page_title="Crime Radar Chart by Age", layout="wide")
st.title("Average Crime Scores by Age Group and Crime Type")

# =====================================================
# OBJECTIVE STATEMENT
# =====================================================
st.header("🎯 Objective Statement")
st.markdown("""
The objective of this visualization is to analyze **how crime patterns differ across age groups**, 
highlighting which types of crimes are more prevalent among certain age ranges.  
By visualizing crime scores in a **radar chart**, we can easily compare crime tendencies 
among different demographic groups and identify age-based behavioral trends.
""")

# =====================================================
# LOAD DATASET
# =====================================================
CSV_URL = 'https://raw.githubusercontent.com/s22a0064-AinMaisarah/UrbanCrime/refs/heads/main/df_uber_cleaned.csv'
df = pd.read_csv(CSV_URL, encoding='cp1252')

# =====================================================
# DATA PROCESSING
# =====================================================
crime_cols = ['violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime']
age_group_crime_means = df.groupby('age', observed=True)[crime_cols].mean().reset_index()

# =====================================================
# RADAR CHART VISUALIZATION
# =====================================================
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

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# SUMMARY METRICS
# =====================================================
st.subheader("📊 Summary Metrics")

# Compute some key insights
avg_violent = df['violent_crime'].mean()
avg_property = df['property_crime'].mean()
avg_whitecollar = df['whitecollar_crime'].mean()
avg_social = df['social_crime'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Average Violent Crime", value=f"{avg_violent:.2f}", help="Mean violent crime score")
col2.metric(label="Average Property Crime", value=f"{avg_property:.2f}", help="Mean property crime score")
col3.metric(label="Average White-Collar Crime", value=f"{avg_whitecollar:.2f}", help="Mean white-collar crime score")
col4.metric(label="Average Social Crime", value=f"{avg_social:.2f}", help="Mean social crime score")

# =====================================================
# SUMMARY OF FINDINGS
# =====================================================
st.header("🧭 Summary of Findings")
st.markdown("""
The radar visualization shows that **crime tendencies vary distinctly by age group**.  
Younger age groups generally exhibit higher scores in **social and property crimes**, which are 
often linked to impulsive behaviors and socio-economic influences.  
In contrast, older age groups show **lower involvement in violent crimes** but a slight rise 
in **white-collar offenses**, possibly reflecting occupational access and financial opportunities.  
Overall, the visualization emphasizes how **age can influence the type of crime**, 
suggesting that prevention strategies should be age-targeted.
""")

# =====================================================
# INTERPRETATION & DISCUSSION
# =====================================================
st.header("💡 Interpretation & Discussion")
st.markdown("""
The data suggests that **age plays a critical role in shaping crime profiles**.  
Younger populations are more likely to engage in **social misconduct and property-related offenses**, 
which may stem from peer influence or financial instability.  
Meanwhile, middle-aged and older individuals show a higher share of **white-collar crimes**, 
reflecting different motivations such as greed or misuse of professional authority.  
These patterns underline the need for **age-specific intervention policies** — for example, 
youth community engagement for crime prevention and financial ethics education for professionals.  
Understanding these distinctions helps policymakers design more effective, demographic-sensitive crime reduction strategies.
""")
