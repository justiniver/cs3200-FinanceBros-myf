import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write(f"### Hi, {st.session_state['first_name']}.")

st.write("# General User Data")

data = {} 
try:
  data = requests.get('http://api:4000/d/users').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)


st.write("# Search Specfic User Data")

data = {} 
key = st.text_input("What is the user_id of the user you want to view?")
if key:
  data = requests.get(f'http://api:4000/d/users/{key}').json()
  data2 = requests.get(f'http://api:4000/d/portfolios_stock/{key}').json()
  st.dataframe(data)
  st.dataframe(data2)

