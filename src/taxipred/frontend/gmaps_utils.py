import googlemaps
from googlemaps.exceptions import HTTPError
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


# Used documentation and got some help from Gemini to set up these functions
@st.cache_resource
def get_gmaps_client(api_key: str):
    """
    Initializes and caches the Google Maps client for the Streamlit app.
    Uses st.cache_resource to prevent re-initialization on every rerun.
    """
    if not api_key:
        st.error("API Key not set. Please update the API_KEY variable.")
        st.stop()

    try:
        # Create client
        client = googlemaps.Client(api_key)
        return client

    except Exception as e:
        #
        st.error(
            f"Could not initialize Google Maps Client. Check key and enabled APIs (Geocoding, Distance Matrix, Places). Error: {e}"
        )
        return None


gmaps = get_gmaps_client(API_KEY)


def get_coordinates(address):
    """Converts a text address to latitude and longitude using the Geocoding API."""
    if gmaps is None:
        return None, None

    try:
        # Call Google Maps Geocoding API
        geocode_result = gmaps.geocode(address, components={"country": "se"})

        if geocode_result:
            location = geocode_result[0]["geometry"]["location"]
            lat = location["lat"]
            lon = location["lng"]
            return lat, lon
        else:
            st.error(f"Could not find the address: {address}")
            return None, None

    except Exception:
        st.error("A problem occurred during communication with the Google Maps API.")
        return None, None


def get_distance_km(
    start_lat, start_lon, dest_lat, dest_lon, departure_time=None, arrival_time=None
):
    if gmaps is None:
        return None

    origins = [f"{start_lat},{start_lon}"]
    destinations = [f"{dest_lat},{dest_lon}"]

    # Retrive time parameter dynamically
    time_param = {}
    if departure_time:
        time_param["departure_time"] = departure_time
    elif arrival_time:
        time_param["arrival_time"] = arrival_time

    try:
        matrix_result = gmaps.distance_matrix(
            origins,
            destinations,
            mode="driving",
            units="metric",
            **time_param,  # Pass the time parameter
        )

        distance_meters = matrix_result["rows"][0]["elements"][0]["distance"]["value"]
        distance_km = distance_meters / 1000

        return distance_km

    except HTTPError as e:
        st.error(
            f"Distance Matrix API Error (HTTP 400). Check if the Distance Matrix API is enabled for your key. Error: {e}"
        )
        return None

    except (IndexError, KeyError, TypeError):
        st.error(
            "Could not calculate distance. Check the addresses or if the route is possible."
        )
        return None
