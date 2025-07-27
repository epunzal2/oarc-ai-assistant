from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from src.config import EMBEDDING_MODEL, QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION_NAME
from src.logger import get_logger

logger = get_logger(__name__)

def get_embedding_model():
    """
    Returns the embedding model.
    """
    logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings

from qdrant_client.http.models import Distance, VectorParams

def get_vector_store(embeddings):
    """
    Creates or gets the Qdrant vector store.
    """
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

def add_documents_to_store(vector_store, documents):
    """
    Adds documents to the vector store.
    """
    logger.info(f"Adding {len(documents)} documents to the vector store.")
    vector_store.add_documents(documents)
    logger.info("Successfully added documents to the vector store.")
