import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import json

SideBarLinks()

st.write("# Verified Profiles")

st.write(f"### Hi, {st.session_state['first_name']}.")
try:
    response = requests.get('http://api:4000/u/influencers')
    response.raise_for_status()  # Check if the request was successful
    data = response.json()
    usernames = [item["username"] for item in data]
    option = st.selectbox(
        "Select a Influencer:",
        options = ["Select a Influencer..."] + usernames, 
        index = 0,
        placeholder="Select a Influencer..."
    )
    if option: 
        data = requests.get(f'http://api:4000/u/influencers/{option}').json()
        st.dataframe(data)
        follow = st.button("Follow?")
        if follow:
            follow_id = requests.get(f'http://api:4000/u/users/{option}').json()
            user_id_influencer = follow_id[0]['user_id']
            follow_json = requests.post(f'http://api:4000/u/follow/9379/{user_id_influencer}')
            st.write(f"You have followed {option}!")
except Exception as e:
    st.write("Choose an Influencer...")
    #st.write(f"Error: {e}")
    data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}
