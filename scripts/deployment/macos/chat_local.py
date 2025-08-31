from llama_cpp import Llama
import sys
import os
import argparse
from flask import Flask, render_template_string, request, jsonify

from src.rag.config import LLAMA_CPP_MODEL_PATH

# Initialize the Llama model instance globally
llm = Llama(model_path=LLAMA_CPP_MODEL_PATH, chat_format="llama-3")

def start_cli_chat():
    """
    Starts an interactive command-line chat session.
    """
    print("Starting CLI chat with Phi-3. Type 'exit' or 'quit' to end.")

    while True:
        try:
            prompt = input("You: ")
            if prompt.lower() in ["exit", "quit"]:
                break

            formatted_prompt = f"<|user|>\n{prompt}<|end|>\n<|assistant|>"
            response = llm(formatted_prompt, max_tokens=1024, stop=["<|end|>"], echo=False)
            print(f"Assistant: {response['choices'][0]['text'].strip()}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    print("\nChat ended.")

def start_web_chat():
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
        formatted_prompt = f"<|user|>\n{user_message}<|end|>\n<|assistant|>"
        response = llm(formatted_prompt, max_tokens=1024, stop=["<|end|>"], echo=False)
        bot_response = response['choices'][0]['text'].strip()
        return jsonify({"response": bot_response})

    print("Starting web server at http://127.0.0.1:8088")
    app.run(host="0.0.0.0", port=8088)

def main():
    parser = argparse.ArgumentParser(description="Chat with a local Llama model.")
    parser.add_argument("--web", action="store_true", help="Start the web-based chat interface.")
    args = parser.parse_args()

    if args.web:
        start_web_chat()
    else:
        start_cli_chat()

if __name__ == "__main__":
    main()