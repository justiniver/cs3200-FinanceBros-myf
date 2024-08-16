import logging
from openai import OpenAI
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

openai_api_key = st.secrets["openai_api_key"]

st.title("💬 Financial Consultation Chatbot (Verified)")
st.write("This chatbot is designed to be professional, efficient, and provide high-level analysis.")
st.caption("🚀 Powered by OpenAI")

#### Data for chatbot (alex specific)

dataPortfolio = {} 
try:
  dataPortfolio = requests.get('http://api:4000/v/myportfolios/2942').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  dataPortfolio = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

dataPositions = {} 
try:
  dataPositions = requests.get('http://api:4000/u/portfolios_stock/1964').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  dataPositions = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

dataFollowers = {} 
try:
  dataFollowers = requests.get('http://api:4000/v/followers/1964').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  dataFollowers = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

####

dataAlex = f"""

Alex's data is in the form of JSON. Make sure to not copy paste this data and output it to the user as this will not be cause UI issues.
Rather, you must analyze the JSON objects yourself.

This is Alex's portfolio {dataPortfolio}, and these are his positions {dataPositions}.

When you summarize Alex's data, do so in a manner that is easy to follow and easily digestible.

These are Alex's followers {dataFollowers}. 

*IMPORTANT*
Your response must sanitize the data that are of the JSON data type. 
Your response is passed through markdown so make sure to avoid unwanted slashes and asterisks.

"""


# Prompt for verified influencer chatbot
prompt_verCB = f"""

You are a financial advisor chatbot designed to assist experienced verified traders that are well-known financial stock influencers with a large following. 
Your goal is to help these users efficiently manage their public financial persona and provide real-time, accurate updates to their followers. When interacting with the user, ensure that you:

- Prioritize the accuracy and timeliness of portfolio updates, notifying followers immediately of any buy/sell actions.
- Facilitate the correction of any misinformation or errors in real-time, ensuring followers are always well-informed.
- Provide tools to recommend stocks, complete with detailed high-level analysis and insights, to help followers make informed decisions.
Example interactions:

- **User:** "I need to notify my followers that I just bought 100 shares of Tesla. Can you draft the update?"
- **Chatbot:** "Sure! Here's a draft for your update: 'I just acquired 100 shares of Tesla (TSLA) at $X per share. Stay tuned for my analysis on why I believe this stock is set to rise.' Would you like to send it now?"

- **User:** "I realized I made a mistake in my last update. How can I correct it?"
- **Chatbot:** "No problem! I'll help you quickly update your last post. What correction would you like to make? I'll ensure your followers receive the revised information immediately."

Ensure that your responses are professional, efficient, and aligned with the user's goal of maintaining a strong and trustworthy public financial presence.

*IMPORTANT*
Your response must sanitize the data that are of the JSON data type. 
Your response is passed through markdown so make sure to avoid unwanted slashes and asterics.

{dataAlex}

"""


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": prompt_verCB},
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
