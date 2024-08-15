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
follower_id = 9379
following_id = 1

def fetch_notifications(follower_id):
    try:
        response = requests.get(
            f'http://api:4000/u/notifications/{follower_id}'
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching notifications: {e}")
        return None

# Fetch notifications from the followed user
notifications_data = fetch_notifications(following_id)

if notifications_data:
    if notifications_data:  # Check if the data is not empty
        st.subheader(f"Notifications from User {following_id}")

        for notification in notifications_data:
            st.write(notification['text'])
    else:
        st.write(f"No notifications from user {following_id}.")
else:
    st.error("Failed to fetch notifications.")

