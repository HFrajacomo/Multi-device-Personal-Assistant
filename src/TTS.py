import subprocess as sp
from kthread import KThread
from time import sleep
import os

from Path import *

class TTS:
	def __init__(self):
		# Event Handlers
		self.queue = []
		# Threading and control
		self.BUSY = False
		self.thread = KThread(target=self.__process_creator)
		self.thread.start()
		self.OS = os.name

	# Adds speech to speech queue
	def speak(self, text):
		self.queue.append(text)
		print(f"Added: {text}")

	# KTHREADED runs proccess initiator for speech
	def __process_creator(self):
		while(1):
			if(self.BUSY or self.queue == []):
				sleep(0.1)
				continue

			self.BUSY = True

			if(self.OS == 'nt'):
				sp.call(["powershell", "python", str(Path("src\\SpeechProcess.py")), str(self.queue.pop(0))], universal_newlines=True)
			else:
				sp.check_output(["python3", str(Path("src\\SpeechProcess.py")), str(self.queue.pop(0))], universal_newlines=True)

			self.BUSY = False

	# Kills thread on deletion
	def delete(self):
		self.thread.kill()