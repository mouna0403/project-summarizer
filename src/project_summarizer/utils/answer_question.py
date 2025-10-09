"""
qa.py
Interactive Q&A over summarized documents using Groq LLM with conversation memory.
"""

import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ConversationBufferMemory
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def create_qa_chain():
    """
    Initialize the Groq LLM for Q&A with conversation memory.
    Returns a chain that can be called with documents and a question.
    """
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

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
                "Context:\n{context}",
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{question}"),
        ]
    )

    chain = create_stuff_documents_chain(llm, prompt)
    return chain


def answer_question(chain, documents, question):
    """
    Ask a question based on a list of Document objects with conversation memory.

    Args:
        chain: QA chain object
        documents: List of langchain Document objects or strings
        question: str, user question
    Returns:
        str: Answer text
    """
    # Convert string documents to Document objects if necessary
    docs = [
        Document(page_content=doc) if isinstance(doc, str) else doc for doc in documents
    ]

    # Load conversation history from memory
    chat_history = memory.load_memory_variables({})["chat_history"]

    # Invoke the chain with documents, question, and conversation history
    result = chain.invoke(
        {"context": docs, "question": question, "chat_history": chat_history}
    )

    # Save the question and answer to memory for future context
    memory.save_context({"input": question}, {"output": result})

    return result


def clear_memory():
    """
    Clear the conversation memory.
    """
    memory.clear()
