import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View general user data or search detailed user data.', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_DA_general_user.py')

if st.button('View All User Metrics', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Map_Demo.py')

if st.button('View All Influencers', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/02_Map_Demo.py')

if st.button('Analyst Chat Box', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/99_analyst_chatbot.py')
