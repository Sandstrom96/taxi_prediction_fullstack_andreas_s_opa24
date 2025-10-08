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
