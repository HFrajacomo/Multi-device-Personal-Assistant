import os
import sys
from time import sleep
from kthread import KThread

sys.path.append('src\\')
sys.path.append('src/')

from NetSocket import *
from Device import *
from TTS import *
from SpeechRecognition import *

s = NetSocket()
s.open_connection("192.168.0.30")
device = Device({'name':'WinDesktop', 'target':'phone'})
threads = []
tts = TTS()
sr = SpeechRecognition()

# Threads that receives data from server
def receive_thread():
	try:
		while(True):
			message = s.recv()
			tts.speak(message)
			pass
	except KeyboardInterrupt:
		kill_all()
		sys.exit()

# Thread that sends speech recognized audio to server
def send_thread():
	try:
		while(True):
			spoken_text = sr.recv_text()

			if(spoken_text.lower() == "quit"):
				return

			sleep(1)
			s.send(spoken_text)

	except KeyboardInterrupt:
		kill_all()
		sys.exit()
	except SpeechRecognitionError:
		kill_all()
		sys.exit()
		raise SpeechRecognitionError

# Just closes everything
def kill_all():
	for th in threads:
		try:
			th.kill()
		except:
			pass

	s.close()
	tts.close()
	sr.close()

# Reconnects to target device
def connect_hb():
	sleep(10)
	s.send(device.serialize())

try:
	s.send(device.serialize())
	threads.append(KThread(target=receive_thread))
	threads.append(KThread(target=send_thread))

	for th in threads:
		th.start()

	connect_hb()

	while(True):
		sleep(1)

except KeyboardInterrupt:
	kill_all()
	sys.exit()