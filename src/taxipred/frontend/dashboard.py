import streamlit as st
from taxipred.utils.helpers import (
    read_api_endpoint,
    calculate_base_fare,
    get_day_of_week,
    get_time_of_day,
    post_api_endpoint,
)
import pandas as pd
import requests
from taxipred.frontend.gmaps_utils import get_distance_km, get_coordinates
from datetime import datetime
import time as py_time


data = read_api_endpoint("taxi")

df = pd.DataFrame(data.json())


st.title("🚕 Taxi fare predictor")

form = st.form("Predict", border=True)
prediction = None

with form:
    st.markdown("### Enter your trip details below")
    col1, col2 = st.columns(2)
    start_address = col1.text_input("Start")
    destination_address = col2.text_input("Destination")

    # st.divider()

    selected_date = st.date_input("Date")
    selected_time_type = st.pills(
        "Departure/Arrival time",
        ["Departure time", "Arrival time"],
        selection_mode="single",
        default="Departure time",
    )
    selected_time = st.time_input(selected_time_type)

    submitted = st.form_submit_button("Predict")

    if submitted:
        time_of_day = get_time_of_day(selected_time.hour)
        day_of_week = get_day_of_week(selected_date)

        # Combine time and date to a full datetime object
        trip_datetime = datetime.combine(selected_date, selected_time)

        # Convert the full datetime object to Unix Timestamp which google maps uses
        trip_timestamp = int(py_time.mktime(trip_datetime.timetuple()))

        if trip_datetime < datetime.now():
            st.warning(
                "The selected time is in the past. Please choose a future date or time."
            )
        elif not start_address or not destination_address:
            st.warning("Please enter both start and destination addresses.")
        else:
            try:
                start_lat, start_lon = get_coordinates(start_address)
                dest_lat, dest_lon = get_coordinates(destination_address)

                with st.spinner("Calculating dstiance and fare..."):
                    if selected_time_type == "Departure time":
                        distance_km = get_distance_km(
                            start_lat,
                            start_lon,
                            dest_lat,
                            dest_lon,
                            departure_time=trip_timestamp,
                        )
                    else:
                        distance_km = get_distance_km(
                            start_lat,
                            start_lon,
                            dest_lat,
                            dest_lon,
                            arrival_time=trip_timestamp,
                        )

                    base_fare = calculate_base_fare(df, time_of_day, day_of_week)
                    payload = {
                        "Base_Fare": base_fare,
                        "Trip_Distance_km": distance_km,
                        "Time_of_Day": time_of_day,
                        "Day_of_Week": day_of_week,
                    }

                    response = post_api_endpoint(payload, "/taxi/predict")
                    response.raise_for_status()
                    prediction = response.json().get("predicted_trip_price")

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to get prediction from API: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")


if prediction is not None:
    st.success(f"Predicted price: {prediction:.2f} USD")
else:
    st.info("Fill in all fields and click *Predict* to calculate your taxi fare.")
