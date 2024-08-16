import logging
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize logger
logger = logging.getLogger(__name__)

# Set up sidebar links
SideBarLinks()

# Greet the user
st.write(f"### Notifications")


data = {}
try:
    # Fetch all users data from the API
    response = requests.get('http://api:4000/u/notifications/7061')
    response.raise_for_status()  # Check if the request was successful
    data = response.json()
    st.dataframe(data)
except requests.exceptions.RequestException as e:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    st.write(f"Error: {e}")
    data = {"a": {"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

