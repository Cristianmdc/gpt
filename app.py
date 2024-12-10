import streamlit as st
import requests

# Streamlit page configuration
st.set_page_config(page_title="GPT Chatbot", page_icon="🤖", layout="wide")

# Chatbot interface
st.title("Chat with Your Custom GPT")

# Define API details
API_URL = "https://chatgpt.com/g/g-MY83uKdFK-meelko-pellet-assistant"  # Replace with your GPT API endpoint
API_KEY = "your_api_key_here"  # Add your API key if required

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
with st.form(key="chat_form"):
    user_message = st.text_input("You:", placeholder="Type your question here...", key="user_input")
    submit = st.form_submit_button("Send")

# Handle user input
if submit and user_message:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Call GPT API
    response = requests.post(
        API_URL,
        json={"messages": st.session_state.messages},
        headers={"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    )

    if response.status_code == 200:
        # Get GPT response
        bot_reply = response.json().get("choices", [])[0].get("message", {}).get("content", "")
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    else:
        bot_reply = "Error: Unable to fetch response from the GPT."

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Assistant:** {message['content']}")
