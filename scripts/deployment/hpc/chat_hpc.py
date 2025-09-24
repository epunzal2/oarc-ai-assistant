import argparse
import socket
from flask import Flask, render_template_string, request, jsonify

from src.rag.vector_store import load_faiss_index, get_embedding_model
from src.rag.rag_pipeline import create_rag_chain
from src.rag.logger import get_logger
from src.rag import config

logger = get_logger(__name__)

def start_cli_chat(chain):
    """
    Starts an interactive command-line chat session.
    """
    print("Starting CLI chat with Phi-3. Type 'exit' or 'quit' to end.")

    while True:
        try:
            prompt = input("You: ")
            if prompt.lower() in ["exit", "quit"]:
                break

            response = chain.invoke(prompt)
            print(f"Assistant: {response.strip()}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    print("\nChat ended.")

def start_web_chat(chain, host: str = "0.0.0.0", port: int = 8088):
    """
    Starts a web-based chat interface using Flask.
    """
    app = Flask(__name__)

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat with Phi-3</title>
        <style>
            body { font-family: sans-serif; }
            #chatbox { width: 80%; height: 400px; border: 1px solid #ccc; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
            #userInput { width: 70%; padding: 10px; }
            #sendButton { padding: 10px; }
        </style>
    </head>
    <body>
        <h1>Chat with Phi-3</h1>
        <div id="chatbox"></div>
        <input type="text" id="userInput" placeholder="Type your message...">
        <button id="sendButton">Send</button>

        <script>
            const chatbox = document.getElementById('chatbox');
            const userInput = document.getElementById('userInput');
            const sendButton = document.getElementById('sendButton');

            async function sendMessage() {
                const message = userInput.value;
                if (!message) return;

                chatbox.innerHTML += `<div><b>You:</b> ${message}</div>`;
                userInput.value = '';

                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                chatbox.innerHTML += `<div><b>Assistant:</b> ${data.response}</div>`;
                chatbox.scrollTop = chatbox.scrollHeight;
            }

            sendButton.addEventListener('click', sendMessage);
            userInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """

    @app.route("/")
    def home():
        return render_template_string(HTML_TEMPLATE)

    @app.route("/chat", methods=["POST"])
    def chat():
        user_message = request.json["message"]
        bot_response = chain.invoke(user_message)
        return jsonify({"response": bot_response.strip()})

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    node = socket.getfqdn() or "localhost"
    print(f"Starting web server at http://{host}:{port} (node: {node})", flush=True)
    app.run(host=host, port=port, debug=False)

def main():
    parser = argparse.ArgumentParser(description="Chat with a local Llama model using RAG.")
    parser.add_argument("--vector-store", type=str, default="faiss", help="The vector store to use.")
    parser.add_argument("--faiss-dir", type=str, default="vector_index/faiss_amarel", help="Path to the saved FAISS index.")
    parser.add_argument("--k", type=int, default=5, help="The number of documents to retrieve.")
    parser.add_argument("--web", action="store_true", help="Start the web-based chat interface.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the web server to.")
    parser.add_argument("--port", type=int, default=8088, help="Port to bind the web server to.")
    args = parser.parse_args()

    logger.info("Starting chat with the following configuration:")
    logger.info(f"  Model path: {config.LLAMA_CPP_MODEL_PATH}")
    logger.info(f"  Embedding model name: {config.EMBEDDING_MODEL}")
    logger.info(f"  FAISS index path: {args.faiss_dir}")
    logger.info(f"  k: {args.k}")
    logger.info(f"  Maximum context length: 2048")

    if args.web:
        logger.info(f"  Web bind: http://{args.host}:{args.port}")

    # Load the FAISS retriever
    embedding_model = get_embedding_model()
    retriever = load_faiss_index(args.faiss_dir, embedding_model)
    retriever.search_kwargs["k"] = args.k

    # Create the RAG chain
    chain = create_rag_chain(retriever=retriever, llm_provider_name="llama_cpp")

    if args.web:
        start_web_chat(chain, host=args.host, port=args.port)
    else:
        start_cli_chat(chain)

if __name__ == "__main__":
    main()