"""
main.py
Streamlit app for uploading a PDF and summarizing it with a Groq LLM.
"""

import streamlit as st
import os
from project_summarizer.utils.summarizer import summarize_text
from project_summarizer.utils.downloader import extract_text_from_pdf

# --- Streamlit UI configuration ---
st.set_page_config(page_title="PDF Summarizer", page_icon="📄", layout="centered")

st.title("📄 PDF Summarizer with Groq LLM")

# Verify the API key is available (injected via Docker or environment)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Missing GROQ_API_KEY environment variable. Please set it in Docker or your environment.")
    st.stop()

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.info("Extracting text from PDF...")
    text = extract_text_from_pdf(uploaded_file)

    if text:
        st.success("Text extracted successfully! Generating summary...")
        with st.spinner("Summarizing..."):
            try:
                summary = summarize_text(text)
                st.subheader("Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("No text could be extracted from the PDF.")