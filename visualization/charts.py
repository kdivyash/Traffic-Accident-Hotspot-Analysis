import plotly.express as px
import streamlit as st
import pandas as pd

def severity_chart(df):

    fig = px.histogram(
        df,
        x="severity",
        color="severity",
        title="Accident Severity Distribution",
        text_auto=True
    )

    fig.update_layout(
        height=420,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def weather_chart(df):

    fig = px.histogram(
        df,
        x="weather",
        color="severity",
        barmode="group",
        title="Weather vs Severity"
    )

    fig.update_layout(
        height=420,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def vehicle_chart(df):

    fig = px.histogram(
        df,
        x="vehicle_type",
        color="severity",
        title="Vehicle Type Analysis"
    )

    fig.update_layout(
        height=420,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def road_type_chart(df):

    fig = px.histogram(
        df,
        x="road_type",
        color="severity",
        title="Road Type Analysis"
    )

    fig.update_layout(
        height=420,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def speed_chart(df):

    fig = px.box(
        df,
        x="severity",
        y="speed_limit",
        color="severity",
        title="Speed Limit vs Severity"
    )

    fig.update_layout(
        height=420,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def casualties_chart(df):

    fig = px.histogram(
        df,
        x="casualties",
        nbins=15,
        title="Casualties Distribution"
    )

    fig.update_layout(
        height=420,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def monthly_chart(df):

    # Create month column
    monthly = (
        df.assign(month=df["date"].dt.month_name())
          .groupby("month")
          .size()
          .reset_index(name="Accidents")
    )

    # Order months correctly
    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    monthly["month"] = pd.Categorical(
        monthly["month"],
        categories=month_order,
        ordered=True
    )

    monthly = monthly.sort_values("month")

    fig = px.line(
        monthly,
        x="month",
        y="Accidents",
        markers=True,
        title="Monthly Accident Trend"
    )

    fig.update_layout(
        height=420,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )