import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")
st.title('🗺️ K-Means Clustering for Crime Pattern Analysis')
st.markdown("""
This app performs K-Means clustering on crime scores after scaling and uses PCA for 2D visualization.
""")

st.header("🎯 Objective Statement")
st.markdown("""
The objective of this visualization is to identify patterns in urban crime by grouping similar crime profiles 
using K-Means clustering and visualizing these patterns with PCA for a 2D interactive view. 
This helps understand how different crime types co-occur across regions and demographics.
""")

# --- Load Data ---
url = "https://raw.githubusercontent.com/s22a0064-AinMaisarah/Crime_Assaigment/refs/heads/main/df_uber_cleaned.csv"
df = pd.read_csv(url)

# --- Features ---
features = ['violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime']
X = df[features]

# --- Scale Features ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- Elbow Method ---
st.header('1. Optimal Cluster Determination (Elbow Method)')
col1, col2 = st.columns([1, 1])

with col1:
    wcss = []
    for k in range(2, 10):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        wcss.append(kmeans.inertia_)
    
    fig_elbow, ax = plt.subplots(figsize=(7, 5))
    ax.plot(range(2, 10), wcss, marker='o')
    ax.set_title('Elbow Method for Optimal k')
    ax.set_xlabel('Number of Clusters (k)')
    ax.set_ylabel('WCSS (Inertia)')
    st.pyplot(fig_elbow)

with col2:
    st.markdown("""
    The **Elbow Method** helps choose the best number of clusters ($k$). 
    The 'elbow' point is where the rate of decrease in the **WCSS** (Within-Cluster Sum-of-Squares) 
    dramatically slows down.
    """)

# --- Select K ---
k_input = st.slider('Select the Optimal Number of Clusters (k)', 2, 8, 3, help="Adjust this based on the elbow plot.")

# --- K-Means Clustering ---
st.header('2. K-Means Clustering Results')
kmeans = KMeans(n_clusters=k_input, random_state=42, n_init=10)
df['crime_cluster'] = kmeans.fit_predict(X_scaled).astype(str)

# --- PCA for Visualization ---
pca = PCA(n_components=2)
pca_data = pca.fit_transform(X_scaled)
df['PC1'] = pca_data[:, 0]
df['PC2'] = pca_data[:, 1]

fig_clusters = px.scatter(
    df,
    x='PC1',
    y='PC2',
    color='crime_cluster',
    hover_data=['crime_cluster'] + features + ['city_cat', 'state', 'age', 'income', 'poverty'],
    title='Crime Pattern Clusters (PCA Visualization)',
    labels={'crime_cluster': 'Crime Cluster'},
    height=550
)
st.plotly_chart(fig_clusters, use_container_width=True)

# --- Summary Metrics ---
st.header("📊 Summary of Cluster Analysis")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Number of Clusters", value=f"{k_input}")
col2.metric(label="Average Violent Crime", value=f"{df['violent_crime'].mean():.2f}")
col3.metric(label="Average Property Crime", value=f"{df['property_crime'].mean():.2f}")
col4.metric(label="Average White-collar Crime", value=f"{df['whitecollar_crime'].mean():.2f}")

st.markdown("""
**Summary:** This analysis identifies distinct clusters of crime patterns. Cluster profiling shows 
that some clusters are dominated by violent crimes while others have higher white-collar or property crimes. 
The PCA visualization demonstrates that clusters are fairly well-separated in 2D space, 
indicating meaningful groupings that can support targeted policy interventions and resource allocation.
""")

# --- Cluster Profile Bar Chart ---
st.header('3. Cluster Profile Bar Chart')
cluster_profile = df.groupby('crime_cluster')[features].mean().reset_index()
cluster_profile_melted = cluster_profile.melt(id_vars='crime_cluster', var_name='Crime Type', value_name='Average Crime Score')

fig_cluster_profile = px.bar(
    cluster_profile_melted,
    x='Crime Type',
    y='Average Crime Score',
    color='crime_cluster',
    barmode='group',
    hover_data=['crime_cluster', 'Crime Type', 'Average Crime Score'],
    title='Interactive Bar Chart: Average Crime Scores per Cluster',
    labels={'crime_cluster': 'Crime Cluster'},
    height=550
)
st.plotly_chart(fig_cluster_profile, use_container_width=True)

# --- Interpretation / Discussion ---
st.header("📝 Interpretation / Discussion")
st.markdown(f"""
- Clusters reveal distinct crime profiles: some cities or regions show high violent crime but low white-collar crime, 
while others exhibit the opposite trend.
- The elbow method suggested that **k = {k_input}** provides a good balance between cluster compactness and simplicity.
- PCA visualization shows that clusters are well-separated, meaning the clustering captures underlying structure in the data.
- Policy makers can use this analysis to prioritize resources and tailor interventions for specific crime patterns.
""")
