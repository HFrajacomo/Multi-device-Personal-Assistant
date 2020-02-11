import pyttsx3
import sys

text = " ".join(sys.argv[1:])

# TTS Engine
engine = pyttsx3.init()
engine.setProperty('rate', 133)
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)

engine.say(text)
engine.runAndWait()
sys.exit()