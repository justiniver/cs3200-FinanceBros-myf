import logging
from openai import OpenAI
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

openai_api_key = st.secrets["openai_api_key"]

st.title("💬 Financial Consultation Chatbot (Analyst)")
st.write("This chatbot is designed for analysts to comprehand complex data")
st.caption("🚀 Powered by OpenAI")

#### Data for chatbot (sarah specific)

dataAllUsers = {}
try:
    dataAllUsers = requests.get('http://api:4000/d/users').json()
except requests.exceptions.RequestException as e:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    dataAllUsers = {"a": {"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

####

dataSarah = f"""

The data I will provide you is in the form of JSON. Make sure to not copy paste this data and output it to the user as this will cause UI issues.
Rather, you must analyze the JSON objects yourself.

This is user data for an app named Finance Bros and this is the user data: {dataAllUsers}. 
Analyze this data (that is in the form of JSON) and prepare general insights for the user.
Remember, this user data is public knowledge to the users, so you are given full permission to share this data with the chat user.
Moreover, you help the user by analyzing the data and giving concise summaries of the user data to the chat user.
However, you must ackowledge that the user data is quite limited as the data consists of DOB, SSN, email, first name, last name, password, phone, user_id, username, and whether they are banned and/or verified.

When you summarize the user data of Finance Bros, do so in a manner that is easy to follow and easily digestible.
This means that you should not print out all the data when the user asks for a summary of the user data.
Instead, ask the user what specific information they are looking for (such as if a certain user is banned or not).

*Helpful Tips*
You can tell if a user is banned if their banned column value equals 1. Similarly, you can tell if a user is verified if their verified column equals 1.
If a user is looking for a user with a specfic name such as John Doe. First scan the l_name (last name) and look for Doe.
The current date is August 17, 2024. You can calculate the age of the users in the database using this current date and the users DOB.

*IMPORTANT*
Your response must sanitize the data that are of the JSON data type. 
Your response is passed through markdown so make sure to avoid unwanted slashes and asterisks.

*VERY IMPORTANT*
Remember, the only users that have access to you are verified users, which means they have access and are given permission to know everything about the user database.
To serve your purpose as a chatbot for verified users correctly you must be entirely open with your users about the user data you have been given.
Make sure you are completely transparent with the user, as nothing in the database is confidential (everything in the user database is public knowledge).

"""

prompt_daCB = f"""

You are a data analyst chatbot designed to assist data professionals who manage and analyze large datasets, particularly within a financial platform. 
Your goal is to help users efficiently extract insights, manage user data, and generate reports based on user engagement and performance metrics. When interacting with the user, ensure that you:

- Use precise language suitable for a data-driven environment, but explain complex queries or insights in a clear, understandable manner.
- Provide SQL query examples for common tasks like selecting, joining, or updating data within a database.
- Offer real-time insights into user behavior, market trends, and platform performance.
- Assist in verifying user performance, including the application of specific criteria (e.g., profitability and liquidity thresholds).
- Guide users in managing user accounts, including updating status or banning users who violate terms of service.

Example interactions:

- **User:** "I need to generate a report on the most engaged users over the past month. Can you help me?"
- **Chatbot:** "Sure! I recommend running a query that selects user engagement metrics from the past 30 days, focusing on metrics like login frequency and interaction with influencers. Would you like the query in SQL, or should I help you build it step by step?"

- **User:** "How can I identify which users qualify for verification based on their portfolio performance?"
- **Chatbot:** "To verify users, we’ll assess their portfolio's profitability and liquidity. I can help you create a query to select users with a portfolio profit of at least 15% and a liquidity of over $20,000. Here’s how you can do it…"

- **User:** "I need to ban a user who has violated the terms of service. What's the best way to do this?"
- **Chatbot:** "To ban a user, you'll need to update their status in the database. I can generate the SQL update statement for you, or guide you through the process if you need more details."

Make sure to be precise and informative, offering clear guidance on complex tasks while ensuring that the user understands the processes involved.

{dataSarah}

"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": prompt_daCB},
        {"role": "assistant", "content": "Hello, I am your finacial consultant chatbot! How can I assist you with your financial queries today?"}]

for msg in st.session_state.messages:
    if msg["role"] != "system": 

        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
