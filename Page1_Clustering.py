import streamlit as st
import pandas as pd
import numpy as np # Used for placeholder data
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns # Not directly used in plotting, but often useful
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

url = "https://raw.githubusercontent.com/s22a0064-AinMaisarah/Crime_Assaigment/refs/heads/main/df_uber_cleaned.csv"
df = pd.read_csv(url)
st.header("📊 Summary of Cluster Analysis")

# Example metrics: you could compute averages or counts dynamically
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Number of Clusters", value=f"{k_input}")
col2.metric(label="Average Violent Crime", value=f"{df_uber_cleaned['violent_crime'].mean():.2f}")
col3.metric(label="Average Property Crime", value=f"{df_uber_cleaned['property_crime'].mean():.2f}")
col4.metric(label="Average White-collar Crime", value=f"{df_uber_cleaned['whitecollar_crime'].mean():.2f}")

st.markdown("""
**Summary:** This analysis identifies distinct clusters of crime patterns. Cluster profiling shows 
that some clusters are dominated by violent crimes while others have higher white-collar or property crimes. 
The PCA visualization demonstrates that clusters are fairly well-separated in 2D space, 
indicating meaningful groupings that can support targeted policy interventions and resource allocation.
""")


## 🔬 Clustering Pipeline

# Select crime-related columns
features = ['violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime']
X = df_uber_cleaned[features]

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---
### 1. Elbow Method for Optimal k

st.header('1. Optimal Cluster Determination (Elbow Method)')
col1, col2 = st.columns([1, 1])

with col1:
    # Determine optimal number of clusters using the Elbow Method
    wcss = []  # within-cluster-sum-of-squares
    for k in range(2, 10):
        # Added n_init=10 to address future changes in sklearn (or to match the original code)
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10) 
        kmeans.fit(X_scaled)
        wcss.append(kmeans.inertia_)

    # Plot the Elbow Method (using Matplotlib)
    fig_elbow, ax = plt.subplots(figsize=(7, 5))
    ax.plot(range(2, 10), wcss, marker='o')
    ax.set_title('Elbow Method for Optimal k')
    ax.set_xlabel('Number of Clusters (k)')
    ax.set_ylabel('WCSS (Inertia)')
    
    # **Display the Matplotlib plot in Streamlit**
    st.pyplot(fig_elbow)

with col2:
    st.markdown("""
    The **Elbow Method** helps choose the best number of clusters ($k$). 
    The 'elbow' point is where the rate of decrease in the **WCSS** (Within-Cluster Sum-of-Squares) 
    dramatically slows down.
    """)
    
    # Streamlit sidebar input for selecting K
    k_input = st.slider('Select the Optimal Number of Clusters (k)', 2, 8, 3, help="Adjust this based on the elbow plot.")


# ---
### 2. K-Means Clustering and PCA

st.header('2. K-Means Clustering Results')

# Apply K-Means clustering (using the selected k)
kmeans = KMeans(n_clusters=k_input, random_state=42, n_init=10)
df_uber_cleaned['crime_cluster'] = kmeans.fit_predict(X_scaled).astype(str) # Convert to string for better Plotly color legend

# Perform PCA for visualization
pca = PCA(n_components=2)
pca_data = pca.fit_transform(X_scaled)

df_uber_cleaned['PC1'] = pca_data[:, 0]
df_uber_cleaned['PC2'] = pca_data[:, 1]

# Visualize the clusters using PCA with Plotly Express for interactivity
fig_clusters = px.scatter(
    df_uber_cleaned,
    x='PC1',
    y='PC2',
    color='crime_cluster',
    hover_data=['crime_cluster', 'violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime', 'city_cat', 'state', 'age', 'income', 'poverty'],
    title='Crime Pattern Clusters (PCA Visualization)',
    labels={'crime_cluster': 'Crime Cluster'},
    height=550
)
# **Display the Plotly figure in Streamlit**
st.plotly_chart(fig_clusters, use_container_width=True)


# ---
## 📈 Cluster Profile Analysis

st.header('3. Cluster Profile Bar Chart')

# Analyze cluster profiles
cluster_profile = df_uber_cleaned.groupby('crime_cluster')[features].mean().reset_index()
cluster_profile_melted = cluster_profile.melt(id_vars='crime_cluster', var_name='Crime Type', value_name='Average Crime Score')

# Visualize cluster profiles interactively using Plotly Express
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
# **Display the second Plotly figure in Streamlit**
st.plotly_chart(fig_cluster_profile, use_container_width=True)

st.header("📝 Interpretation / Discussion")
st.markdown("""
- Clusters reveal distinct crime profiles: some cities or regions show high violent crime but low white-collar crime, 
while others exhibit the opposite trend.
- The elbow method suggested that **k = {0}** provides a good balance between cluster compactness and simplicity.
- PCA visualization shows that clusters are well-separated, meaning the clustering captures underlying structure in the data.
- Policy makers can use this analysis to prioritize resources and tailor interventions for specific crime patterns.
""".format(k_input))

