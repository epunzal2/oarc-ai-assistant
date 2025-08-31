# RAG System for OARC Documentation

This project implements a Retrieval-Augmented Generation (RAG) system to answer questions about the Amarel cluster based on the OARC Google Sites guide and ServiceNow data.

## Architecture

The system is built with Python, LangChain, and a Hugging Face model. It supports both Qdrant and an in-memory FAISS vector store. For a detailed explanation of the architecture, please see the [`architecture/architecture.md`](./architecture/architecture.md) file.

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

Run the indexing script to populate the vector store with the document embeddings. Use the `--vector-store` flag to specify whether to use `qdrant` (default) or `in_memory`.

**For Qdrant:**

```bash
python -m scripts.rag.create_vector_store --vector-store qdrant
```

**For In-Memory FAISS:**

```bash
python -m scripts.rag.create_vector_store --vector-store in_memory
```

## Running the Chatbot

Once the setup is complete, you can run the Streamlit chatbot interface. The script now accepts command-line arguments to select the LLM provider and the vector store.

-   `--llm-provider`: Choose between `huggingface` (default) and `ollama`.
-   `--vector-store`: Choose between `qdrant` (default) and `in_memory`.

**Examples:**

**Using Hugging Face and Qdrant (default):**
```bash
streamlit run src/rag/main.py
```

**Using Ollama and Qdrant:**
```bash
streamlit run src/rag/main.py -- --llm-provider ollama
```

**Using Hugging Face and In-Memory FAISS:**
```bash
streamlit run src/rag/main.py -- --vector-store in_memory
```

**Using Ollama and In-Memory FAISS:**
```bash
streamlit run src/rag/main.py -- --llm-provider ollama --vector-store in_memory
```

The app will be available at `http://localhost:8501`.

## Deployment

### Deployment on an HPC Cluster

To deploy the chatbot on an HPC cluster, you can use the provided `sbatch` script. This script sets up the necessary environment, including loading the required modules and activating the virtual environment, and then runs the chatbot application.

**To submit the job, run the following command:**
```bash
sbatch scripts/deployment/hpc/run_chat_hpc.sbatch
```

This will submit the job to the Slurm scheduler, and the chatbot will be accessible through the compute node where the job is running.