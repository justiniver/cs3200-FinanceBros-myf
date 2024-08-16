import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("All Verified Users")
st.write("Here are all the current verified users:")

data = {} 
try:
  data = requests.get('http://api:4000/d/influencers').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)


data = {} 
try:
  data = requests.get('http://api:4000/d/influencers').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

key = st.text_input("Enter the user_id of the verified user you want to view:")
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
        if st.button("Verify User"):
            van_response = requests.put(f'http://api:4000/d/verify/{key}')
            van_response.raise_for_status()  # Check if the request was successful
            st.success(f"User {key} has been verified successfully.")
            response = requests.get('http://api:4000/d/users')
            response.raise_for_status()  # Check if the request was successful
            data = response.json()
            st.dataframe(data)
        if st.button("Unverify User"):
            unverify_response = requests.put(f'http://api:4000/d/unverify/{key}')
            unverify_response.raise_for_status()  # Check if the request was successful
            st.success(f"User {key} has been unverified successfully.")
             # Fetch all users data from the API
            response = requests.get('http://api:4000/d/users')
            response.raise_for_status()  # Check if the request was successful
            data = response.json()
            st.dataframe(data)
    except requests.exceptions.RequestException as e:
        st.write("User does not exist or an error occurred.")
        st.write(f"Error: {e}")