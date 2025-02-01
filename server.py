from flask import Flask, request, jsonify
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests

# Initialize chatbot
chatbot = ChatBot("Health Companion")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

# Define chatbot personalities
profiles = {
    "calm": "I provide gentle and comforting advice.",
    "motivational": "I offer energetic and uplifting advice!",
    "logical": "I analyze problems critically."
}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    personality = data.get("personality", "calm")  # Default: calm mode
    user_message = data["message"]

    bot_response = chatbot.get_response(user_message)
    final_response = f"[{personality.upper()} MODE] {profiles[personality]} {bot_response}"

    return jsonify({"reply": final_response})

if __name__ == "__main__":
    app.run(debug=True)