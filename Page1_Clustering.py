import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.express as px

st.title("📊 Crime Clustering with PCA")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/s22a0064-AinMaisarah/Crime_Assaigment/refs/heads/main/df_uber_cleaned.csv"
    return pd.read_csv(url, encoding="cp1252")

df = load_data()

features = ['violent_crime', 'property_crime', 'whitecollar_crime', 'social_crime']
X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

wcss = []
for k in range(2, 10):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(X_scaled)
    wcss.append(model.inertia_)

fig, ax = plt.subplots()
ax.plot(range(2, 10), wcss, marker='o')
ax.set_title('Elbow Method to Find Best k')
st.pyplot(fig)

model = KMeans(n_clusters=3, random_state=42, n_init=10)
df["crime_cluster"] = model.fit_predict(X_scaled)

pca = PCA(n_components=2)
pca_data = pca.fit_transform(X_scaled)
df["PC1"], df["PC2"] = pca_data[:,0], pca_data[:,1]

st.subheader("📍 PCA Cluster Visualization")
fig_clusters = px.scatter(
    df, x="PC1", y="PC2", color="crime_cluster",
    hover_data=features + ["state", "city_cat"],
    title="Crime Clusters (PCA)"
)
st.plotly_chart(fig_clusters)

cluster_profile = df.groupby("crime_cluster")[features].mean().reset_index()
melted = cluster_profile.melt(id_vars="crime_cluster", var_name="Crime", value_name="Avg Score")

st.subheader("📦 Cluster Crime Profiles")
fig_profile = px.bar(
    melted, x="Crime", y="Avg Score", color="crime_cluster", barmode="group",
    title="Average Crime Score Per Cluster"
)
st.plotly_chart(fig_profile)
