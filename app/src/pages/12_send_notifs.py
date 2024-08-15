import logging
import requests
import streamlit as st

# Configure logging
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(layout='wide')

# Title
st.title("Create Notification")

user_id = 1964  # Hardcoded user ID

# Function to create a notification
def create_notification(text, user_id):
    try:
        # Make a POST request to the correct route
        response = requests.post(
            'http://api:4000/v/notifications',  # Correct route URL
            json={'text': text, 'user_id': user_id}  # Pass user_id in the JSON payload
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error creating notification: {e}")
        return None

# Form to create a notification
with st.form(key='create_form'):
    st.subheader("Create New Notification")
    text = st.text_area("Notification Text")  # Text area for user to input the notification
    submit_button = st.form_submit_button(label='Create Notification')

    if submit_button:
        if text:
            result = create_notification(text, user_id)
            if result:
                st.success(result.get('message', 'Notification created successfully.'))
            else:
                st.error("Failed to create notification.")
        else:
            st.error("Please fill in the notification text.")
