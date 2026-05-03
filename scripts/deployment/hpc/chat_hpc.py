"""Legacy HPC CLI/Flask chat harness for an injected RAG chain."""

import argparse
import socket
import time

import requests
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

            result = chain.invoke(prompt)
            # The RAG chain returns a dict with keys including 'answer'
            if isinstance(result, dict):
                answer = result.get("answer", "")
            else:
                answer = str(result)
            print(f"Assistant: {answer}")

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
        result = chain.invoke(user_message)
        if isinstance(result, dict):
            answer = result.get("answer", "")
        else:
            answer = str(result)
        return jsonify({"response": answer})

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    node = socket.getfqdn() or "localhost"
    print(f"Starting web server at http://{host}:{port} (node: {node})", flush=True)
    app.run(host=host, port=port, debug=False)

def _ensure_provider_health(
    provider_name: str,
    host: str,
    max_wait_seconds: float,
    interval_seconds: float,
) -> None:
    """Wait for an HTTP provider health endpoint before starting the chat app."""

    url = config.provider_health_url(provider_name, host=host)
    if url is None:
        return
    deadline = time.time() + max_wait_seconds
    while time.time() < deadline:
        try:
            response = requests.get(url, timeout=5)
        except requests.RequestException as exc:
            logger.warning("Health probe failed for %s: %s", url, exc)
            time.sleep(interval_seconds)
            continue
        if response.status_code == 200:
            logger.info("Provider health check OK: %s", url)
            return
        logger.warning(
            "Health probe for %s returned %s; retrying...",
            url,
            response.status_code,
        )
        time.sleep(interval_seconds)
    raise RuntimeError(
        f"Provider health check failed for {provider_name} at {url} within {max_wait_seconds}s"
    )


def main():
    """Load the persisted FAISS index, create the RAG chain, and start chat."""

    parser = argparse.ArgumentParser(description="Chat with a local Llama model using RAG.")
    parser.add_argument("--vector-store", type=str, default="faiss", help="The vector store to use.")
    parser.add_argument("--faiss-dir", type=str, default="vector_index/faiss_amarel", help="Path to the saved FAISS index.")
    parser.add_argument("--k", type=int, default=5, help="The number of documents to retrieve.")
    parser.add_argument("--web", action="store_true", help="Start the web-based chat interface.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the web server to.")
    parser.add_argument("--port", type=int, default=8088, help="Port to bind the web server to.")
    parser.add_argument(
        "--provider",
        type=str,
        default=config.DEFAULT_LLM_PROVIDER,
        choices=["llama_cpp", "huggingface_api", "vllm", "vllm_api", "sglang", "sglang_api"],
        help="LLM provider to use when constructing the RAG chain.",
    )
    parser.add_argument(
        "--provider-health-host",
        type=str,
        default="127.0.0.1",
        help="Host address to probe for provider /healthz endpoint when applicable.",
    )
    parser.add_argument(
        "--provider-health-timeout",
        type=float,
        default=45.0,
        help="Seconds to wait for the provider health endpoint before failing.",
    )
    parser.add_argument(
        "--provider-health-interval",
        type=float,
        default=5.0,
        help="Seconds between provider health checks.",
    )
    args = parser.parse_args()

    logger.info("Starting chat with the following configuration:")
    logger.info(f"  Model path: {config.LLAMA_CPP_MODEL_PATH}")
    logger.info(f"  Embedding model name: {config.EMBEDDING_MODEL}")
    logger.info(f"  FAISS index path: {args.faiss_dir}")
    logger.info(f"  k: {args.k}")
    logger.info("  Maximum context length: 2048")
    logger.info(f"  LLM provider: {args.provider}")

    if args.web:
        logger.info(f"  Web bind: http://{args.host}:{args.port}")

    try:
        _ensure_provider_health(
            provider_name=args.provider,
            host=args.provider_health_host,
            max_wait_seconds=args.provider_health_timeout,
            interval_seconds=args.provider_health_interval,
        )
    except RuntimeError as exc:
        logger.error(str(exc))
        raise SystemExit(1) from exc

    # Load the FAISS retriever
    embedding_model = get_embedding_model()
    retriever = load_faiss_index(args.faiss_dir, embedding_model)
    retriever.search_kwargs["k"] = args.k

    # Create the RAG chain
    chain = create_rag_chain(retriever=retriever, llm_provider_name=args.provider)

    if args.web:
        start_web_chat(chain, host=args.host, port=args.port)
    else:
        start_cli_chat(chain)

if __name__ == "__main__":
    main()
