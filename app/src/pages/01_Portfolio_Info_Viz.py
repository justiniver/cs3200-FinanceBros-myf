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


st.write(f"### Select Stock by TICKER:")

# data = {}
# try:
#     response = requests.get('http://api:4000/u/getTicker')
#     response.raise_for_status()  # Check if the request was successful
#     data = response.json()
#     stock_names = [item["ticker"] for item in data]
#     option = st.selectbox(
#         "Select a stock by ticker:",
#         stock_names,
#         index=0,  
#         placeholder="Select a ticker...",
#     )
#     if option: 
#       response = response.post('http://api:4000/u/addStockToPortfolio/9379/{option}')
#     st.write("You added:", option)
# except:
#   st.write("**Important**: Could not connect to sample api, so using dummy data.")
#   data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

# st.write(f"### All Stocks:")

data = {}
try:
    # Fetch the available tickers from the API
    response = requests.get('http://api:4000/u/getTicker')
    response.raise_for_status()  # Check if the request was successful
    data = response.json()

    # Extract stock tickers for the dropdown
    stock_names = [item["ticker"] for item in data]

    # Display selectbox with stock tickers
    option = st.selectbox(
        "Select a stock by ticker:",
        stock_names,
        index=0,  
        placeholder="Select a ticker...",
    )

    # Fetch the user's current portfolio to check for duplicates
    portfolio_response = requests.get('http://api:4000/u/getUserPortfolio/9379')
    portfolio_response.raise_for_status()  # Ensure the GET request was successful
    portfolio_data = portfolio_response.json()

    # Extract tickers already in the portfolio
    portfolio_tickers = [item["ticker"] for item in portfolio_data]

    if option in portfolio_tickers:
        st.warning(f"The stock {option} is already in your portfolio.")
    else:
        if option:
            # Format the URL with the selected ticker
            add_stock_url = f'http://api:4000/u/addStockToPortfolio/9379/{option}'
            
            # Send the POST request to add the stock to the portfolio
            add_stock_response = requests.post(add_stock_url)
            add_stock_response.raise_for_status()  # Ensure the POST request was successful
            
            st.success(f"You added: {option}")

            # Refresh the app to update the list of stocks in real-time
            st.experimental_rerun()

except requests.exceptions.RequestException as e:
    st.write("**Important**: Could not connect to the sample API, so using dummy data.")
    st.write(f"Error details: {e}")
    data = {"a": {"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}
    
    # Display dummy data if API connection fails
    st.write("### All Stocks:")
    st.write(data)