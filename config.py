"""
Application configuration settings.
"""

# -----------------------------
# Streamlit
# -----------------------------

PAGE_TITLE = "Traffic Accident Hotspot Analysis"

PAGE_ICON = "🚦"

LAYOUT = "wide"

# -----------------------------
# Machine Learning
# -----------------------------

DEFAULT_CLUSTERS = 5

MIN_CLUSTERS = 2

MAX_CLUSTERS = 10

RANDOM_STATE = 42

N_INIT = 10

# -----------------------------
# Map
# -----------------------------

DEFAULT_ZOOM = 5

MAP_HEIGHT = 650

# -----------------------------
# Files
# -----------------------------

DEFAULT_DATASET = "data/sample_accidents.csv"