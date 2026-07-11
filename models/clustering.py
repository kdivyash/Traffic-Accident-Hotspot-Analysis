from sklearn.cluster import KMeans
import pandas as pd


def perform_kmeans(df, n_clusters=5):
    """
    Performs K-Means clustering using latitude and longitude.
    Returns:
        updated dataframe
        cluster centers
        trained model
    """

    coordinates = df[["latitude", "longitude"]].copy()

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    df = df.copy()
    df["cluster"] = model.fit_predict(coordinates)

    centers = pd.DataFrame(
    model.cluster_centers_,
    columns=["latitude", "longitude"]
)

# Add cluster ID
    centers["cluster"] = centers.index

    return df, centers, model