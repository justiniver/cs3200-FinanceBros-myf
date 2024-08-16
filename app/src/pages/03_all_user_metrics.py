import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("User Metrics")
st.write("Here are all currently tracked metrics for each user")
data = {} 
try:
  data = requests.get('http://api:4000/d/metrics').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

key = st.text_input("Enter the user_id of the user you want to view:")
if key:
    try:
        user_data_response = requests.get(f'http://api:4000/d/users/{key}')
        user_data_response.raise_for_status()
        user_data = user_data_response.json()
        st.dataframe(user_data)
        
    except requests.exceptions.RequestException as e:
        st.write("User does not exist or an error occurred.")
        st.write(f"Error: {e}")

