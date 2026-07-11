import pandas as pd
from pandas.api.types import is_string_dtype
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def train_prediction_model(df):
    """
    Train a Random Forest model to predict accident severity.
    """

    data = df.copy()

    features = [
        "weather",
        "vehicle_type",
        "road_type",
        "road_condition",
        "light_condition",
        "speed_limit",
        "casualties"
    ]

    target = "severity"

    categorical_columns = [
        "weather",
        "vehicle_type",
        "road_type",
        "road_condition",
        "light_condition",
        "severity"
    ]

    encoders = {}

    for column in categorical_columns:
        encoder = LabelEncoder()
        data[column] = encoder.fit_transform(data[column].astype(str))
        encoders[column] = encoder

    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    print("Feature dtypes:")
    print(X.dtypes)

    print("\nMissing values:")
    print(X.isnull().sum())

    print("\nFirst 5 rows:")
    print(X.head())

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    return model, encoders, accuracy