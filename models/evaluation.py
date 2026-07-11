import pandas as pd
import plotly.express as px

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from config import RANDOM_STATE, N_INIT

def calculate_wcss(df, max_clusters=10):
    """
    Calculate WCSS for the Elbow Method.
    """

    coordinates = df[["latitude", "longitude"]]

    wcss = []

    for k in range(2, max_clusters + 1):

        model = KMeans(
            n_clusters=k,
            random_state=RANDOM_STATE,
            n_init=N_INIT
        )

        model.fit(coordinates)

        wcss.append(model.inertia_)

    return wcss


def calculate_silhouette(df, n_clusters):
    """
    Calculate the Silhouette Score.
    """

    coordinates = df[["latitude", "longitude"]]

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(coordinates)

    score = silhouette_score(
        coordinates,
        labels
    )

    return score



def hotspot_statistics(df):
    """
    Returns cluster statistics sorted by number of accidents.
    """

    stats = (
        df.groupby("cluster")
        .size()
        .reset_index(name="Accidents")
        .sort_values("Accidents", ascending=False)
    )

    stats["Rank"] = range(1, len(stats) + 1)

    return stats



def elbow_chart(wcss):

    

    df = pd.DataFrame({
        "Clusters": list(range(2, len(wcss)+2)),
        "WCSS": wcss
    })

    fig = px.line(
        df,
        x="Clusters",
        y="WCSS",
        markers=True,
        title="Elbow Method"
    )

    fig.update_layout(
        template="plotly_white",
        height=420
    )

    return fig


def recommend_clusters(df, min_clusters=2, max_clusters=10):
    """
    Finds the best number of clusters using the Silhouette Score.
    """

    coordinates = df[["latitude", "longitude"]]

    best_score = -1
    best_k = min_clusters

    scores = []

    for k in range(min_clusters, max_clusters + 1):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(coordinates)

        score = silhouette_score(
            coordinates,
            labels
        )

        scores.append(score)

        if score > best_score:
            best_score = score
            best_k = k

    return best_k, best_score, scores

def silhouette_chart(scores):
    """
    Creates a Silhouette Score line chart.
    """

    df = pd.DataFrame({
        "Clusters": list(range(2, len(scores) + 2)),
        "Silhouette Score": scores
    })

    fig = px.line(
        df,
        x="Clusters",
        y="Silhouette Score",
        markers=True,
        title="Silhouette Score vs Number of Clusters"
    )

    fig.update_layout(
        template="plotly_white",
        height=420
    )

    return fig