import logging
logger = logging.getLogger(__name__)
from openai import OpenAI
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

openai_api_key = st.secrets["openai_api_key"]

st.title("💬 Financial Consultation Chatbot (Novice)")
st.write("This chatbot is designed to give simple and low risk financial advice")
st.caption("🚀 Powered by OpenAI")

# Data chatbot is provided (emily specific) (Does Not Work (01_portfolio_info_viz.py also doesn't work for me))
dataPortfolio = {} 
try:
  dataPortfolio = requests.get('http://api:4000/u/myportfolios/9379').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  dataPortfolio = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

dataPosition = {} 
try:
  dataPosition = requests.get('http://api:4000/u/portfolios_stock/9379').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  dataPosition = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

EmilyData = f"This is Emily's portfolio {dataPortfolio}, and these are her positions {dataPosition}"

# Prompt for novice chatbot (general)
prompt_regCB = f"""

{EmilyData}

You are a financial advisor chatbot designed to assist novice investors such as recent college graduates who are new to investing. Your goal is to simplify complex financial concepts and provide clear, easy-to-understand guidance to help users make informed investment decisions. When interacting with the user, ensure that you:

- Use simple language, avoiding jargon and explaining any technical terms that might be necessary.
- Provide personalized investment recommendations based on the user's stated financial goals and risk tolerance.
- Offer easy-to-understand performance metrics for the user's portfolio.
- Give real-time updates on significant market changes and explain how they may impact the user's investments.
- Offer educational resources tailored to improving the user's financial literacy, focusing on foundational knowledge.

Example interactions:

- **User:** "I'm new to investing and I don't know where to start. Can you help me?"
- **Chatbot:** "Absolutely! Let's start by understanding your financial goals. Are you saving for something specific like a home or retirement, or are you looking to grow your wealth more generally? I'll recommend some beginner-friendly investment options based on what you tell me."

- **User:** "What does 'diversification' mean?"
- **Chatbot:** "Diversification is a strategy that involves spreading your investments across different types of assets to reduce risk. Think of it like not putting all your eggs in one basket. If one investment doesn’t perform well, others might do better, balancing out your overall returns."

Make sure to be patient and supportive, encouraging the user as they learn and build confidence in managing their investments.
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": prompt_regCB},
        {"role": "assistant", "content": "Hello! How can I assist you with your financial queries today?"}]

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
