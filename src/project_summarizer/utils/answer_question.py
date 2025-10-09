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

    # English prompt, with instructions to reply in the same language as the question
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a precise and factual assistant. "
                "Answer the user's question *only* using the information from the provided context below. "
                "Do not include any information that is not present in the context. "
                "If the answer cannot be found, respond exactly with: "
                "'I cannot find this information in the provided document.'\n\n"
                "Respond in the **same language** as the user's question.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}",
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
