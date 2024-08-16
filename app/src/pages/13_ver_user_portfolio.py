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
  data = requests.get('http://api:4000/u/myportfolios/2942').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)


st.write(f"### Your Positions:")

data = {} 
try:
  data = requests.get('http://api:4000/u/portfolios_stock/1964').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)


data = {}
try:
    response = requests.get('http://api:4000/u/getTicker')
    response.raise_for_status()  # Check if the request was successful
    data = response.json()
    stock_names = [item["ticker"] for item in data]
    option = st.selectbox(
        "Select a stock by ticker:",
        (stock_names),
        index=0,  
        placeholder="Select a ticker...",
    )
    
    if option: 
        response = requests.post(f'http://api:4000/u/addStockToPortfolio/596999/{option}')
        if response.status_code == 200:
            st.write(f"You added: {option}")
        else:
            st.write("Error adding stock to portfolio; Stock is already in your profile.")
except Exception as e:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    st.write(f"Error: {e}")
    data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}


st.write(f"### Top 5 Recommended Stocks for lowest risk level:")

data = {} 
try:
    data = requests.get('http://api:4000/u/recStocks').json()
except:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)

st.write(f"### All Stocks:")

data = {} 
try:
    data = requests.get('http://api:4000/u/stocks').json()
except:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)