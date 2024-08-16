import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import json

SideBarLinks()

# st.write(f"### Your written Notifications:")
# notificationTable = requests.get('http://api:4000/v/get_notifications/1964').json()
# st.dataframe(notificationTable)

st.subheader("Create New Notification")
text = st.text_input("Create Notification Text")  # Text area for user to input the notification
if text:
   response = requests.post(f"http://api:4000/v/create-notifications/{text}")
user_written_notifs =  requests.get('http://api:4000/v/get_notifications/1964').json()
st.dataframe(user_written_notifs) 

st.subheader("Delete Notification")
text_id = st.text_input("Enter Notification ID")  # Text area for user to input the notification
if text_id:
    user_delete_notifs = requests.delete(f'http://api:4000/v/delete_notifications/{text_id}').json()
    st.write(user_delete_notifs)
user_written_notifs =  requests.get('http://api:4000/v/get_notifications/1964').json()
st.dataframe(user_written_notifs) 


