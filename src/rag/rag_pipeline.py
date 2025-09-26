from typing import Optional, Dict, Any
import os

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

try:
    import tiktoken  # type: ignore
    _ENCODING = tiktoken.get_encoding("cl100k_base")
except Exception:  # pragma: no cover - optional dependency
    _ENCODING = None

from src.rag.vector_store import get_vector_store, get_embedding_model
from src.rag.llm_provider import get_llm_provider
from src.rag.logger import get_logger

logger = get_logger(__name__)

def create_rag_chain(
    llm_provider_name: str = "huggingface_api",
    vector_store_type: str = "qdrant",
    retriever=None,
    llm=None,
    llm_provider_kwargs: Optional[Dict[str, Any]] = None,
    max_context_chars: Optional[int] = None,
):
    """
    Creates the RAG chain.
    """
    logger.info(f"Creating RAG chain with LLM provider: {llm_provider_name} and vector store: {vector_store_type}...")

    # Get the embedding model and vector store
    if retriever is None:
        logger.info("No retriever provided, creating a new one...")
        embeddings = get_embedding_model()
        vector_store = get_vector_store(embeddings, vector_store_type=vector_store_type)
        retriever = vector_store.as_retriever()
    else:
        logger.info("Using the provided retriever.")

    # Get the LLM provider unless an explicit LLM instance was supplied
    if llm is None:
        kwargs = llm_provider_kwargs or {}
        llm_provider = get_llm_provider(llm_provider_name, **kwargs)
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
    # Determine caps from environment; tokens take precedence over characters
    # RAG_MAX_CONTEXT_TOKENS: hard limit on context tokens (preferred)
    # RAG_MAX_CONTEXT_CHARS: fallback character cap
    env_tokens = os.environ.get("RAG_MAX_CONTEXT_TOKENS")
    try:
        max_context_tokens = int(env_tokens) if env_tokens else None
    except Exception:
        max_context_tokens = None

    if max_context_chars is None:
        env_cap = os.environ.get("RAG_MAX_CONTEXT_CHARS")
        try:
            max_context_chars = int(env_cap) if env_cap else 12000
        except Exception:
            max_context_chars = 12000

    def _join_trim_by_tokens(docs, token_limit: int) -> str:
        if token_limit <= 0:
            return ""
        if _ENCODING is None:
            # Fallback: conservative char approximation (3 chars/token)
            approx_chars = max(512, token_limit * 3)
            text = "\n\n".join(doc.page_content for doc in docs)
            return text[:approx_chars]
        toks_accum = []
        used = 0
        for doc in docs:
            toks = _ENCODING.encode(doc.page_content)
            if used + len(toks) <= token_limit:
                toks_accum.extend(toks)
                used += len(toks)
            else:
                remaining = max(0, token_limit - used)
                if remaining > 0:
                    toks_accum.extend(toks[:remaining])
                break
        return _ENCODING.decode(toks_accum)

    def format_docs(docs):
        if max_context_tokens:
            return _join_trim_by_tokens(docs, max_context_tokens)
        text = "\n\n".join(doc.page_content for doc in docs)
        if max_context_chars and len(text) > max_context_chars:
            return text[: max_context_chars]
        return text

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | RunnablePassthrough.assign(
            answer=(
                RunnablePassthrough.assign(
                    context=(lambda x: format_docs(x["context"]))
                )
                | prompt
                | llm
                | StrOutputParser()
            )
        )
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
