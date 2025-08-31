import sys
import os
import argparse

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.rag.data_loader import load_documents, chunk_documents
from src.rag.vector_store import get_embedding_model, get_vector_store, add_documents_to_store
from src.rag.logger import get_logger

logger = get_logger(__name__)

def main(vector_store_type):
    """
    Main function to create the vector store.
    """
    logger.info("Starting the vector store creation process...")
    
    # Load and chunk documents
    documents = load_documents()
    chunked_documents = chunk_documents(documents)
    
    # Get embedding model
    embeddings = get_embedding_model()
    
    logger.info(f"Creating '{vector_store_type}' vector store...")
    if vector_store_type == "in_memory":
        # For in-memory, we pass documents during creation
        vector_store = get_vector_store(embeddings, vector_store_type=vector_store_type, documents=chunked_documents)
    else:
        # For Qdrant, we create the store and then add documents
        vector_store = get_vector_store(embeddings, vector_store_type=vector_store_type)
        logger.info("Adding documents to the vector store...")
        add_documents_to_store(vector_store, chunked_documents, vector_store_type=vector_store_type)
        
    logger.info(f"Vector store '{vector_store_type}' created and documents added successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a vector store for the RAG system.")
    parser.add_argument(
        "--vector-store",
        type=str,
        choices=["qdrant", "in_memory"],
        default="in_memory",
        help="The vector store to create."
    )
    args = parser.parse_args()
    main(args.vector_store)