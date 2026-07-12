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
    width: 250px;
    background-color: white;
    color: #222222;
    border: 2px solid #444;
    border-radius: 10px;
    padding: 12px;
    font-size: 14px;
    font-family: Arial, sans-serif;
    line-height: 1.7;
    box-shadow: 0 4px 10px rgba(0,0,0,0.35);
    z-index: 9999;
    ">

    <h4 style="margin:0 0 10px 0; color:#222;">
    🚨 Accident Legend
    </h4>

    <span style="color:green;">●</span> Minor Accident<br>
    <span style="color:orange;">●</span> Major Accident<br>
    <span style="color:red;">●</span> Fatal Accident

    <hr style="margin:10px 0;">

    <h4 style="margin:0 0 10px 0; color:#222;">
    🏆 Hotspot Ranking
    </h4>

    <span style="color:red;">●</span> Rank #1 Hotspot<br>
    <span style="color:orange;">●</span> Rank #2 Hotspot<br>
    <span style="color:blue;">●</span> Rank #3 Hotspot<br>
    <span style="color:black;">●</span> Other Hotspots

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
    width=None,
    height=650,
    use_container_width=True
)