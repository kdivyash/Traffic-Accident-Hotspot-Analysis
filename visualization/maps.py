import streamlit as st
import folium
from streamlit_folium import st_folium
from config import DEFAULT_ZOOM
from config import MAP_HEIGHT

from folium.plugins import (
    HeatMap,
    MarkerCluster,
    MiniMap,
    Fullscreen,
    MeasureControl,
    MousePosition
)

def hotspot_map(
    df,
    centers,
    heat_radius,
    heat_blur,
    heat_opacity
):
    st.write(centers.head())

    # Create base map
    m = folium.Map(
        location=[
            df["latitude"].mean(),
            df["longitude"].mean()
        ],
        zoom_start=DEFAULT_ZOOM,
        control_scale=True
    )

    # st.write("Map created successfully")


    # -----------------------
    # Feature Groups
    # -----------------------

    accident_layer = folium.FeatureGroup(
    name="🚗 Accident Markers",
    show=True
)

    heatmap_layer = folium.FeatureGroup(
    name="🔥 Heatmap",
    show=True
)

    hotspot_layer = folium.FeatureGroup(
    name="📍 Hotspot Centers",
    show=True
)

    # -----------------------
    # Marker Cluster
    # -----------------------
    marker_cluster = MarkerCluster().add_to(accident_layer)

    # Accident markers
    for _, row in df.iterrows():

        if row["severity"] == "Fatal":
            color = "red"

        elif row["severity"] == "Major":
            color = "orange"

        else:
            color = "green"

        folium.CircleMarker(
            location=[
                row["latitude"],
                row["longitude"]
            ],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"""
            City: {row['city']}<br>
            Severity: {row['severity']}<br>
            Weather: {row['weather']}
            """
        ).add_to(marker_cluster)
    # -----------------------
    # Cluster Statistics
    # -----------------------

    #st.write("Checking columns:")
    #st.write(df.columns)

    cluster_counts = (
        df.groupby("cluster")
        .size()
        .reset_index(name="Accidents")
)
    hotspots = centers.merge(
    cluster_counts,
    on="cluster"
)

    hotspots = hotspots.sort_values(
    "Accidents",
    ascending=False
    ).reset_index(drop=True)

    # -----------------------
    # Cluster Centers
    # -----------------------

    for rank, (_, hotspot) in enumerate(hotspots.iterrows(), start=1):

        accidents = hotspot["Accidents"]

        # Assign colors based on hotspot rank
        if rank == 1:
            marker_color = "red"
        elif rank == 2:
            marker_color = "orange"
        elif rank == 3:
            marker_color = "blue"
        else:
            marker_color = "black"

        risk = (
            "🔴 Very High"
            if rank == 1
            else "🟠 High"
            if rank == 2
            else "🟡 Moderate"
            if rank == 3
            else "🟢 Low"
        )

        popup_html = f"""
        <div style="
        width:240px;
        padding:10px;
        font-family:Arial;
        ">

        <h4 style="margin-bottom:10px;">
        🚨 Hotspot #{rank}
        </h4>

        <b>🚗 Estimated Accidents:</b> {accidents}<br>

        <b>📍 Latitude:</b> {hotspot["latitude"]:.4f}<br>

        <b>📍 Longitude:</b> {hotspot["longitude"]:.4f}<br>

        <b>⚠ Risk Level:</b> {risk}<br>

        <b>⭐ Priority:</b> {"Immediate Action" if rank == 1 else "Monitoring"}

        </div>
        """

        folium.Marker(
            location=[
    hotspot["latitude"],
    hotspot["longitude"]
],
            tooltip=f"Hotspot #{rank}",
            popup=folium.Popup(
                popup_html,
                max_width=260
            ),
            icon=folium.Icon(
                color=marker_color,
                icon="exclamation-triangle",
                prefix="fa"
            )
        ).add_to(hotspot_layer)
        
    # -----------------------
    # Heatmap
    # -----------------------
    HeatMap(
        df[["latitude", "longitude"]].values.tolist(),
        radius=heat_radius,
        blur=heat_blur,
        min_opacity=heat_opacity
    ).add_to(heatmap_layer)

    # -----------------------
    # Plugins
    # -----------------------
    MiniMap().add_to(m)

    Fullscreen().add_to(m)

    MeasureControl().add_to(m)

    MousePosition().add_to(m)

    # -----------------------
    # Map Legend
    # -----------------------

    legend_html = """
    <div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 240px;
    background-color: white;
    border:2px solid grey;
    z-index:9999;
    font-size:14px;
    padding:12px;
    border-radius:10px;
    box-shadow:2px 2px 8px rgba(0,0,0,0.3);
    ">

    <b>🚨 Accident Legend</b><br><br>

    🟢 Minor Accident<br>
    🟠 Major Accident<br>
    🔴 Fatal Accident<br>

    <hr>

    <b>🏆 Hotspot Ranking</b><br>

    🔴 Rank #1 Hotspot<br>
    🟠 Rank #2 Hotspot<br>
    🔵 Rank #3 Hotspot<br>
    ⚫ Other Hotspots

    </div>
    """

    m.get_root().html.add_child(
        folium.Element(legend_html)
    )

    accident_layer.add_to(m)
    heatmap_layer.add_to(m)
    hotspot_layer.add_to(m)

    folium.LayerControl().add_to(m)

    # Display map
    st_folium(
    m,
    width=900,
    height=600
)