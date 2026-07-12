import streamlit as st
from models.evaluation import silhouette_chart
from models.evaluation import recommend_clusters
from models.evaluation import (
    calculate_silhouette,
    calculate_wcss,
    hotspot_statistics,
    elbow_chart
)
from models.clustering import perform_kmeans
from models.evaluation import calculate_silhouette
from utils.data_loader import load_dataset
from utils.preprocessing import preprocess_data
from utils.ui import (
    page_configuration,
    display_header,
    sidebar_filters,
    show_kpi_cards,
)

from visualization.dashboard import show_dashboard
from models.prediction import train_prediction_model
from components.prediction_panel import prediction_panel
from components.ai_insights import show_ai_insights

# ----------------------------------------
# Page Configuration
# ----------------------------------------
page_configuration()

# ----------------------------------------
# Header
# ----------------------------------------
display_header()

# ----------------------------------------
# Load Dataset
# ----------------------------------------
with st.spinner("Loading dataset..."):
    df = load_dataset()

# ----------------------------------------
# Preprocess Dataset
# ----------------------------------------
with st.spinner("Preprocessing dataset..."):
    df = preprocess_data(df)

# ----------------------------------------
# Sidebar Filters
# ----------------------------------------
filtered_df = sidebar_filters(df)

from config import (
    MIN_CLUSTERS,
    MAX_CLUSTERS,
    DEFAULT_CLUSTERS
)

cluster_count = st.sidebar.slider(
    "Number of Clusters",
    MIN_CLUSTERS,
    MAX_CLUSTERS,
    DEFAULT_CLUSTERS
)

st.sidebar.markdown("---")
st.sidebar.subheader("🗺️ Map Controls")

heat_radius = st.sidebar.slider(
    "Heatmap Radius",
    min_value=5,
    max_value=40,
    value=18
)

heat_blur = st.sidebar.slider(
    "Heatmap Blur",
    min_value=5,
    max_value=30,
    value=15
)

heat_opacity = st.sidebar.slider(
    "Minimum Opacity",
    min_value=0.1,
    max_value=1.0,
    value=0.4,
    step=0.1
)

clustered_df, centers, model = perform_kmeans(
    filtered_df,
    cluster_count
)

silhouette = calculate_silhouette(
    clustered_df,
    cluster_count
)

wcss = calculate_wcss(filtered_df)

recommended_k, recommended_score, scores = recommend_clusters(
    filtered_df
)

stats = hotspot_statistics(clustered_df)


# ----------------------------------------
# Train Prediction Model
# ----------------------------------------

prediction_model, encoders, accuracy = train_prediction_model(
    clustered_df
)

# ----------------------------------------
# KPI Cards
# ----------------------------------------
# ----------------------------------------
# Machine Learning Dashboard
# ----------------------------------------

# ----------------------------------------
# Machine Learning Analysis
# ----------------------------------------

st.header("🤖 Machine Learning Analysis")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Silhouette Score",
        f"{silhouette:.3f}"
    )

with col2:
    st.metric(
        "Recommended Clusters",
        recommended_k
    )

with col3:
    st.metric(
        "Current Clusters",
        cluster_count
    )

with col4:
    st.metric(
        "Hotspots Found",
        len(centers)
    )
with col5:
    st.metric(
        "Prediction Accuracy",
        f"{accuracy:.2%}"
    )

st.success(
    f"""
✅ Best cluster count: **{recommended_k}**

Highest Silhouette Score: **{recommended_score:.3f}**
"""
)

# ----------------------------------------
# Evaluation Charts
# ----------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        elbow_chart(wcss),
        width="stretch"
    )

with col2:
    st.plotly_chart(
        silhouette_chart(scores),
        width="stretch"
    )

st.subheader("🏆 Hotspot Ranking")

st.dataframe(
    stats,
    width="stretch",
    hide_index=True
)

# ----------------------------------------
# AI Insights
# ----------------------------------------

st.subheader("💡 AI-Powered Insights")

largest = stats.iloc[0]

st.success(
    f"""
### Highest Risk Hotspot

🚨 **Cluster {largest['cluster']}** has the highest concentration of accidents.

**Total Accidents:** {largest['Accidents']}

**Recommendation:**
- Increase traffic police deployment.
- Install additional warning signs.
- Improve road lighting and maintenance.
- Conduct regular road safety audits.
"""
)


show_dashboard(
    clustered_df,
    centers,
    heat_radius,
    heat_blur,
    heat_opacity
)
prediction_panel(
    clustered_df,
    prediction_model,
    encoders
)
show_ai_insights(
    clustered_df
)