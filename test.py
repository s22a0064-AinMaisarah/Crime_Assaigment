import streamlit as st
st.set_page_config(
    page_title="SCrime Analytics Dashboard"
)
visualise = st.Page('Crime.py', title='Crime Visualization Dashboard ', icon=":material/school:")

home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [home, visualise]
        }
    )

pg.run()
