import logging
import requests
import streamlit as st

"""
with st.form(key='create_form'):

    st.subheader("Create New Notification")
    text = st.text_input("Notification Text")  # Text area for user to input the notification
    submit_button = st.form_submit_button(label='Create Notification')

    if submit_button:
        if text:
            result = requests.put(f"http://api:4000/v//creat-notifications/{text}") 
            if result:
                st.success(result.get('message', 'Notification created successfully.'))
            else:
                st.error("Failed to create notification.")
        else:
            st.error("Please fill in the notification text.")
"""

with st.form(key='create_form'):

    st.subheader("Create New Notification")
    text = st.text_input("Notification Text")  # Text area for user to input the notification
    submit_button = st.form_submit_button(label='Create Notification')

    if submit_button:
        response = requests.put(f"http://api:4000/v/create-notifications/{text}")
        st.write(response)
        #st.write(response_message)