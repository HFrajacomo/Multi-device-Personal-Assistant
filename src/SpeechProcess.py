import pyttsx3
import sys

'''
Instantiation of a voice call. Everytime Sky opens a voice speech command,
this script is run in a new process
'''

text = " ".join(sys.argv[1:])

# TTS Engine
engine = pyttsx3.init()
engine.setProperty('rate', 133)
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)

engine.say(text)
engine.runAndWait()
sys.exit()