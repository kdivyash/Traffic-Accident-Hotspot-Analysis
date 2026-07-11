import streamlit as st

def page_configuration():

    # Configure the page FIRST
    st.set_page_config(
        page_title="Traffic Accident Hotspot Analysis",
        page_icon="🚦",
        layout="wide"
    )

    # Load custom CSS
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

def display_header():

    st.title("🚦 Traffic Accident Hotspot Analysis")

    st.markdown("""
### 📍 AI Powered Geospatial Analytics Dashboard

Analyze road accidents using **Machine Learning**, **Interactive Maps**, and
**Data Visualization** to identify high-risk locations and improve road safety.
""")

    st.divider()

def sidebar_filters(df):

    st.sidebar.title("Filters")

    city = st.sidebar.multiselect(
        "City",
        options=sorted(df["city"].unique()),
        default=sorted(df["city"].unique())
    )

    severity = st.sidebar.multiselect(
        "Severity",
        options=sorted(df["severity"].unique()),
        default=sorted(df["severity"].unique())
    )

    weather = st.sidebar.multiselect(
        "Weather",
        options=sorted(df["weather"].unique()),
        default=sorted(df["weather"].unique())
    )

    vehicle = st.sidebar.multiselect(
        "Vehicle Type",
        options=sorted(df["vehicle_type"].unique()),
        default=sorted(df["vehicle_type"].unique())
    )

    road = st.sidebar.multiselect(
        "Road Type",
        options=sorted(df["road_type"].unique()),
        default=sorted(df["road_type"].unique())
    )

    filtered = df[
        (df["city"].isin(city)) &
        (df["severity"].isin(severity)) &
        (df["weather"].isin(weather)) &
        (df["vehicle_type"].isin(vehicle)) &
        (df["road_type"].isin(road))
    ]

    st.sidebar.markdown("---")

    st.sidebar.info("""
    👨‍💻 **Developer:** K Divyash

    🚦 **Project:**
    Traffic Accident Hotspot Analysis

    🛠 **Tech Stack**
    - Python
    - Streamlit
    - Plotly
    - Folium
    - Scikit-Learn
    - Pandas
    - NumPy
    """)

    return filtered

def show_kpi_cards(df):

    total=len(df)

    fatal=len(df[df["severity"]=="Fatal"])

    major=len(df[df["severity"]=="Major"])

    minor=len(df[df["severity"]=="Minor"])

    casualties=df["casualties"].sum()

    c1,c2,c3,c4,c5=st.columns(5)

    c1.metric("🚨 Total",total)

    c2.metric("☠ Fatal",fatal)

    c3.metric("⚠ Major",major)

    c4.metric("✅ Minor",minor)

    c5.metric("🏥 Casualties",casualties)