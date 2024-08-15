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
st.title("Create Notification")

def create_notification(text, user_id):
    try:
        response = requests.post(  # Use POST if creating a new notification
            'http://localhost:4000/v/notifications',  # Adjust URL if needed
            json={'text': text, 'user_id': user_id}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error creating notification: {e}")
        return None
    

# User ID (Example value, replace with actual logged-in user ID)
user_id = 1  # This should be dynamically set based on the logged-in user
notification_id = st.number_input("Notification ID", min_value=1, label="Notification ID")

# Form to create a notification
with st.form(key='create_form'):
    st.subheader("Create New Notification")
    
    text = st.text_area("Notification Text")
    
    submit_button = st.form_submit_button(label='Create Notification')

    if submit_button:
        if text and notification_id:
            result = create_notification(text, user_id)
            if result:
                st.success(result.get('message'))
            else:
                st.error("Failed to create notification.")
        else:
            st.error("Please fill in all fields.")

# Check if there's a message in session state
if 'user_message' in st.session_state:
    # Display the stored message
    st.subheader("Message from the user:")
    st.write(st.session_state['user_message'])
else:
    st.write("No message has been submitted yet.")
