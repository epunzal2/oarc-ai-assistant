import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_documents, chunk_documents
from src.vector_store import get_embedding_model, get_vector_store, add_documents_to_store
from src.logger import get_logger

logger = get_logger(__name__)

def main():
    """
    Main function to create the vector store.
    """
    logger.info("Starting the vector store creation process...")
    
    # Load and chunk documents
    documents = load_documents()
    chunked_documents = chunk_documents(documents)
    
    # Get embedding model and vector store
    embeddings = get_embedding_model()
    vector_store = get_vector_store(embeddings)
    
    # Add documents to the store
    add_documents_to_store(vector_store, chunked_documents)
    
    logger.info("Vector store creation process completed successfully.")

if __name__ == "__main__":
    main()