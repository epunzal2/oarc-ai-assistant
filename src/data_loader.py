from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import DATA_PATH
from src.logger import get_logger

logger = get_logger(__name__)

def load_documents():
    """
    Loads all .md files from the directory specified in the config.
    """
    logger.info(f"Loading documents from {DATA_PATH}")
    loader = DirectoryLoader(DATA_PATH, glob="**/*.md", show_progress=True)
    documents = loader.load()
    logger.info(f"Loaded {len(documents)} documents.")
    return documents

def chunk_documents(documents):
    """
    Splits the loaded documents into smaller chunks.
    """
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