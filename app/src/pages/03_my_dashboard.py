import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

# Configure logging
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged-in user
SideBarLinks()

# Title
st.title("Notifications from Followed User")

# Hardcoded follower user ID and followed user ID
user_id = 9379
follower_id = 9379
following_id = 1

# dashboard notifications



# Dashboard statistics part

