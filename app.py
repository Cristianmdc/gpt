import streamlit as st
from PyPDF2 import PdfReader
import openai
import os

# Title of the application
st.title("LLM Chat App Using PDF Data")

# Load OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to extract text from uploaded PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("PDF uploaded and content extracted!")

    # Display chat messages from history
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if user_input := st.chat_input("Ask a question based on the PDF content:"):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Generate response using OpenAI
        with st.chat_message("assistant"):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Use the following PDF content to answer the user's questions: " + pdf_text},
                    *st.session_state["messages"]
                ]
            )
            reply = response["choices"][0]["message"]["content"]
            st.markdown(reply)
            st.session_state["messages"].append({"role": "assistant", "content": reply})
