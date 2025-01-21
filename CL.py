from flask import Flask, request, jsonify
import openai

# Set up the Groq API base URL and API key
openai.api_base = "https://api.groq.com/openai/v1"
openai.api_key = "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"

# Flask app
app = Flask(__name__)

# Initial knowledge about Composite Labs and Monad
initial_context = """
You are an expert on Composite Labs and Monad. Provide concise, accurate, and relevant answers to user queries. 

### Composite Labs:
- A venture-backed startup developing a next-generation decentralized exchange (DEX) entirely on-chain.
- Key offerings: spot trading, perpetual contracts, and on-chain lending.
- Unique features: central limit order book (CLOB), cross-margin mechanism, enhanced leverage, and low fees.
- Builds on the Monad blockchain for scalability and efficiency.

### Monad:
- A high-performance layer 1 blockchain designed for 10,000 transactions per second, 1-second block times, and single-slot finality.
- 100% Ethereum Virtual Machine (EVM) compatible.
- Innovations include optimistic parallel execution, asynchronous execution, and MonadDB for efficient state storage.
- Backed by $225M funding from Paradigm, Electric Capital, and Greenoaks.

Answer queries in a professional manner, sticking to the scope of Composite Labs and Monad.
"""

conversation_history = [{"role": "system", "content": initial_context}]

# Route for the chatbot
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Add user input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Get a response from the Groq API
        response = openai.ChatCompletion.create(
            model="llama-3.3-70b-versatile",  # Replace with the actual model name
            messages=conversation_history,
            temperature=0.5,
            max_tokens=256,
            top_p=1.0,
        )
        assistant_message = response["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": assistant_message})

        return jsonify({"response": assistant_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Welcome route
@app.route("/", methods=["GET"])
def welcome():
    return "Welcome to the Composite Labs and Monad chatbot API. Use the /chat endpoint to interact with the bot."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
