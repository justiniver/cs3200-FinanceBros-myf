import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Data Analyst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Portfolio', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Portfolio_Info_Viz.py')

if st.button('View Verified Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_ver_public_profile.py')

if st.button('Send Notifications to Followers', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/12_send_notifs.py')
if st.button('Dashboard', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/03_my_dashboard.py')