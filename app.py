import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_data(file):
    bytes_data = file.getvalue()
    # Convert bytes to string
    csv_string = bytes_data.decode('utf-8')
    return csv_string

def process_with_gemini(text, user_prompt):
    """Process the extracted text with Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(f"Answer the following question {user_prompt} given the following data {text}")
    return response.text

def main():
    st.title("Upload a CSV File and Ask Questions")

    # File uploader
    uploaded_file = st.file_uploader("Choose a csv file", type=["csv"])

    if uploaded_file is not None:
        # Extract data
        extracted_text = extract_data(uploaded_file)

        # Get User Prompt
        user_prompt = st.text_input("Enter prompt")

        # Perform OCR
        if st.button("Submit"):
            with st.spinner("Processing"):
                analysis = process_with_gemini(extracted_text, user_prompt)
                st.subheader("Gemini Analysis:")
                st.write(analysis)


if __name__ == "__main__":
    main()