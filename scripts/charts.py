# https://plotly.com/python/map-configuration/


import pandas as pd
import altair as alt
import plotly.graph_objects as go
import streamlit as st


def scattergeo(lat: list, lon: list, hovertext: list) -> None:
    """
    Create a 3D outline map with given latitude, longitude, and popup text list.

    Args:
        lat (list): The list of latitudes.
        lon (list): The list of longitudes.
        hovertext (list): The list of popup texts.

    Returns:
        None
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            name="",
            lat=lat,
            lon=lon,
            hovertext=hovertext,
            mode="markers",
            marker=dict(
                size=10,
                opacity=1,
                color="orangered",
                symbol="hexagon2-open-dot"
                ),
        )
    )

    fig.update_geos(projection_type="natural earth")  # "natural earth"
    fig.update_layout(width=999, height=750)

    st.plotly_chart(fig, use_container_width=True)


def hourly_distribution(df: pd.DataFrame, x: str, y: str) -> None:
    """
    Create an hourly distribution bar chart with given x and y axis values.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        x (str): The column name to be used for the x-axis.
        y (str): The column name to be used for the y-axis.

    Returns:
        None
    """
    events = df.loc[:, y].tolist()
    scale = alt.Scale(domain=[0, max(events) + max(events) / 10])

    bars = (
        alt.Chart(data=df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X(x),
            y=alt.Y(y, scale=scale),
            color=alt.condition(
                alt.datum[y] == max(events),
                alt.value("orangered"),
                alt.value("white"),
            ),
        )
    )

    text = bars.mark_text(
        align="center",
        baseline="middle",
        dy=-10
    ).encode(text=f"{y}:O")

    st.altair_chart(bars + text, use_container_width=True)


def magnitude_distribution(df: pd.DataFrame, x: str, y: str) -> None:
    """
    Create a magnitude bar chart with given x and y axis values.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        x (str): The column name to be used for the x-axis.
        y (str): The column name to be used for the y-axis.

    Returns:
        None
    """
    events = df.loc[:, y].tolist()
    scale = alt.Scale(domain=[0, max(events) + max(events) / 10])

    bars = (
        alt.Chart(data=df)
        .mark_bar()
        .encode(
            x=alt.X(x),
            y=alt.Y(y, scale=scale),
            color=alt.condition(
                alt.datum[y] == max(events),
                alt.value("orangered"),
                alt.value("white"),
            ),
            tooltip=[x, y],
        )
        .interactive()
    )

    st.altair_chart(bars, use_container_width=True)

