# RAG System for OARC Documentation

This project implements a Retrieval-Augmented Generation (RAG) system to answer questions about the Amarel cluster based on the OARC Google Sites guide.

## Architecture

The system is built with Python, LangChain, Qdrant, and a Hugging Face model. For a detailed explanation of the architecture, please see the [`architecture/architecture.md`](./architecture/architecture.md) file.

## Setup and Installation

### 1. Prerequisites

-   Python 3.9+
-   Docker
-   `uv` (can be installed with `pip install uv`)

### 2. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 3. Set Up the Environment

Create a virtual environment and install the required packages:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 4. Set Up the Hugging Face API Token

Create a `.env` file in the root of the project and add your Hugging Face API token:

```
HUGGINGFACE_API_TOKEN="your-token-here"
```

Then, log in to the Hugging Face Hub:

```bash
huggingface-cli login --token $HUGGINGFACE_API_TOKEN
```

### 5. Start the Qdrant Vector Database

Run the Qdrant Docker container:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 6. Create the Vector Store

Run the indexing script to populate the vector store with the document embeddings:

```bash
python -m scripts.create_vector_store
```

## Running the Chatbot

Once the setup is complete, you can run the Streamlit chatbot interface:

```bash
streamlit run src/main.py
```

The app will be available at `http://localhost:8501`.