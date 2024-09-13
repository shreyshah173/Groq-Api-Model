import os
import json

import streamlit as st
from groq import Groq

# streamlit page configuration
st.set_page_config(
    page_title="Groq Streamlit Example",
    layout="centered"
)

# Define working directory and load config
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(os.path.join(working_dir, "config.json")))

# Set the Groq API key
groq_api_key = config_data["Groq_API_KEY"]
os.environ["GROQ_API_KEY"] = groq_api_key

# Initialize Groq client
client = Groq()

# Initialize chat history if not already present in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display the title
st.title("Groq Streamlit Example")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for the user's prompt
prompt = st.chat_input("Enter your prompt here")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Send the user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Adjust model name as needed
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
