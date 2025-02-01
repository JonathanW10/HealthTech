'''
Run this code to clear all data previously learned from training lessons. The bot will store the chats in the "db.sqlite3" file
even after the program has ended, so if undesired topics/ words are taught this will clear everything and begin the training from
the source code again.
'''

import bot


# Clear the database from previous training lessons
bot.chatbot.storage.drop()
