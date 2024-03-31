import os
import logging
from typing import Tuple, Optional
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2 import Error
import streamlit as st
import charts

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load .env file
load_dotenv()

def fetch_data_from_postgres() -> Optional[Tuple[pd.DataFrame, str]]:
    """
    Fetch data from PostgreSQL database.

    Returns:
        Tuple containing DataFrame with the fetched data and maximum 'generated' value.
        Returns None if an error occurred.
    """
    try:
        # Connect to PostgreSQL database
        connection = psycopg2.connect(
            user="postgres",
            password=os.getenv("POSTGRES_PASSWORD"),
            host="localhost",
            port="5432",
            database="postgres"
        )

        cursor = connection.cursor()

        # Fetch data from the earthquakes table
        cursor.execute("SELECT * FROM earthquakes;")
        records = cursor.fetchall()

        # Convert records to DataFrame
        df = pd.DataFrame(records, columns=[column.name for column in cursor.description])

        # Get the maximum 'generated' value
        max_generated = df['generated'].max()

        logging.info("Data fetched successfully from PostgreSQL database.")
        return df, max_generated

    except (Exception, Error) as error:
        logging.error(f"Error while fetching data from PostgreSQL: {error}")
        return None

def main() -> None:
    """
    Main function to run the Streamlit app.
    """
    # Fetch data from PostgreSQL database
    df, max_generated = fetch_data_from_postgres()
    if df is not None:
        title = f"Earthquakes - mini batch (5 minutes) - last update: {max_generated}"
        st.set_page_config(
            page_title=title,
            initial_sidebar_state="expanded",
            layout="wide",
        )
        st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)

        st.markdown(
            """
            <style>
            .streamlit-expanderHeader, .streamlit-expanderContent {
                background: #E8DFDF;
                font-size: 25px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Initiating session state for location information
        if "location" not in st.session_state:
            st.session_state.location = None

        if df is not None and not df.empty:

            column_1 = st.text([""])

            with column_1:
                column_1_table_1, column_1_table_2 = st.columns(2)

                with column_1_table_1:
                    st.write("")
                    st.markdown(
                        """
                            <h3 style='text-align: center; color: orangered;'>
                            Grab a map to move it around
                            </h3>
                        """,
                        unsafe_allow_html=True,
                    )

                    df['hover_text'] = df['title'].apply(lambda x: f'<span style="font-size: 20px;">{x}</span>') \
                        + '<br><span style="font-size: 20px;">Time:</span> ' + df['time'].apply(lambda x: f'<span style="font-size: 20px;">{x}</span>') \
                        + '<br><span style="font-size: 20px;">Geometry coordinates:</span> ' + df['geometry_coordinates'].apply(lambda x: f'<span style="font-size: 20px;">{x}</span>')

                    charts.scattergeo(
                        lat=df["latitude"].tolist(),
                        lon=df["longitude"].tolist(),
                        hovertext=df['hover_text'],
                    )
                with column_1_table_2:
                    st.write("")
                    st.markdown(
                        """
                            <h3 style='text-align: center; color: orangered;'>
                            Hourly distribution of earthquakes
                            </h3>
                        """,
                        unsafe_allow_html=True,
                    )

                    hours_str = ["%.2d" % i for i in range(24)]
                    x_label = [f"{x}:00 - {x}:59" for x in hours_str]
                    df['time'] = pd.to_datetime(df['time'], utc=True)
                    hourly_earthquake_count = [
                        len(df[df['time'].dt.hour == hour])
                        for hour in range(24)
                    ]

                    chart_data1 = pd.DataFrame(
                        {
                            "Time Period": x_label,
                            "Number of Events": hourly_earthquake_count,
                        }
                    )

                    charts.hourly_distribution(
                        df=chart_data1, x="Time Period", y="Number of Events"
                    )

                    st.markdown(
                        """
                            <h3 style='text-align: center; color: orangered;'>
                            Magnitude distribution of earthquakes
                            </h3>
                        """,
                        unsafe_allow_html=True,
                    )

                    magnitudes = sorted(df["mag"].unique())
                    events = [len(df.loc[df["mag"] == mag]) for mag in magnitudes]
                    chart_data2 = pd.DataFrame({"Magnitude": magnitudes, "Number of Events": events})
                    charts.magnitude_distribution(
                        df=chart_data2, x="Magnitude", y="Number of Events"
                    )

            st.markdown(
                """
                    <h3 style='text-align: center; color: orangered;'>
                    Most recent entries
                    </h3>
                """,
                unsafe_allow_html=True,
            )

            # Display the most recent rows
            st.table(df[
                [
                    "generated",
                    "metadata_url",
                    "metadata_title",
                    "title",
                    "time",
                    "geometry_coordinates",
                    "id"
                ]].tail())

        else:
            st.warning("No values to show")


if __name__ == "__main__":
    main()
