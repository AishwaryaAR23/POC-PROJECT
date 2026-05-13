import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# Page Configuration
st.set_page_config(
    page_title="EV Charging Station Locator",
    layout="wide"
)

# Title
st.title("EV Charging Station Locator")

# Charging Station Dataset
stations = pd.DataFrame({
    "Name": [
        "Bangalore Station A",
        "Bangalore Station B",
        "Chennai Station A",
        "Hyderabad Station A",
        "Mumbai Station A",
        "Delhi Station A"
    ],

    "Latitude": [
        12.9716,
        12.9352,
        13.0827,
        17.3850,
        19.0760,
        28.6139
    ],

    "Longitude": [
        77.5946,
        77.6141,
        80.2707,
        78.4867,
        72.8777,
        77.2090
    ],

    "Type": [
        "Fast Charger",
        "Normal Charger",
        "Fast Charger",
        "Fast Charger",
        "Normal Charger",
        "Fast Charger"
    ]
})

# User Input
st.header("Enter Your Current Location")

latitude = st.number_input(
    "Enter Current Latitude",
    value=12.9700,
    format="%.4f"
)

longitude = st.number_input(
    "Enter Current Longitude",
    value=77.5900,
    format="%.4f"
)

battery = st.slider(
    "Battery Level (%)",
    0,
    100,
    30
)

# Session State Fix
if "show_result" not in st.session_state:
    st.session_state.show_result = False

# Button
if st.button("Find Nearest Stations"):
    st.session_state.show_result = True

# Show Results
if st.session_state.show_result:

    user_location = (latitude, longitude)

    # Distance Calculation
    stations["Distance (km)"] = stations.apply(
        lambda row: geodesic(
            user_location,
            (row["Latitude"], row["Longitude"])
        ).km,
        axis=1
    )

    # Get Nearest Stations
    nearest = stations.sort_values(
        "Distance (km)"
    ).head(3)

    # Display Table
    st.subheader("Nearest Charging Stations")

    st.dataframe(
        nearest[
            ["Name", "Type", "Distance (km)"]
        ]
    )

    # Battery Warning
    if battery < 20:
        st.warning(
            "Battery level is low. Please charge soon."
        )

    # Create Map
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=5
    )

    # User Marker
    folium.Marker(
        [latitude, longitude],
        tooltip="Your Location",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # Station Markers
    for _, row in nearest.iterrows():

        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            tooltip=row["Name"],
            popup=f"{row['Name']} - {row['Distance (km)']:.2f} km",
            icon=folium.Icon(color="green")
        ).add_to(m)

    # Display Map
    st.subheader("Charging Station Map")

    st_folium(
        m,
        width=1200,
        height=500
    )