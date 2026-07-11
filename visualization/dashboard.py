import streamlit as st
from models.evaluation import hotspot_statistics
from visualization.maps import hotspot_map
from utils.report_generator import generate_pdf_report

from visualization.charts import (
    severity_chart,
    weather_chart,
    vehicle_chart,
    road_type_chart,
    speed_chart,
    casualties_chart,
    monthly_chart
)

def show_dashboard(
    df,
    centers,
    heat_radius,
    heat_blur,
    heat_opacity
):

    st.divider()

    st.header("🗺️ Accident Hotspot Map")

    hotspot_map(
    df,
    centers,
    heat_radius,
    heat_blur,
    heat_opacity
)

    # ====================================
    # Accident Overview
    # ====================================

    st.header("📊 Accident Overview")

    col1, col2 = st.columns(2)

    with col1:
        severity_chart(df)

    with col2:
        weather_chart(df)

    st.divider()

    # ====================================
    # Vehicle & Road Analysis
    # ====================================

    st.header("🚗 Vehicle & Road Analysis")

    col3, col4 = st.columns(2)

    with col3:
        vehicle_chart(df)

    with col4:
        road_type_chart(df)

    st.divider()

    # ====================================
    # Speed & Casualties
    # ====================================

    st.header("⚠ Speed & Casualty Analysis")

    col5, col6 = st.columns(2)

    with col5:
        speed_chart(df)

    with col6:
        casualties_chart(df)

    st.divider()

    # ====================================
    # Monthly Trend
    # ====================================

    st.header("📈 Accident Trend")

    monthly_chart(df)

    st.divider()

    with st.expander("📋 View Filtered Dataset", expanded=False):

        st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    

    # ====================================
    # Data Table
    # ====================================


    # --------------------------
    # Download
    # --------------------------
    with st.expander("📥 Download Reports"):

        csv = df.to_csv(
        index=False
    )


    st.download_button(
        label="⬇ Download CSV Dataset",
        data=csv,
        file_name="filtered_accidents.csv",
        mime="text/csv"
    )


    pdf_file = "accident_report.pdf"


    generate_pdf_report(
        pdf_file,
        df,
        hotspot_statistics(df)
    )


    with open(pdf_file,"rb") as file:

        st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name="accident_analysis_report.pdf",
            mime="application/pdf"
        )

    # --------------------------
    # Dashboard Information
    # --------------------------
    with st.expander("ℹ Dashboard Information"):

        st.markdown("""
### Dashboard Overview

This dashboard provides:

- Interactive accident analysis
- Severity distribution
- Weather analysis
- Vehicle analysis
- Road type analysis
- Speed analysis
- Monthly accident trends
- Machine Learning based hotspot detection (Coming in Part 3)

### Technologies Used

- Python
- Streamlit
- Plotly
- Pandas
- NumPy
- Scikit-Learn
- Folium
""")