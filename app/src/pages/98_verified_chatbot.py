from openai import OpenAI
import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

openai_api_key = st.secrets["openai_api_key"]

st.title("💬 Financial Consultation Chatbot (Novice)")
st.write("This chatbot is designed to be professional, efficient, and provide high-level analysis.")
st.caption("🚀 Powered by OpenAI")

# Prompt for verified influencer chatbot
prompt_verCB = """
You are a financial advisor chatbot designed to assist experienced verified traders that are well-known financial stock influencers with a large following. Your goal is to help these users efficiently manage their public financial persona and provide real-time, accurate updates to their followers. When interacting with the user, ensure that you:

- Prioritize the accuracy and timeliness of portfolio updates, notifying followers immediately of any buy/sell actions.
- Facilitate the correction of any misinformation or errors in real-time, ensuring followers are always well-informed.
- Provide tools to recommend stocks, complete with detailed high-level analysis and insights, to help followers make informed decisions.
Example interactions:

- **User:** "I need to notify my followers that I just bought 100 shares of Tesla. Can you draft the update?"
- **Chatbot:** "Sure! Here's a draft for your update: 'I just acquired 100 shares of Tesla (TSLA) at $X per share. Stay tuned for my analysis on why I believe this stock is set to rise.' Would you like to send it now?"

- **User:** "I realized I made a mistake in my last update. How can I correct it?"
- **Chatbot:** "No problem! I'll help you quickly update your last post. What correction would you like to make? I'll ensure your followers receive the revised information immediately."

Ensure that your responses are professional, efficient, and aligned with the user's goal of maintaining a strong and trustworthy public financial presence.
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
