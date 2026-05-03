"""Retriever and vector-store factories for runtime and index-building scripts."""

import os
import re
from dataclasses import dataclass
from pathlib import Path

from qdrant_client.http.models import Distance, VectorParams

from src.rag.config import EMBEDDING_MODEL, QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION_NAME
from src.rag.logger import get_logger

logger = get_logger(__name__)


@dataclass
class KeywordDocument:
    """Minimal document shape used by the lightweight keyword retriever."""

    page_content: str
    metadata: dict


class KeywordRetriever:
    """Simple in-process retriever used when vector stores are unavailable."""

    def __init__(self, documents, *, k=4):
        self.documents = documents
        self.k = k

    def invoke(self, query):
        query_terms = _terms(query)
        scored = []
        for doc in self.documents:
            text = doc.page_content.lower()
            metadata_text = " ".join(str(value) for value in doc.metadata.values()).lower()
            score = 0
            for term in query_terms:
                if term in text:
                    score += 3
                if term in metadata_text:
                    score += 2
                if len(term) > 8 and term in text:
                    score += 8
            if score:
                scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [doc for _, doc in scored[: self.k]]

    def get_relevant_documents(self, query):
        return self.invoke(query)

    def __call__(self, query):
        return self.invoke(query)

def get_embedding_model():
    """Load the configured Hugging Face embedding model."""

    logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
    model_kwargs = {}
    embedding_device = os.environ.get("EMBEDDING_DEVICE")
    if embedding_device:
        model_kwargs["device"] = embedding_device
    from langchain_huggingface import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, model_kwargs=model_kwargs)
    return embeddings


def get_keyword_retriever(paths=None, *, k=4):
    """Build a keyword retriever from Markdown corpus paths.

    Raw ServiceNow task JSON is intentionally ignored here; approved ServiceNow
    content should be prepared to JSONL and loaded through `data_loader.py`.
    """

    raw_paths = paths or os.environ.get(
        "KEYWORD_CORPUS_PATHS",
        "docs/google_sites_guide:docs/slurm-23.02.7/markdown",
    )
    corpus_paths = [Path(item) for item in raw_paths.split(":") if item]
    documents = []
    for corpus_path in corpus_paths:
        if not corpus_path.exists():
            continue
        for path in corpus_path.rglob("*.md"):
            if _is_blocked_path(path):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            documents.extend(_chunk_keyword_document(path, text))
    logger.info("Loaded %s keyword corpus chunks.", len(documents))
    return KeywordRetriever(documents, k=k)


def _chunk_keyword_document(path, text, *, chunk_chars=1400, overlap=200):
    """Split one Markdown file into overlapping keyword-searchable chunks."""

    normalized = "\n".join(line.rstrip() for line in text.splitlines())
    chunks = []
    start = 0
    index = 0
    while start < len(normalized):
        chunk = normalized[start : start + chunk_chars].strip()
        if chunk:
            chunks.append(
                KeywordDocument(
                    page_content=chunk,
                    metadata={
                        "source": str(path),
                        "title": path.stem.replace("-", " ").replace("_", " ").title(),
                        "chunk_id": f"{path}:{index}",
                    },
                )
            )
        index += 1
        start += max(1, chunk_chars - overlap)
    return chunks


def _terms(text):
    stopwords = {
        "what",
        "does",
        "mean",
        "slurm",
        "oarc",
        "amarel",
        "guide",
        "once",
        "ready",
        "command",
    }
    return [
        term
        for term in re.findall(r"[a-z0-9_./-]+", str(text).lower())
        if len(term) > 2 and term not in stopwords
    ]


def _is_blocked_path(path):
    """Prevent raw ServiceNow task JSON from entering keyword retrieval."""

    parts = {part.lower() for part in path.parts}
    return "servicenow" in parts and path.name.startswith("task") and path.suffix == ".json"

def get_vector_store(embeddings, vector_store_type="qdrant", documents=None):
    """Create or connect to the requested vector-store backend."""

    if vector_store_type == "qdrant":
        from langchain_community.vectorstores import Qdrant
        from qdrant_client import QdrantClient

        logger.info(f"Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

        # Get the embedding dimension by embedding a dummy text
        dummy_embedding = embeddings.embed_query("test")
        embedding_dim = len(dummy_embedding)
        logger.info(f"Deduced embedding dimension: {embedding_dim}")

        # Check if the collection exists
        try:
            client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
            logger.info(f"Collection '{QDRANT_COLLECTION_NAME}' already exists.")
        except Exception:
            logger.info(f"Collection '{QDRANT_COLLECTION_NAME}' not found. Creating new collection.")
            client.recreate_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE),
            )
            logger.info(f"Collection '{QDRANT_COLLECTION_NAME}' created successfully.")

        vector_store = Qdrant(
            client=client,
            collection_name=QDRANT_COLLECTION_NAME,
            embeddings=embeddings,
        )
        logger.info(f"Connected to Qdrant collection: {QDRANT_COLLECTION_NAME}")
        return vector_store
    
    elif vector_store_type == "faiss":
        if documents is None:
            raise ValueError("Documents must be provided for in-memory vector store.")
        from langchain_community.vectorstores import FAISS

        logger.info("Creating in-memory FAISS vector store.")
        return FAISS.from_documents(documents, embeddings)

def load_faiss_index(persist_dir, embedding_model):
    """Load a persisted FAISS index and expose it as a retriever."""

    from langchain_community.vectorstores import FAISS

    logger.info(f"Loading FAISS index from '{persist_dir}'...")
    vector_store = FAISS.load_local(persist_dir, embedding_model, allow_dangerous_deserialization=True)
    logger.info("FAISS index loaded successfully.")
    return vector_store.as_retriever()

def add_documents_to_store(vector_store, documents, vector_store_type="qdrant"):
    """Add documents to mutable vector-store backends."""

    if vector_store_type == "qdrant":
        logger.info(f"Adding {len(documents)} documents to the vector store.")
        vector_store.add_documents(documents)
        logger.info("Successfully added documents to the vector store.")
