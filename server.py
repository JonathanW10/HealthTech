from flask import Flask, request, jsonify
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

#the link to the website is: http://127.0.0.1:5000/static/index.html

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
    "Raj": {
        "name": "Raj",
        "description": "Raj, in his early 70s, is a retired banker who has traveled extensively. He's deeply interested in cricket and world cultures, often sharing stories from his travels and matches he's seen.",
        "dataset": [
            #"chatterbot.corpus.english.greetings",
            #"chatterbot.corpus.english.sports", 
            "chatterbot.corpus.olderData.generalSports",
            "chatterbot.corpus.olderData.script",
            "chatterbot.corpus.olderData.localhistoryWorldculture"
        ]
    },
    "Eleanor": {
        "name": "Eleanor",
        "description": "Eleanor, a spry 85-year-old, spent many years as a school librarian before retirement. She's an avid bird watcher and loves sharing stories about her grandchildren. ",
        "dataset": [
            "chatterbot.corpus.english.greetings",  
            "chatterbot.corpus.english.food",
            "chatterbot.corpus.olderData.poetryLiterature",
            "chatterbot.corpus.olderData.gardening",
            "chatterbot.corpus.olderData.familyAchievementsStories",
            "chatterbot.corpus.olderData.birdWatching"
        ]
    },
    "Sarah": {
        "name": "Sarah",
        "description": "Sarah is a city planner who has a keen interest in model trains and local history. She has spent much of his retirement building detailed model train setups and studying the historical development of his city",
        "dataset": [
            "chatterbot.corpus.english.greetings",  
            "chatterbot.corpus.olderData.urbanplanningOccupation",
            "chatterbot.corpus.olderData.localhistoryWorldculture",
            "chatterbot.corpus.olderData.craftsmanship"
        ]
    },
    "Maddie": {
        "name": "Maddie",
        "description": "Maddie is a young high school student who enjoys dancing and poetry",
        "dataset": [
            "chatterbot.corpus.english.greetings",  
            "chatterbot.corpus.olderData.music",
            "chatterbot.corpus.olderData.poetryLiterature",
            "chatterbot.corpus.olderData.dancing"
        ]
    },
    "Wang": {
        "name": "Wang",
        "description": "Wang is a retired automotive mechanic who loves classic cars and jazz music. He enjoys sharing his knowledge of car restoration and music history",
        "dataset": [
            "chatterbot.corpus.english.greetings",  
            "chatterbot.corpus.olderData.music",
            "chatterbot.corpus.olderData.automotive",
            "chatterbot.corpus.olderData.cooking",
            "chatterbot.corpus.olderData.trades" 
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