from dataclasses import replace
from email import message
import pywhatkit
# for speech-to-text
from cgitb import text
from tracemalloc import start
import speech_recognition as sr
# for text-to-speech
from gtts import gTTS
# for language model
import transformers
import os 
import time
import webbrowser
import pyjokes
# for data
#import os
import datetime
import numpy as np
# Building the AI

class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(mic)
            audio = recognizer.listen(mic)
            self.text = "ERROR"
        try:
            self.text = recognizer.recognize_google(audio)
            print("Me  --> ", self.text)
        except:
            print("Me  -->  ERROR")

    @staticmethod
    def text_to_speech(text):
        print("om --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        statbuf = os.stat("res.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        # if you are using mac->afplay or else for windows->start
        os.system('start res.mp3')
        # os.system("close res.mp3")
        time.sleep(int(50*duration))
        os.remove("res.mp3")

    def wake_up(self, text):
        return True if self.name in text.lower() else False
 
    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M:%p')


# Running the AI
if __name__ == "__main__":
    ai = ChatBot(name="om")
    nlp = transformers.pipeline(
        "conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    ex = True
    while ex:
        ai.speech_to_text()
        # wake up
        if ai.wake_up(ai.text) is True:
            res = "Hello I am Personal command assistant AI, chatbot what can i do for you?"
            
        elif "name" in ai.text:
            res = "Hello I am Personal command assistant AI Chatbot, What can i do?"
            
        elif "happy birthday dear" in ai.text:
            res = np.random.choice(["Happy birthday to my best friend in the whole wide world!","Cheers to your personal new year! Let’s live it up.",
                                    "Happy birthday to the person who knows all my secrets","You make the world a better and brighter place. Happy birthday, bestie!",
                                    "Today should be a national holiday because it’s the day my best friend was born!","Wishing you the best birthday yet!"])
        
        elif "jokes" in ai.text:
                om =  pyjokes.get_jokes(language="en", category="neutral")
                res=np.random.choice(om)
        
            
        
            
        elif "open Google" in ai.text:
            webbrowser.open("https://www.google.com/")
            res = "google is open"
        elif "open YouTube" in ai.text:
             webbrowser.open("https://www.youtube.com/")
             res = "youtube is open"
       
             
        
       
        elif "open chrome" in ai.text:
            webbrowser.open("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            res = "chrome is open"
        
            
           
            
        # action time
        elif "time" in ai.text: 
            res = ai.action_time()
        # respond politely
        elif any(i in ai.text for i in ["thank", "thanks"]):
            res = np.random.choice(["you're welcome!", "anytime!", "no problem!",
                                   "cool!", "I'm here if you need me!", "mention not"])
        elif any(i in ai.text for i in ["exit", "close"]):
            res = np.random.choice(
                ["Tata", "Have a good day", "Bye", "Goodbye", "Hope to meet soon", "peace out!"])
    
            ex = False
        # conversation
        else:
            if ai.text == "ERROR":
                res = "Sorry, come again?"
            else:
                chat = nlp(transformers.Conversation(
                    ai.text), pad_token_id=50256)
                res = str(chat)
                res = res[res.find("bot >> ")+6:].strip()
        ai.text_to_speech(res)
    print("----- Closing down om -----") 