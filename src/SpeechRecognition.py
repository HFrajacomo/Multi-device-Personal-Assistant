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
	exception_phrases = ["What?", "I did not understand", "What did you say?", "What was that?"]

	def __init__(self, energy=2000, exception=False):
		self.client = sr.Recognizer()
		self.text = ""
		self.exception = exception


		# Adjust Noise
		#with sr.Microphone() as source:
		#	self.client.adjust_for_ambient_noise(source)

		self.client.energy_threshold = energy

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
				recognized_text = self.__clean(recognized_text)

				return recognized_text
		except KeyboardInterrupt:
			self.close()
			raise SpeechRecognitionError()

	# KThreaded to recognize audio
	def audio_thread(self):
		while(1):
			try:
				with sr.Microphone() as source:
					audio = self.client.listen(source)
					try:
						self.text = self.client.recognize_google(audio)
						if(self.text == None):
							if(self.exception):
								self.text = self.__get_exception()
							else:
								continue
					except:
						try:
							self.text = self.client.recognize_sphinx(audio)
							if(self.text == None):
								if(self.exception):
									self.text = self.__get_exception()
								else:
									continue

						except:
							self.text = "Something is wrong with my Speech Recognition"

					if(self.LOCK.locked()):
						self.LOCK.release()
			except KeyboardInterrupt:
				self.close()
				raise SpeechRecognitionError()

	# Formats string to usable format
	def __clean(self, text):
		text = text.replace("\'s", " is")
		text = text.replace("n\'t", " not")
		return text

	# Closes all thread activity
	def close(self):
		self.thread.kill()
		self.EXIT = True

		if(self.LOCK.locked()):
			self.LOCK.release()

	# Gets a random exception phrase
	def __get_exception(self):
		return self.exception_phrases[randint(0,len(self.exception_phrases)-1)]


# Raises on invalid type definition
class SpeechRecognitionError(Exception):

	def __str__(self):
		return f"Something went wrong in the SpeechRecognizer"
