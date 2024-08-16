from openai import OpenAI
import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

# This will only run with viable openAI API key
openai_api_key = st.secrets["openai_api_key"]

st.title("💬 Financial Consultation Chatbot (Analyst)")
st.write("This chatbot is designed for analysts to comprehand complex data")
st.caption("🚀 Powered by OpenAI")

#### Data for chatbot (sarah specific)


####

prompt_daCB = """

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

"""



if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you with your financial queries today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate a response from OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
