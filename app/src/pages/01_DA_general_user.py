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
st.write(f"### Hi, {st.session_state.get('first_name', 'User')}.")

st.write("# General User Data")

data = {}
try:
    # Fetch all users data from the API
    response = requests.get('http://api:4000/d/users')
    response.raise_for_status()  # Check if the request was successful
    data = response.json()
except requests.exceptions.RequestException as e:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    st.write(f"Error: {e}")
    data = {"a": {"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}


st.dataframe(data)

st.write("# Search Specific User Data")

key = st.text_input("Enter the user_id of the user you want to view:")
if key:
    try:
        user_data_response = requests.get(f'http://api:4000/d/users/{key}')
        user_data_response.raise_for_status()
        user_data = user_data_response.json()
        portfolio_data_response = requests.get(f'http://api:4000/d/myportfolios_stock/{key}')
        portfolio_data_response.raise_for_status()
        portfolio_data = portfolio_data_response.json()
        st.dataframe(user_data)
        st.dataframe(portfolio_data)
        if st.button("Ban User"):
            ban_response = requests.put(f'http://api:4000/d/banUser/{key}')
            ban_response.raise_for_status()  # Check if the request was successful
            st.success(f"User {key} has been banned successfully.")
            response = requests.get('http://api:4000/d/users')
            response.raise_for_status()  # Check if the request was successful
            data = response.json()
            st.dataframe(data)
        if st.button("Unban User"):
            unban_response = requests.put(f'http://api:4000/d/unbanUser/{key}')
            unban_response.raise_for_status()  # Check if the request was successful
            st.success(f"User {key} has been unbanned successfully.")
             # Fetch all users data from the API
            response = requests.get('http://api:4000/d/users')
            response.raise_for_status()  # Check if the request was successful
            data = response.json()
            st.dataframe(data)
    except requests.exceptions.RequestException as e:
        st.write("User does not exist or an error occurred.")
        st.write(f"Error: {e}")
