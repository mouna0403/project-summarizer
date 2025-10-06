"""
summarizer.py
This module handles LLM-based summarization of document text using Groq's Llama 3.1 model.
"""

import os
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document


def summarize_text(text: str) -> str:
    """Summarize the provided text using a Groq-hosted Llama model."""

    # Initialize the LLM (ensure the API key is set in environment variables)
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Define the summarization prompt
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Write a concise and clear summary of the following text:\n\n{context}")]
    )

    # Create summarization chain
    chain = create_stuff_documents_chain(llm, prompt)

    # Convert text to Document object
    doc = Document(page_content=text)

    # Run summarization
    result = chain.invoke({"context": [doc]})

    return result