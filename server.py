from flask import Flask, request, jsonify
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests

# Initialize chatbot
#chatbot = ChatBot("Health Companion", storage_adapter="chatterbot.storage.SQLStorageAdapter")
chatbot = ChatBot(
    "Health Companion",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///your_database.db",
    database_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        # Add any other adapters you need
    ],
    preprocessors=[
        "chatterbot.preprocessors.clean_whitespace",
    ],
    read_only=True
)
trainer = ChatterBotCorpusTrainer(chatbot)

# Define personalized profiles with specific interests
profiles = {
    "Joe": {
        "name": "Joe",
        "description": "I enjoy sports and history. I love discussing past events and sporting achievements.",
        "dataset": [
            "chatterbot.corpus.english.greetings",
            "chatterbot.corpus.english.sports", 
            "chatterbot.corpus.english.history"
        ]
    },
    "Annie": {
        "name": "Annie",
        "description": "I enjoy cooking and science. I love sharing recipes and hiking tips.",
        "dataset": [
            "chatterbot.corpus.english.greetings",  
            "chatterbot.corpus.english.food",
            "chatterbot.corpus.english.science"
        ]
    },
    "Sarah": {
        "name": "Sarah",
        "description": "I enjoy movies and trivia. Let's talk!",
        "dataset": [
            "chatterbot.corpus.english.greetings",  
            "chatterbot.corpus.english.movies",
            "chatterbot.corpus.english.trivia"  
        ]
    }
}

# Train each profile with its own dataset
def train_profile(profile_name):
    chatbot.storage.drop()  # Clear previous data
    # Load the dataset specific to the profile
    profile_data_files = profiles[profile_name]["dataset"]
    try:
        for profile_data_file in profile_data_files:
            trainer.train(profile_data_file)
    except Exception as e:
        print(f"Error training profile {profile_name}: {e}")


# Define routes for chatbot interaction
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    personality = data.get("personality", "Joe")  # Default: Joe profile
    user_message = data["message"]

    # Train the selected profile
    train_profile(personality)  # Re-train with the selected profile's dataset

    # Get a response from the chatbot
    bot_response = chatbot.get_response(user_message)

    # Return the response text (not the Statement object) in the JSON
    return jsonify({"reply": str(bot_response.text)})

if __name__ == "__main__":
    app.run(debug=True)
