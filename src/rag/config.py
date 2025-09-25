import os
from dotenv import load_dotenv

load_dotenv()

"""Centralized configuration with env-first overrides.

These values provide convenient defaults for local runs while allowing Slurm
jobs and other environments to override via exported environment variables.
"""

# Path to the directory containing the markdown files
DATA_PATH = os.environ.get("DATA_PATH", "docs/google_sites_guide/")
SERVICE_NOW_DATA_PATH = os.environ.get(
    "SERVICE_NOW_DATA_PATH", "docs/servicenow/task_prepared.jsonl"
)

# Embedding model to use
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Qdrant configuration
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = os.environ.get("QDRANT_PORT", 6333)
QDRANT_COLLECTION_NAME = os.environ.get("QDRANT_COLLECTION_NAME", "rag_system_collection")

# Hugging Face API configuration
HF_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")

# RAG and Llama.cpp server configuration
LLAMA_CPP_MODEL_PATH = os.environ.get(
    "LLAMA_CPP_MODEL_PATH", "models/Phi-3-mini-4k-instruct-q4.gguf"
)
FAISS_INDEX_PATH = os.environ.get("FAISS_INDEX_PATH", "vector_index/faiss_amarel")
