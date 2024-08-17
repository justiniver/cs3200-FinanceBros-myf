import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import pandas as pd
import plotly.express as px

SideBarLinks()

st.write("# My Portfolio")

st.write(f"### Hi, {st.session_state['first_name']}.")


data = {} 
try:
  data = requests.get('http://api:4000/u/myportfolios/1964').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)



import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def fetch_data(user_id):
    try:
        response = requests.get(f'http://api:4000/u/portfolios_stock/{user_id}')
        return response.json()
    except requests.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")

# Function to create bar charts with Plotly
def create_barcharts(data):
    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Create separate DataFrames for 'beta' and 'sharePrice'
    beta_df = df[['stockName', 'beta']]
    share_price_df = df[['stockName', 'sharePrice']]
    
    # Create subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Beta Values by Ticker', 'Share Prices by Ticker'))
    
    # Add beta bar chart
    fig.add_trace(go.Bar(x=beta_df['stockName'], y=beta_df['beta'], name='Beta'), row=1, col=1)
    
    # Add share price bar chart
    fig.add_trace(go.Bar(x=share_price_df['stockName'], y=share_price_df['sharePrice'], name='Share Price'), row=1, col=2)
    
    # Update layout
    fig.update_layout(height=400, width=800, showlegend=False)
    
    # Display the charts in Streamlit
    st.plotly_chart(fig)

# Fetch data for user_id 1964
data = fetch_data(1964)

# Check if data is fetched successfully
if data:
    # Display the data as a dataframe
    st.dataframe(data)
    
    # Create bar charts based off the data
    create_barcharts(data)



# #  # #
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
        options = ["Select a ticker..."] + stock_names, 
        index = 0,
        placeholder="Select a ticker...",
    )
    
    if option: 
        response = requests.post(f'http://api:4000/u/addStockToPortfolio/730368/{option}')
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