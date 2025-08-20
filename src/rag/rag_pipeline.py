from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.vector_store import get_vector_store, get_embedding_model
from src.llm_provider import get_llm_provider
from src.logger import get_logger

logger = get_logger(__name__)

def create_rag_chain(llm_provider_name="huggingface_api"):
    """
    Creates the RAG chain.
    """
    logger.info(f"Creating RAG chain with LLM provider: {llm_provider_name}...")

    # Get the embedding model and vector store
    embeddings = get_embedding_model()
    vector_store = get_vector_store(embeddings)
    retriever = vector_store.as_retriever()

    # Get the LLM provider
    llm_provider = get_llm_provider(llm_provider_name)
    llm = llm_provider.get_llm()

    # Define the prompt template
    template = """
    Answer the following question based on the provided context.
    If the context does not contain the answer, try your best to answer in a general manner and tell the user to refer to 
    the user guide and contact helpdesk support.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = PromptTemplate.from_template(template)

    # Create the RAG chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    logger.info("RAG chain created successfully.")
    return rag_chain

if __name__ == '__main__':
    # This is for testing the RAG pipeline
    try:
        rag_chain = create_rag_chain()
        logger.info("Successfully created RAG chain.")
        question = "What is the Amarel cluster?"
        logger.info(f"Testing RAG chain with question: {question}")
        answer = rag_chain.invoke(question)
        logger.info(f"Answer: {answer}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")