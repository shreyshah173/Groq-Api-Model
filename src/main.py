import os
import json
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Groq Streamlit Example",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(os.path.join(working_dir, "config.json")))

groq_api_key = config_data["Groq_API_KEY"]
os.environ["GROQ_API_KEY"] = groq_api_key

client = Groq()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Groq Streamlit Example")

model_options = {
    "Distil-Whisper English": "distil-whisper-large-v3-en",
    "Gemma 2 9B": "gemma2-9b-it",
    "Gemma 7B": "gemma-7b-it",
    "Llama 3 Groq 70B Tool Use (Preview)": "llama3-groq-70b-8192-tool-use-preview",
    "Llama 3 Groq 8B Tool Use (Preview)": "llama3-groq-8b-8192-tool-use-preview",
    "Llama 3.1 70B (Preview)": "llama-3.1-70b-versatile",
    "Llama 3.1 8B (Preview)": "llama-3.1-8b-instant",
    "Llama Guard 3 8B": "llama-guard-3-8b",
    "LLaVA 1.5 7B": "llava-v1.5-7b-4096-preview",
    "Meta Llama 3 70B": "llama3-70b-8192",
    "Meta Llama 3 8B": "llama3-8b-8192",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Whisper": "whisper-large-v3"
}

selected_model = st.selectbox("Select a model", list(model_options.keys()))

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Enter your prompt here")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    model_id = model_options[selected_model]

    response = client.chat.completions.create(
        model=model_id,
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
