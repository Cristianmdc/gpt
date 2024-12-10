import streamlit as st
import requests

# Set the base URL for your custom GPT assistant API
BASE_URL = "https://chatgpt.com/g/g-MY83uKdFK-meelko-pellet-assistant/api"  # Replace with actual API endpoint if available

# Title and description
st.title("Meelko Pellet Assistant")
st.subheader("Ask anything about Meelko Pellet!")

# User input
query = st.text_area("Enter your question:")

if st.button("Submit"):
    if query.strip():
        # Call the GPT API
        try:
            response = requests.post(
                f"{BASE_URL}",
                json={"input": query},  # Adjust payload if necessary
                headers={"Authorization": "Bearer YOUR_API_KEY"}  # Replace with your key if needed
            )
            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "No response received.")
                st.success("### Meelko Assistant's Response:")
                st.write(answer)
            else:
                st.error(f"API returned an error: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a question to submit.")

# Footer or additional information
st.caption("Powered by Meelko Pellet Assistant")
