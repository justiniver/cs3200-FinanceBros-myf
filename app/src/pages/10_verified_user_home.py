import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Verified Trader, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Portfolio', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_ver_user_portfolio.py')

if st.button('View Verified Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_ver_public_profile.py')

if st.button('Send Notifications to Followers', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/12_send_notifs.py')
if st.button('See Notifications From Following', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/02_verified_user_see_notifications.py')

if st.button('Financial AI Consultant (Verified)', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/98_verified_chatbot.py')