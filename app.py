import streamlit as st
import requests

# Streamlit app title
st.title("Meelko Pellet Assistant Chatbot")

# Input text box for user
user_input = st.text_input("Ask your question:")

# Function to send request to the GPT chatbot API
def get_bot_response(user_query):
    # Replace the following URL with your bot's API endpoint if available
    api_url = "https://chatgpt.com/api/your-bot-endpoint"
    payload = {"input": user_query}
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Replace with your actual API key
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("response", "No response received.")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Display response
if user_input:
    response = get_bot_response(user_input)
    st.write(f"Bot: {response}")
