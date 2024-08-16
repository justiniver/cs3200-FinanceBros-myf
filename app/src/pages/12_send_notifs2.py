import logging
import requests
import streamlit as st

st.subheader("Create New Notification")
text = st.text_input("Notification Text")  # Text area for user to input the notification
if text:
    response = requests.post(f"http://api:4000/v/create-notifications/{text}")
    user_written_notifs = requests.get(f"http://api:4000/v/get_notifications/1962")
    st.dataframe(user_written_notifs) 