"""Corpus loaders shared by index-building and runtime setup code."""

import hashlib
import json
import os
from pathlib import Path
from langchain_core.documents import Document
from src.rag.config import DATA_PATH, SERVICE_NOW_DATA_PATH
from src.rag.logger import get_logger
from src.rag.source_metadata import (
    infer_source_metadata_from_path,
    parse_metadata_sidecar,
    split_front_matter,
    stable_content_hash,
)

logger = get_logger(__name__)


def load_servicenow_documents(servicenow_path=SERVICE_NOW_DATA_PATH):
    """Load prepared ServiceNow JSONL records into LangChain documents."""

    logger.info(f"Loading documents from {servicenow_path}")
    documents = []
    try:
        with open(servicenow_path, 'r') as f:
            for line in f:
                data = json.loads(line)
                document = Document(
                    page_content=data.get("text", ""),
                    metadata=data.get("metadata", {})
                )
                documents.append(document)
        logger.info(f"Loaded {len(documents)} documents from ServiceNow.")
    except FileNotFoundError:
        logger.error(f"ServiceNow data file not found at: {servicenow_path}")
    return documents


def load_documents(servicenow_path=SERVICE_NOW_DATA_PATH):
    """Load configured Markdown corpus and optional prepared ServiceNow records."""

    logger.info(f"Loading documents from {DATA_PATH}")
    markdown_documents = load_markdown_documents(DATA_PATH)
    logger.info(f"Loaded {len(markdown_documents)} documents.")

    servicenow_documents = load_servicenow_documents(servicenow_path)

    documents = markdown_documents + servicenow_documents
    logger.info(f"Loaded a total of {len(documents)} documents.")
    return documents

def chunk_documents(documents):
    """Split loaded documents with the runtime chunking defaults."""

    logger.info("Chunking documents...")
    chunked_documents = []
    for document in documents:
        chunked_documents.extend(_split_document(document, chunk_size=1000, chunk_overlap=200))
    _assign_chunk_metadata(chunked_documents)
    logger.info(f"Created {len(chunked_documents)} document chunks.")
    return chunked_documents


def load_markdown_documents(data_path=DATA_PATH):
    """Load Markdown documents from one or more `os.pathsep`-separated roots."""

    documents = []
    for corpus_path in _iter_data_paths(data_path):
        if not corpus_path.exists():
            logger.warning("Markdown corpus path does not exist: %s", corpus_path)
            continue
        loaded = [
            Document(
                page_content=path.read_text(encoding="utf-8", errors="ignore"),
                metadata={"source": str(path)},
            )
            for path in sorted(corpus_path.rglob("*.md"))
        ]
        documents.extend(_enrich_markdown_documents(loaded))
    return documents


def _iter_data_paths(data_path):
    for raw_path in str(data_path or "").split(os.pathsep):
        if raw_path:
            yield Path(raw_path)


def _enrich_markdown_documents(documents):
    enriched = []
    for document in documents:
        metadata = dict(getattr(document, "metadata", {}) or {})
        source_path = metadata.get("source")
        content = getattr(document, "page_content", "") or ""
        if source_path:
            try:
                raw_content = Path(source_path).read_text(encoding="utf-8")
            except OSError:
                raw_content = content
            front_matter, body = split_front_matter(raw_content)
            sidecar = parse_metadata_sidecar(source_path)
            inferred = infer_source_metadata_from_path(source_path, content=body)
            metadata.update(inferred)
            metadata.update(front_matter)
            metadata.update(sidecar)
            metadata.setdefault("source", str(source_path))
            content = body
        else:
            metadata.update(infer_source_metadata_from_path("", content=content))
        metadata.setdefault("content_hash", stable_content_hash(content))
        enriched.append(Document(page_content=content, metadata=metadata))
    return enriched


def _assign_chunk_metadata(documents):
    counters = {}
    for document in documents:
        metadata = dict(getattr(document, "metadata", {}) or {})
        parent_key = (
            metadata.get("source")
            or metadata.get("document_id")
            or metadata.get("id")
            or metadata.get("source_id")
            or "__unknown__"
        )
        counters[parent_key] = counters.get(parent_key, 0) + 1
        metadata.setdefault("content_hash", stable_content_hash(document.page_content))
        metadata.setdefault("chunk_id", _stable_chunk_id(metadata, parent_key, counters[parent_key]))
        document.metadata = metadata


def _stable_chunk_id(metadata, parent_key, chunk_index):
    source_id = metadata.get("source_id") or "source"
    parent_hash = hashlib.sha256(str(parent_key).encode("utf-8")).hexdigest()[:12]
    return f"{source_id}:{parent_hash}:{chunk_index}"


def _split_document(document, *, chunk_size, chunk_overlap):
    text = getattr(document, "page_content", "") or ""
    metadata = dict(getattr(document, "metadata", {}) or {})
    chunks = []
    start = 0
    step = max(1, chunk_size - chunk_overlap)
    while start < len(text):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(Document(page_content=chunk, metadata=dict(metadata)))
        start += step
    if not chunks and text == "":
        chunks.append(Document(page_content="", metadata=dict(metadata)))
    return chunks

if __name__ == '__main__':
    # This is for testing the data loader
    docs = load_documents()
    chunked_docs = chunk_documents(docs)
    logger.info("Sample chunk:")
    logger.info(chunked_docs[0].page_content)
