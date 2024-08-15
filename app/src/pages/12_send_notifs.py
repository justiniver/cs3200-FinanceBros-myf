import logging
import requests
import streamlit as st

# Configure logging
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(layout='wide')

# Title
st.title("Create Notification")

# Hardcoded user ID for the logged-in user
'''
def create_notification(text, user_id):
    try:
        response = requests.post(
            f'http://api:4000/v/create-notifications/{user_id}',  # Include user_id in the URL
            json={'text': text}
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
    user_id = 865
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
'''