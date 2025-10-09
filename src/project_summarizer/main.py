"""
main.py
Streamlit app for uploading documents, generating multi-level summaries,
and performing interactive Q&A on the summarized text using Groq LLM.
"""

import os

import streamlit as st
from langchain_core.documents import Document

from project_summarizer.utils.answer_question import (
    answer_question,
    clear_memory,
    create_qa_chain,
)
from project_summarizer.utils.downloader import extract_text_from_file
from project_summarizer.utils.summarizer import summarize_text

# --- Streamlit UI configuration ---
st.set_page_config(
    page_title="Document Summarizer & Q&A", page_icon="📄", layout="centered"
)

st.title("📄 Document Summarizer & Q&A with Groq LLM")
st.markdown(
    "Upload a PDF, DOCX, TXT, or CSV file, generate a summary, "
    "and ask questions interactively about the content."
)

# --- Verify GROQ API Key ---
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error(
        "Missing GROQ_API_KEY environment variable. "
        "Please set it in Docker or your environment."
    )
    st.stop()

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt", "csv"])

# --- Summary level selection ---
summary_level = st.radio(
    "Choose summary level:",
    options=["brief", "standard", "detailed"],
    index=1,  # Default to "standard"
)

# --- Process uploaded file ---
if uploaded_file:
    st.info("Extracting text from file...")
    text = extract_text_from_file(uploaded_file)

    if text:
        st.success("Text extracted successfully!")

        # --- Generate multi-level summary ---
        with st.spinner("Generating summary..."):
            try:
                summary = summarize_text(text, level=summary_level)
                st.subheader(f"{summary_level.capitalize()} Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"An error occurred while generating the summary: {e}")
                summary = None

        # --- Interactive Q&A ---
        if summary:
            st.subheader("Ask questions about your document")
            user_question = st.text_input("Type your question here:")

            # Initialize the QA chain once
            chain = create_qa_chain()

            if user_question:
                with st.spinner("Generating answer..."):
                    try:
                        answer = answer_question(
                            chain, [Document(page_content=text)], user_question
                        )
                        st.markdown(f"**Answer:** {answer}")
                    except Exception as e:
                        st.error(f"An error occurred while answering the question: {e}")
    else:
        st.warning("No text could be extracted from the uploaded file.")
