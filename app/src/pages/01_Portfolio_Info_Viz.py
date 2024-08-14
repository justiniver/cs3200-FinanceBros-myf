import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# My Portfolio")

st.write(f"### Hi, {st.session_state['first_name']}.")

data = {} 
try:
  data = requests.get('http://api:4000/u/myportfolios/9379').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)


st.write(f"### Your Positions:")

data = {} 
try:
  data = requests.get('http://api:4000/u/portfolios_stock/9379').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)
