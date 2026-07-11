import streamlit as st


def show_ai_insights(df):

    st.divider()

    st.header("💡 AI Generated Safety Insights")


    # -----------------------------
    # Highest Risk City
    # -----------------------------

    city_risk = (
        df.groupby("city")
        .size()
        .sort_values(
            ascending=False
        )
    )

    highest_city = city_risk.index[0]
    city_accidents = city_risk.iloc[0]


    st.error(
        f"""
        🚨 **Highest Risk City**

        📍 {highest_city}

        Total Accidents:
        **{city_accidents}**

        Recommendation:
        Increase traffic monitoring and improve accident prevention measures.
        """
    )


    # -----------------------------
    # Dangerous Road Type
    # -----------------------------

    road_risk = (
        df.groupby("road_type")
        .size()
        .sort_values(
            ascending=False
        )
    )

    risky_road = road_risk.index[0]
    road_accidents = road_risk.iloc[0]


    st.warning(
        f"""
        🛣️ **Most Dangerous Road Type**

        {risky_road}

        Accidents:
        **{road_accidents}**

        Recommendation:
        Improve road infrastructure and safety signs.
        """
    )


    # -----------------------------
    # Weather Analysis
    # -----------------------------

    weather_risk = (
        df.groupby("weather")
        .size()
        .sort_values(
            ascending=False
        )
    )

    risky_weather = weather_risk.index[0]


    st.info(
        f"""
        🌦️ **High Risk Weather Condition**

        {risky_weather}

        Recommendation:
        Implement additional warnings and speed control during this condition.
        """
    )


    # -----------------------------
    # Vehicle Analysis
    # -----------------------------

    vehicle_risk = (
        df.groupby("vehicle_type")
        .size()
        .sort_values(
            ascending=False
        )
    )

    risky_vehicle = vehicle_risk.index[0]


    st.success(
        f"""
        🚗 **Highest Accident Involvement Vehicle**

        {risky_vehicle}

        Recommendation:
        Focus safety campaigns on this vehicle category.
        """
    )