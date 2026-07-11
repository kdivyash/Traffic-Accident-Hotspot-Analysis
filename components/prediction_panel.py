import streamlit as st
import pandas as pd


def prediction_panel(df, model, encoders):

    st.divider()

    st.header("🚦 Accident Severity Prediction")

    st.write(
        "Enter accident conditions to predict accident severity using Machine Learning."
    )


    col1, col2 = st.columns(2)


    with col1:

        weather = st.selectbox(
            "🌦 Weather Condition",
            sorted(df["weather"].unique())
        )


        vehicle = st.selectbox(
            "🚗 Vehicle Type",
            sorted(df["vehicle_type"].unique())
        )


        road_type = st.selectbox(
            "🛣 Road Type",
            sorted(df["road_type"].unique())
        )


        road_condition = st.selectbox(
            "Road Condition",
            sorted(df["road_condition"].unique())
        )


    with col2:

        light = st.selectbox(
            "💡 Light Condition",
            sorted(df["light_condition"].unique())
        )


        speed = st.slider(
            "Speed Limit",
            int(df["speed_limit"].min()),
            int(df["speed_limit"].max()),
            int(df["speed_limit"].median())
        )


        casualties = st.slider(
            "Casualties",
            int(df["casualties"].min()),
            int(df["casualties"].max()),
            1
        )


    if st.button(
        "🔮 Predict Severity"
    ):


        input_data = pd.DataFrame({

            "weather":[weather],

            "vehicle_type":[vehicle],

            "road_type":[road_type],

            "road_condition":[road_condition],

            "light_condition":[light],

            "speed_limit":[speed],

            "casualties":[casualties]

        })


        # Encode input values

        for col in input_data.columns:

            if col in encoders:

                input_data[col] = (
                    encoders[col]
                    .transform(input_data[col])
                )


        prediction = model.predict(
            input_data
        )[0]


        probability = model.predict_proba(
            input_data
        )[0]


        severity = (
            encoders["severity"]
            .inverse_transform(
                [prediction]
            )[0]
        )


        confidence = max(probability)

        # Get probability for each severity class

        probability_df = pd.DataFrame({

            "Severity": encoders["severity"].classes_,

            "Probability": probability

        })

        probability_df["Probability"] = (
            probability_df["Probability"] * 100
        )


        if severity == "Fatal":

            st.error(
                f"""
                🚨 Predicted Severity: **{severity}**

                🎯 Confidence:
                **{confidence:.2%}**
                """
            )


        elif severity == "Major":

            st.warning(
                f"""
                ⚠ Predicted Severity: **{severity}**

                🎯 Confidence:
                **{confidence:.2%}**
                """
            )


        else:

            st.success(
                f"""
                ✅ Predicted Severity: **{severity}**

                🎯 Confidence:
                **{confidence:.2%}**
                """
            )

        st.subheader(
            "📊 Prediction Probability"
        )


        st.bar_chart(
            probability_df.set_index(
                "Severity"
            )
        )