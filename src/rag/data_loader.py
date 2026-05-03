"""Corpus loaders shared by index-building and runtime setup code."""

import json
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.rag.config import DATA_PATH, SERVICE_NOW_DATA_PATH
from src.rag.logger import get_logger

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
    loader = DirectoryLoader(DATA_PATH, glob="**/*.md", show_progress=True)
    markdown_documents = loader.load()
    logger.info(f"Loaded {len(markdown_documents)} documents.")

    servicenow_documents = load_servicenow_documents(servicenow_path)

    documents = markdown_documents + servicenow_documents
    logger.info(f"Loaded a total of {len(documents)} documents.")
    return documents

def chunk_documents(documents):
    """Split loaded documents with the runtime chunking defaults."""

    logger.info("Chunking documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunked_documents = text_splitter.split_documents(documents)
    logger.info(f"Created {len(chunked_documents)} document chunks.")
    return chunked_documents

if __name__ == '__main__':
    # This is for testing the data loader
    docs = load_documents()
    chunked_docs = chunk_documents(docs)
    logger.info("Sample chunk:")
    logger.info(chunked_docs[0].page_content)
