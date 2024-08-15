import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Novice Trader, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View My Portfolio', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_portfolio_info_viz.py')

if st.button('View Verified Profiles', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_verified_profiles.py') 

if st.button('My Dashboard', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_my_dashboard.py')

if st.button('Financial AI Consultant', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/99_consult_chatbox.py') 