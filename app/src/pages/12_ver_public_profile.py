import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("Welcome to your profile Alex!")
st.write("Here's your followers:")
data = {} 
try:
  data = requests.get('http://api:4000/v/followers/1964').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)
st.write("Here's your public profile!")
profile = requests.get('http://api:4000/v/public_profile/1964').json()
st.dataframe(profile)

option = st.selectbox(
      "What would you like to change in your profile?",
      ("Choose an Option...", "Biography", "Profile Photo", "Username"),
      placeholder="Choose an Option...",
  )

if option == "Biography":
  message = st.text_input("What do you want to change your bio to?")
  if message:
    bio = requests.put(f'http://api:4000/v/update-bio/1964/{message}').json()
    response_message = bio['message']
    st.write(response_message)
    profile = requests.get('http://api:4000/v/public_profile/1964').json()
    st.dataframe(profile) 

if option == "Username":
  message = st.text_input("What do you want to change your username to?")
  if message:
    username = requests.put(f'http://api:4000/v/update-username/1964/{message}').json()
    response_message = username['message']
    st.write(response_message)
    profile = requests.get('http://api:4000/v/public_profile/1964').json()
    st.dataframe(profile) 
    
if option == "Profile Photo":
  message = st.text_input("Please upload photo URL")
  if message:
    photo = requests.put(f'http://api:4000/v/update-photo/1964/{message}').json()
    response_message = photo['message']
    st.write(response_message)
    profile = requests.get('http://api:4000/v/public_profile/1964').json()
    st.dataframe(profile) 
