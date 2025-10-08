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
