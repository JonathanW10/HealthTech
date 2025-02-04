# train

from chatterbot import ChatBot
import nltk
nltk.download('punkt_tab')
from chatterbot.trainers import ListTrainer
from chatterbot_corpus import data
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot_name = "Your Companion"
chatbot = ChatBot(chatbot_name, read_only=False)

##Define types of chat trainers
List_trainer = ListTrainer(chatbot)
Corpus_trainer = ChatterBotCorpusTrainer(chatbot)

##Terms that will end the chat
exit_conditions = (":q", "quit", "exit", "bye", "goodbye", "go away", "goodnight", "shut up")

name = None
age = None
hobby = None



def introduce_yourself():
    name = input("What is your name? (ex. Maggie): ")
    if name in exit_conditions:
        return 0
    
    age = input("How old are you? (ex. 20): ")
    if age in exit_conditions:
        return 0
    
    hobby = input("What is your favorite hobby (ex. baking): ")
    if hobby in exit_conditions:
        return 0


def trainbot():
    #Training chatbot with .yml files from chatterbot_corpus
    Corpus_trainer.train(
        "chatterbot.corpus.english.emotion",
        "chatterbot.corpus.english.conversations",
        "chatterbot.corpus.english.greetings",
        "formatted_health_training2"
    )

    ##Training chatbot with single conversation lines
    List_trainer.train([
    "What is my name?",
    "Your name is {name}",
    ])
    List_trainer.train([
    "How old am I?",
    "You are {age} years young",
    ])
    List_trainer.train([
    "I dont know what to do",
    "You should try {hobby}",
    ])

    List_trainer.train([
    "Hi",
    "How can I help you?",
    ])
    List_trainer.train([
    "i am not feeling well",
    "is it mental or physical?",
    ])
    List_trainer.train([
    "i am sad",
    "do you want to talk to me about it?",
    ])
    
    return print("training complete")
