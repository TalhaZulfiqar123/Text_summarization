import requests
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Get the API key from the environment variables
API_KEY = os.getenv("mykey")
if not API_KEY:
    st.error("API key not found! Please check your .env file.")

# Define the API URL and headers for the Hugging Face API
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {API_KEY}"}

def query(payload):
    """
    Sends a POST request to the Hugging Face API with the given payload.
    
    Args:
        payload (dict): The data to be sent to the API.
    
    Returns:
        dict: The JSON response from the API if successful, None otherwise.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    
    try:
        response.raise_for_status()  # Raises an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    
    return None

# Create the Streamlit web app
st.title("Text Summarization")
st.write("This is a simple web app to demonstrate text summarization using Hugging Face API.")
st.write("Enter the text you want to summarize:")

# Input text area for the user to enter the text to be summarized
text = st.text_area("Input Text", height=200)

# Sliders to set the minimum and maximum length of the summary
min_length = st.slider("Minimum length of the summary", 0, 150, 30)
max_length = st.slider("Maximum length of the summary", 0, 150, 100)

# Button to trigger the summarization
button = st.button("Summarize")

# Use the query function to get the output when the button is clicked
if button:
    output = query({
        "inputs": text,
        "parameters": {"min_length": min_length, "max_length": max_length},
    })
    
    if output and isinstance(output, list) and len(output) > 0:
        summary_text = output[0].get("summary_text", None)
        if summary_text:
            st.write(summary_text)
        else:
            st.write("No summary text found.")
    else:
        st.write("Failed to generate a summary. Please try again.")


