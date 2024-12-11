import streamlit as st
from PyPDF2 import PdfReader
from openai.embeddings_utils import get_embedding
import openai
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Streamlit app title
st.title("Clothing Matchmaker Chatbot")

# Load OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Read the PDF
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    st.write("PDF content loaded successfully!")
    
    # Process and embed content
    st.write("Generating embeddings for the document...")
    doc_embeddings = []
    chunk_size = 200
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        embedding = get_embedding(chunk, model="text-embedding-ada-002")
        doc_embeddings.append(embedding)
    st.write("Embeddings generated.")

    # Chatbot interaction
    def answer_query(query, doc_embeddings, doc_text):
        query_embedding = get_embedding(query, model="text-embedding-ada-002")
        similarities = cosine_similarity([query_embedding], doc_embeddings).flatten()
        best_idx = np.argmax(similarities)
        return doc_text[best_idx]

    query = st.text_input("Enter your question about the PDF content:")
    if query:
        response = answer_query(query, doc_embeddings, text)
        st.write(f"Answer: {response}")

else:
    st.write("Please upload a PDF file to begin.")
