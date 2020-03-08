import speech_recognition as sr
from threading import Lock
from kthread import KThread
from random import randint
import os
import sys

from Path import Path

'''
Speech Recognition module. Run whenever speech is detected in Sky
'''

class SpeechRecognition:
	exception_phrases = ["What?", "I didn't undestand", "What did you say?", "What was that?"]

	def __init__(self):
		self.client = sr.Recognizer()
		self.text = ""

		self.LOCK = Lock()
		self.EXIT = False
		self.thread = KThread(target=self.audio_thread)
		self.thread.start()

	# Blocks until audio thread gets a text
	def recv_text(self):
		try:
			while(1):
				if(self.EXIT):
					return

				if(self.text == ""):
					self.LOCK.acquire()
					continue

				recognized_text = self.text
				self.text = ""
				return recognized_text
		except KeyboardInterrupt:
			self.close()
			sys.exit()

	# KThreaded to recognize audio
	def audio_thread(self):
		while(1):
			with sr.Microphone() as source:
				print("Speak")
				audio = self.client.listen(source)
				try:
					self.text = self.client.recognize_google(audio)
					if(self.text == None):
						self.text = self.__get_exception()
				except:
					try:
						self.text = self.client.recognize_sphinx(audio)
						if(self.text == None):
							self.text = self.__get_exception()

					except:
						self.text = "Something is wrong with my Speech Recognition"

				if(self.LOCK.locked()):
					self.LOCK.release()

	# Closes all thread activity
	def close(self):
		self.thread.kill()
		self.EXIT = True

		if(self.LOCK.locked()):
			self.LOCK.release()

	# Gets a random exception phrase
	def __get_exception(self):
		return self.exception_phrases[randint(0,len(self.exception_phrases)-1)]

microfone = SpeechRecognition()
try:
	while(1):
		text = microfone.recv_text()
		print(text)
except KeyboardInterrupt:
	microfone.close()
	sys.exit()