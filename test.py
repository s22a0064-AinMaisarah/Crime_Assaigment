import streamlit as st

st.set_page_config(page_title="Crime Analytics Dashboard", page_icon="🚓")

home = st.Page("home.py", title="🏠 Home", default=True)
page1 = st.Page("Page1_Clustering.py", title="📊 Crime Clustering (PCA)")
page2 = st.Page("Page2_IncomeCrime.py", title="💰 Income vs Crime Analysis")
page3 = st.Page("Page3_RadarAge.py", title="🧭 Crime Radar by Age Group")

navigation = st.navigation(
    {
        "Menu": [home, page1, page2, page3]
    }
)

navigation.run()
