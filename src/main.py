import sys
import os
import streamlit as st

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag_pipeline import create_rag_chain
from src.logger import get_logger

logger = get_logger(__name__)

# Initialize the RAG chain
try:
    rag_chain = create_rag_chain()
except Exception as e:
    logger.error(f"Failed to create RAG chain: {e}")
    st.error("Failed to initialize the RAG pipeline. Please check the logs for more details.")
    st.stop()

# Streamlit app
st.title("RAG System Chatbot")
st.write("Ask a question about the Amarel cluster and I will try to answer it.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Get the answer from the RAG chain
        with st.spinner("Thinking..."):
            answer = rag_chain.invoke(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        logger.error(f"An error occurred while processing the request: {e}")
        st.error("An error occurred while processing your request. Please try again.")
