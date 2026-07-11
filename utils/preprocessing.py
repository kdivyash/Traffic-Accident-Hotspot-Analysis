import pandas as pd


def preprocess_data(df):

    # -----------------------------
    # Standardize Column Names
    # -----------------------------
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # -----------------------------
    # Required Columns
    # -----------------------------
    required_columns = [
        "latitude",
        "longitude",
        "severity",
        "weather",
        "time",
        "date",
        "vehicle_type",
        "road_type",
        "road_condition",
        "light_condition",
        "speed_limit",
        "casualties",
        "city"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing Columns: {missing}"
        )

    # -----------------------------
    # Convert Date
    # -----------------------------
    df["date"] = pd.to_datetime(df["date"])

    # -----------------------------
    # Remove Missing Values
    # -----------------------------
    df = df.dropna()

    # -----------------------------
    # Remove Duplicates
    # -----------------------------
    df = df.drop_duplicates()

    # -----------------------------
    # Validate Coordinates
    # -----------------------------
    df = df[
        (df["latitude"] >= -90) &
        (df["latitude"] <= 90)
    ]

    df = df[
        (df["longitude"] >= -180) &
        (df["longitude"] <= 180)
    ]

    # -----------------------------
    # Sort Dataset
    # -----------------------------
    df = df.sort_values("date")

    # -----------------------------
    # Reset Index
    # -----------------------------
    df.reset_index(
        drop=True,
        inplace=True
    )

    return df