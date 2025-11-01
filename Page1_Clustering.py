import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go

# --- Streamlit App ---
st.set_page_config(page_title="Crime Clustering Dashboard", layout="wide")
st.title("Urban Crime Clustering Analysis")

st.header("🎯 Objective Statement")
st.markdown("""
The objective of this visualization is to identify patterns in urban crime by grouping similar crime profiles 
using K-Means clustering and visualizing these patterns with PCA for a 2D interactive view. 
This helps understand how different crime types co-occur across regions and demographics.
""")

# --- Load Dataset ---
CSV_URL = 'https://raw.githubusercontent.com/s22a0064-AinMaisarah/UrbanCrime/refs/heads/main/df_uber_cleaned.csv'
df = pd.read_csv(CSV_URL, encoding='cp1252')

# --- Select crime-related features ---
features = ['violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime']
X = df[features]

# --- Scale features ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- Determine optimal number of clusters using Elbow Method ---
wcss = []
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# --- Elbow Method Plot using Plotly ---
fig_elbow = go.Figure()
fig_elbow.add_trace(go.Scatter(
    x=list(range(2, 10)),
    y=wcss,
    mode='lines+markers',
    name='WCSS'
))
fig_elbow.update_layout(
    title='Elbow Method for Optimal k',
    xaxis_title='Number of Clusters',
    yaxis_title='WCSS',
    template='plotly_white'
)
st.plotly_chart(fig_elbow, use_container_width=True)

# --- Apply K-Means clustering (choosing k=3) ---
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['crime_cluster'] = kmeans.fit_predict(X_scaled)

# --- PCA for 2D visualization ---
pca = PCA(n_components=2)
pca_data = pca.fit_transform(X_scaled)
df['PC1'] = pca_data[:, 0]
df['PC2'] = pca_data[:, 1]

# --- PCA Cluster Scatter Plot ---
fig_clusters = px.scatter(
    df,
    x='PC1',
    y='PC2',
    color='crime_cluster',
    hover_data=['crime_cluster'] + features + ['city_cat', 'state', 'age', 'income', 'poverty'],
    title='Crime Pattern Clusters (PCA)',
    labels={'crime_cluster': 'Crime Cluster'},
    template='plotly_white'
)
st.plotly_chart(fig_clusters, use_container_width=True)

# --- Cluster Profiles ---
cluster_profile = df.groupby('crime_cluster')[features].mean().reset_index()
cluster_profile_melted = cluster_profile.melt(
    id_vars='crime_cluster', var_name='Crime Type', value_name='Average Crime Score'
)

# --- Interactive Bar Chart of Cluster Profiles ---
fig_cluster_profile = px.bar(
    cluster_profile_melted,
    x='Crime Type',
    y='Average Crime Score',
    color='crime_cluster',
    barmode='group',
    hover_data=['crime_cluster', 'Crime Type', 'Average Crime Score'],
    title='Average Crime Scores per Cluster',
    labels={'crime_cluster': 'Crime Cluster'},
    template='plotly_white'
)
st.plotly_chart(fig_cluster_profile, use_container_width=True)








