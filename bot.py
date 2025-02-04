'''
Author:Maggie Crawford
Date: 12th Nov , 2024
Project: Health Hub -Health Companion

Solution provides base AI chat bot structure and training format to create a Mental Health resource companion
'''

#do this before running to allow scripts to run: Set-ExecutionPolicy Unrestricted -Scope Process
#Then activate the envionment using: chatbotenv\Scripts\activate

#To add text to speech, first run: pip install pyttsx3
#To add speech to text for input: pip install SpeechRecognition
#Also need to install this to use microphone: pip install pyaudio

import pyttsx3 #Text-to-speech
import speech_recognition as sr  # Speech-to-text

from chatterbot import ChatBot
import nltk
nltk.download('punkt_tab')
from chatterbot.trainers import ListTrainer
import train
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot_name = "Your Companion"
chatbot = ChatBot(chatbot_name)
# trainer = ListTrainer(chatbot)
trainer = ChatterBotCorpusTrainer(chatbot)


##Run Training Protcols from train.py
#train.introduce_yourself()
#train.trainbot()
trainer.train(
    "chatterbot.corpus.english",
    "formatted_health_training2",

    )

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Set properties for the voice engine
engine.setProperty("rate", 180)  # Adjust speed (default ~200)
engine.setProperty("volume", 1.0)  # Adjust volume (0.0 to 1.0)

# Select a different voice
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Change index for different voices

# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak now:")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)  # Google Web Speech API
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results. Check your internet connection.")
        return None

##Chat-Response loop
while True:
    #query = input(">  ")
    #if query in train.exit_conditions:
        #break

    #for speech to text as input
    query = speech_to_text()  # Get user input via speech
    if query is None: # If speech recognition failed, skip this loop iteration
        continue
    # Check exit condition
    if query.lower() in train.exit_conditions:
        break
    else:
        #print(f">>>>: {chatbot.get_response(query)}")

        #for text to speech
        response = chatbot.get_response(query)
        print(f">>>>: {response}")
        speak(str(response))  # Convert response to speech