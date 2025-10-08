import streamlit as st
from taxipred.utils.helpers import (
    read_api_endpoint,
    calculate_base_fare,
    get_day_of_week,
    get_time_of_day,
    post_api_endpoint,
)
import pandas as pd
from taxipred.frontend.gmaps_utils import get_distance_km, get_coordinates
import datetime
import time as py_time


data = read_api_endpoint("taxi")

df = pd.DataFrame(data.json())


# TODO
# - Start/end destination
# - Calculate distance
# - day
# - time
# - calculate base fare
# - get time of day/ day of week


def main():
    st.title("Taxi Fare")
    form = st.form("Predict", border=True)

    with form:
        st.markdown("# Enter your trip details below")
        col1, col2 = st.columns(2)
        start_address = col1.text_input("Start")
        destination_address = col2.text_input("Destination")
        st.divider()
        date = st.date_input("Date")
        test = st.pills(
            "departure/arrical",
            ["Departure time", "Arrival time"],
            selection_mode="single",
            default="Departure time",
        )
        if test == "Departure time":
            time = st.time_input("Departure time")
        else:
            time = st.time_input("Arrival time")

        submitted = st.form_submit_button("Predict")
        if submitted:
            time_of_day = get_time_of_day(time.hour)
            day_of_week = get_day_of_week(date)
            # Combine time and date to a full datetime object
            time_datetime = datetime.datetime.combine(date, time)
            # Convert the full datetime object to Unix Timestamp which google maps uses
            time_timestamp = int(py_time.mktime(time_datetime.timetuple()))
            if start_address and destination_address:
                if test == "Departure time":
                    start_lat, start_lon = get_coordinates(start_address)
                    dest_lat, dest_lon = get_coordinates(destination_address)
                    distance_km = get_distance_km(
                        start_lat,
                        start_lon,
                        dest_lat,
                        dest_lon,
                        departure_time=time_timestamp,
                    )
                else:
                    start_lat, start_lon = get_coordinates(start_address)
                    dest_lat, dest_lon = get_coordinates(destination_address)
                    distance_km = get_distance_km(
                        start_lat,
                        start_lon,
                        dest_lat,
                        dest_lon,
                        arrival_time=time_timestamp,
                    )
            base_fare = calculate_base_fare(df, time_of_day, day_of_week)
            payload = {
                "Base_Fare": base_fare,
                "Trip_Distance_km": distance_km,
                "Time_of_Day": time_of_day,
                "Day_of_Week": day_of_week,
            }
            response = post_api_endpoint(payload, "/taxi/predict")
            prediction = response.json().get("predicted_trip_price")
    st.write(prediction)


if __name__ == "__main__":
    main()
