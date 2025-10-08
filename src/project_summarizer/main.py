"""
main.py
Streamlit app for uploading files and generating multi-level summaries with Groq LLM.
"""

import os

import streamlit as st

from project_summarizer.utils.downloader import extract_text_from_file
from project_summarizer.utils.summarizer import summarize_text

# --- Streamlit UI configuration ---
st.set_page_config(page_title="Document Summarizer", page_icon="📄", layout="centered")

st.title("📄 Document Summarizer with Groq LLM")
st.markdown(
    "Upload PDF, DOCX, TXT, or CSV and generate multi-level summaries: brief, standard, detailed."
)

# Verify the API key is available (injected via Docker or environment)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error(
        "Missing GROQ_API_KEY environment variable. Please set it in Docker or your environment."
    )
    st.stop()

# File uploader
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt", "csv"])

# Select summary level
summary_level = st.radio(
    "Choose summary level:",
    options=["brief", "standard", "detailed"],
    index=1,  # Default to "standard"
)

if uploaded_file:
    st.info("Extracting text from file...")
    text = extract_text_from_file(uploaded_file)

    if text:
        st.success("Text extracted successfully!")
        st.info(f"Generating {summary_level} summary...")
        with st.spinner("Summarizing..."):
            try:
                summary = summarize_text(text, level=summary_level)
                st.subheader(f"{summary_level.capitalize()} Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"An error occurred while generating the summary: {e}")
    else:
        st.warning("No text could be extracted from the uploaded file.")
