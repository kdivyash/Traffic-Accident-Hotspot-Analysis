import pandas as pd
import numpy as np

np.random.seed(42)

cities = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Jaipur": (26.9124, 75.7873),
    "Ahmedabad": (23.0225, 72.5714)
}

vehicle_types = [
    "Car",
    "Bike",
    "Truck",
    "Bus",
    "Auto",
    "Bicycle"
]

weather_conditions = [
    "Clear",
    "Rainy",
    "Foggy",
    "Cloudy"
]

road_conditions = [
    "Dry",
    "Wet",
    "Under Construction"
]

road_types = [
    "Highway",
    "City Road",
    "Rural Road"
]

light_conditions = [
    "Daylight",
    "Night",
    "Street Lights"
]

severity = [
    "Minor",
    "Major",
    "Fatal"
]

rows = []

for accident_id in range(1,10001):

    city = np.random.choice(list(cities.keys()))

    lat,lon = cities[city]

    latitude = lat + np.random.normal(0,0.08)

    longitude = lon + np.random.normal(0,0.08)

    date = pd.Timestamp("2024-01-01") + pd.to_timedelta(
        np.random.randint(0,365),
        unit="D"
    )

    hour = np.random.randint(0,24)

    minute = np.random.randint(0,60)

    time = f"{hour:02}:{minute:02}"

    casualties = np.random.poisson(2)

    rows.append({

        "Accident_ID": accident_id,

        "City": city,

        "Latitude": latitude,

        "Longitude": longitude,

        "Date": date,

        "Time": time,

        "Severity": np.random.choice(
            severity,
            p=[0.55,0.30,0.15]
        ),

        "Vehicle_Type": np.random.choice(vehicle_types),

        "Weather": np.random.choice(weather_conditions),

        "Road_Condition": np.random.choice(road_conditions),

        "Road_Type": np.random.choice(road_types),

        "Light_Condition": np.random.choice(light_conditions),

        "Speed_Limit": np.random.choice(
            [30,40,50,60,80,100]
        ),

        "Casualties": casualties

    })

df = pd.DataFrame(rows)

df.to_csv(
    "data/sample_accidents.csv",
    index=False
)

print(df.head())

print("\nDataset Created Successfully")