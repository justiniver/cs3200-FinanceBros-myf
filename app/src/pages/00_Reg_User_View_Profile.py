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
key = st.text_input("Whats the username of the profile you want to view?")
influencers = requests.get('http://api:4000/u/influencers').json()
st.dataframe(influencers)

data = {} 
if key:
    data = requests.get(f'http://api:4000/u/influencers/{key}').json()
    st.dataframe(data)
    follow = st.button("Follow?")
    if follow:
        follow_id = requests.get(f'http://api:4000/u/users/{key}').json()
        user_id_influencer = follow_id[0]['user_id']
        # 7061 should be emilys user id
        follow_json = requests.post(f'http://api:4000/u/follow/7061/{user_id_influencer}')
        st.write(f"You have followed {key}!")
