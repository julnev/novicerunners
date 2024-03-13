import openai
import streamlit as st
from guide import get_content
from datetime import datetime
import ssl

# Disable SSL certificate verification (not recommended for production)
ssl._create_default_https_context = ssl._create_unverified_context

# Configure Streamlit
st.set_page_config(
    page_title="Novice Runners Ideation stories",
    page_icon=":memo:",
)

st.title("Create stories for ideation")
"Just give me a brief of your idea and I will write a story to summarize the concept"

# Configure OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]
#private_key_id = st.secrets["private_key_id"]
#private_key = st.secrets["private_key"]

content = get_content()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": content}
    ]

# Display existing conversation history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
if prompt := st.chat_input("Hello, tell me more about your idea"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
