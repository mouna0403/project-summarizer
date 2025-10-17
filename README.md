# Summarizer Project

This project is a Streamlit web app that allows you to upload PDF, Word, TXT, or CSV files and generate summaries using the Groq Llama 3.1 model. Users can also interactively ask questions about the summarized content.

## Features

- Upload PDF, Word (DOCX), Text (TXT), or CSV documents via a simple web interface.
- Automatically extract text from uploaded files — including OCR for scanned PDFs.
- Generate **multi-level summaries**: brief, standard, or detailed.
- Ask questions interactively about the summarized document using a Groq-hosted LLM.
- Dockerized for easy deployment.

## Requirements

- **Docker** installed on your system.
- A **Groq API key** — sign up at [https://groq.com](https://groq.com) to obtain it.
- `.env` file with your API key.

### Example `.env` file

```env
GROQ_API_KEY=your_groq_api_key_here
```

⚠️ **Never commit your .env file to GitHub.**

## How to Run

### 1. Stop any running container

If a previous container is still running, stop it with Ctrl+C in the terminal, or:

```bash
docker ps
docker stop <CONTAINER_ID>
```

### 2. Build the Docker image

From the project root:

```bash
docker build -t summarizer-app .
```

### 3. Run the container

```bash
docker run -p 8501:8501 --env-file .env summarizer-app
```

This will start the Streamlit app on http://localhost:8501.

Make sure your .env file contains a valid Groq API key.

## How to Use

1. Upload a document (PDF, DOCX, TXT, CSV).
2. Select the summary level: brief, standard, or detailed.
3. View the generated summary.
4. Ask questions interactively about the content — the answers are based solely on the summarized text.
5. The Q&A system automatically replies in the same language as the question.

                          # Groq API key (not committed)
├── Dockerfile                         # Docker image build instructions
└── README.md                          # This file
```
