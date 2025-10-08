"""
qa.py
Interactive Q&A over summarized documents using Groq LLM.
"""

import os

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


def create_qa_chain():
    """
    Initialize the Groq LLM for Q&A.
    Returns a function that can be called with a list of Documents and a question.
    """
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

    # Standard Q&A prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user question based on the provided context:\n\n{context}",
            )
        ]
    )

    # Load a basic QA chain
    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
    return chain


def answer_question(chain, documents, question):
    """
    Ask a question based on a list of Document objects.

    Args:
        chain: QA chain object
        documents: List of langchain Document objects
        question: str, user question
    Returns:
        str: Answer text
    """
    # Ensure documents are Document objects
    docs = [
        Document(page_content=doc) if isinstance(doc, str) else doc for doc in documents
    ]

    result = chain.run(input_documents=docs, question=question)
    return result
