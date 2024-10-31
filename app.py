import pandas as pd
import streamlit as st
from groq import Groq

# Load your dataset
dataset_path = 'Hydra-Movie-Scrape.csv'  # Use the filename directly
data = pd.read_csv(dataset_path)

# Initialize the Groq client with your API key
client = Groq(api_key="gsk_eZCN0c1hgszzo7TXSdTr")  # Replace with your actual API key

def retrieve_information(query):
    # Simple keyword-based retrieval from the dataset
    results = data[data['Title'].str.contains(query, case=False)]
    if not results.empty:
        return results.iloc[0].to_dict()
    return None

def generate_response(retrieved_info):
    context = f"Title: {retrieved_info['Title']}\nSummary: {retrieved_info['Summary']}\n"
    messages = [{"role": "user", "content": context + "Explain the importance of fast language models."}]
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )
    
    return chat_completion.choices[0].message.content

def rag_application(user_query):
    retrieved_info = retrieve_information(user_query)
    if retrieved_info is not None:
        response = generate_response(retrieved_info)
        return response
    else:
        return "No relevant information found."

# Streamlit UI
st.title("Movie RAG Application")
st.write("Enter a movie title or keyword to get information:")

user_input = st.text_input("Movie Title/Keyword")

if st.button("Get Information"):
    if user_input:
        response = rag_application(user_input)
        st.write("Response:")
        st.write(response)
    else:
        st.warning("Please enter a movie title or keyword.")
