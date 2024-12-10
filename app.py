import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_URL = "https://chatgpt.com/api/your-model-endpoint"  # Replace with your model's API endpoint
API_KEY = os.getenv("API_KEY")  # Store the API key securely

def get_bot_response(prompt):
    """Send a prompt to the GPT API and get a response."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"prompt": prompt}
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.json().get("response", "Error: No response from the model.")

# Streamlit UI
st.title("Meelko Pellet Chatbot")
st.write("Interact with the Meelko Pellet Assistant!")

user_input = st.text_input("Ask a question:")
if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            bot_response = get_bot_response(user_input)
        st.success("Bot Response:")
        st.write(bot_response)
    else:
        st.warning("Please enter a question.")
