import streamlit as st
import pandas as pd
import numpy as np
import json
import base64
import ast
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from typing import List

# Initialize OpenAI client
client = OpenAI()

GPT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-large"

# Functions for Embedding and Cosine Similarity
@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(10))
def get_embeddings(input: List):
    response = client.embeddings.create(
        input=input,
        model=EMBEDDING_MODEL
    ).data
    return [data.embedding for data in response]

def cosine_similarity_manual(vec1, vec2):
    vec1, vec2 = np.array(vec1, dtype=float), np.array(vec2, dtype=float)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# App layout and setup
st.title("Clothing Matchmaker App")
st.write("Upload an image of a clothing item to find complementary matches!")

uploaded_file = st.file_uploader("Choose a clothing image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    def encode_image_to_base64(image):
        return base64.b64encode(image.read()).decode('utf-8')

    encoded_image = encode_image_to_base64(uploaded_file)
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    
    subcategories = ["Shirts", "Pants", "Jackets", "Dresses", "T-shirts", "Shoes", "Accessories"]

    def analyze_image(image_base64, subcategories):
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "user", "content": f"Analyze this image and classify using {subcategories}"}
            ],
        )
        return json.loads(response.choices[0].message.content)

    # Process image and display results
    analysis = analyze_image(encoded_image, subcategories)
    st.write("Analysis Results:", analysis)

    # Fetch dataset and filter matches
    @st.cache
    def load_dataset():
        df = pd.read_csv('sample_styles_with_embeddings.csv')
        df['embeddings'] = df['embeddings'].apply(lambda x: ast.literal_eval(x))
        return df
    
    styles_df = load_dataset()
    item_descs, item_category, item_gender = analysis['items'], analysis['category'], analysis['gender']
    filtered_items = styles_df[styles_df['gender'].isin([item_gender, 'Unisex'])]
    filtered_items = filtered_items[filtered_items['articleType'] != item_category]

    # Match items
    def find_similar_items(input_embedding, embeddings, threshold=0.5, top_k=3):
        similarities = [(i, cosine_similarity_manual(input_embedding, vec)) for i, vec in enumerate(embeddings)]
        filtered_similarities = [(i, sim) for i, sim in similarities if sim >= threshold]
        return sorted(filtered_similarities, key=lambda x: x[1], reverse=True)[:top_k]

    for desc in item_descs:
        input_embedding = get_embeddings([desc])[0]
        matches = find_similar_items(input_embedding, filtered_items['embeddings'].tolist(), 0.6)
        st.write(f"Matches for {desc}:")
        for index, _ in matches:
            matched_item = filtered_items.iloc[index]
            st.image(f"sample_images/{matched_item['id']}.jpg")

