"""Retriever and vector-store factories for runtime and index-building scripts."""

import os
import re
import math
from dataclasses import dataclass
from pathlib import Path

from qdrant_client.http.models import Distance, VectorParams

from src.rag.config import EMBEDDING_MODEL, QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION_NAME
from src.rag.logger import get_logger
from src.rag.source_metadata import infer_source_metadata_from_path, stable_content_hash

logger = get_logger(__name__)


@dataclass
class KeywordDocument:
    """Minimal document shape used by the lightweight keyword retriever."""

    page_content: str
    metadata: dict


class KeywordRetriever:
    """Small in-process BM25-style retriever for keyword and hybrid modes."""

    def __init__(self, documents, *, k=4):
        self.documents = documents
        self.k = k
        self._tokenized_docs = [_terms(_document_text(doc)) for doc in documents]
        self._avgdl = (
            sum(len(tokens) for tokens in self._tokenized_docs) / len(self._tokenized_docs)
            if self._tokenized_docs
            else 0.0
        )
        self._idf = self._build_idf(self._tokenized_docs)

    def invoke(self, query):
        query_terms = _terms(query)
        scored = []
        for doc, tokens in zip(self.documents, self._tokenized_docs):
            score = self._bm25_score(query_terms, tokens)
            metadata_text = " ".join(str(value) for value in doc.metadata.values()).lower()
            for term in set(query_terms):
                if term in metadata_text:
                    score += 0.5
                if len(term) > 8 and term in _document_text(doc).lower():
                    score += 1.0
            if score:
                scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [doc for _, doc in scored[: self.k]]

    def get_relevant_documents(self, query):
        return self.invoke(query)

    def __call__(self, query):
        return self.invoke(query)

    @staticmethod
    def _build_idf(tokenized_docs):
        total_docs = len(tokenized_docs)
        document_frequency = {}
        for tokens in tokenized_docs:
            for token in set(tokens):
                document_frequency[token] = document_frequency.get(token, 0) + 1
        return {
            token: math.log(1 + (total_docs - frequency + 0.5) / (frequency + 0.5))
            for token, frequency in document_frequency.items()
        }

    def _bm25_score(self, query_terms, doc_terms) -> float:
        if not query_terms or not doc_terms:
            return 0.0
        k1 = 1.5
        b = 0.75
        doc_len = len(doc_terms)
        term_frequency = {}
        for term in doc_terms:
            term_frequency[term] = term_frequency.get(term, 0) + 1
        score = 0.0
        for term in set(query_terms):
            tf = term_frequency.get(term, 0)
            if tf == 0:
                continue
            idf = self._idf.get(term, 0.0)
            denominator = tf + k1 * (1 - b + b * doc_len / max(self._avgdl, 1.0))
            score += idf * (tf * (k1 + 1)) / denominator
        return score

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
        os.environ.get("DATA_PATH", "docs/google_sites_guide:docs/slurm-23.02.7/markdown"),
    )
    if isinstance(raw_paths, (list, tuple, set)):
        corpus_paths = [Path(item) for item in raw_paths if item]
    else:
        corpus_paths = [Path(item) for item in str(raw_paths).split(":") if item]
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


def get_docstore_keyword_retriever(retriever, *, k=4):
    """Build a keyword retriever from documents already embedded in a vector store."""

    vector_store = getattr(retriever, "vectorstore", None)
    docstore = getattr(vector_store, "docstore", None)
    doc_dict = getattr(docstore, "_dict", None)
    if not isinstance(doc_dict, dict):
        return None
    documents = [
        doc
        for doc in doc_dict.values()
        if hasattr(doc, "page_content") and hasattr(doc, "metadata")
    ]
    if not documents:
        return None
    logger.info("Loaded %s keyword fallback chunks from vector-store docstore.", len(documents))
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
                        "content_hash": stable_content_hash(chunk),
                        **infer_source_metadata_from_path(path, content=chunk),
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

def load_faiss_index(persist_dir, embedding_model, *, k=None):
    """Load a persisted FAISS index and expose it as a retriever."""

    from langchain_community.vectorstores import FAISS

    logger.info(f"Loading FAISS index from '{persist_dir}'...")
    vector_store = FAISS.load_local(persist_dir, embedding_model, allow_dangerous_deserialization=True)
    logger.info("FAISS index loaded successfully.")
    search_kwargs = {"k": k} if k else None
    return vector_store.as_retriever(search_kwargs=search_kwargs) if search_kwargs else vector_store.as_retriever()

def add_documents_to_store(vector_store, documents, vector_store_type="qdrant"):
    """Add documents to mutable vector-store backends."""

    if vector_store_type == "qdrant":
        logger.info(f"Adding {len(documents)} documents to the vector store.")
        vector_store.add_documents(documents)
        logger.info("Successfully added documents to the vector store.")


def _document_text(doc):
    metadata_text = " ".join(str(value) for value in getattr(doc, "metadata", {}).values())
    return f"{getattr(doc, 'page_content', '')} {metadata_text}"
