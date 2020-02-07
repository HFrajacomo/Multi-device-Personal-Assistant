import os
import sys
from socket import *
from kthread import KThread
from threading import Lock

class NetSocket:
	def __init__(self, t="DEALER"):
		self.type = t  # "DEALER" or "ROUTER"
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.port = 33000
		self.receive_buffer = []
		self.LOCK = Lock()

		if(self.type == "ROUTER"):
			self.ips = []
			self.clients = []
			self.receive_threads = {}
			self.traffic_thread = None

		if(t != "DEALER" and t != "ROUTER"):
			raise SocketTypeError(t)

	# Encrypt and decrypt message
	def __crypt(self, text):
		'''
		new = ""
		for e in text:
			new += chr(ord(e) ^ ord("B"))
		'''
		return text#new

	# Turns message into bytes
	def __byt(self, text):
		return bytes(text, "UTF-8")

	# Sets connection or binding
	# Is persistent on DEALER connections
	def open_connection(self, ip):
		if(self.type == "DEALER"):
			CONNECTED = False

			# Persistent connection
			while(not CONNECTED):
				try:
					self.sock.connect((ip, self.port))
					CONNECTED = True
				except ConnectionRefusedError:
					continue


			self.traffic_thread = KThread(target=self.handle_receives_dealer)
			self.traffic_thread.start()
		elif(self.type == "ROUTER"):
			self.sock.bind(("0.0.0.0", self.port))
			self.sock.listen(1)
			self.traffic_thread = KThread(target=self.accept_connections)
			self.traffic_thread.start()
			
	# Sends message to other connection
	def send(self, message, client=None):
		try:
			if(self.type == "DEALER"):
				self.sock.send(self.__byt(self.__crypt(message)))
			elif(self.type == "ROUTER"):
				##### CHANGE LATER BECAUSE ROUTER CAN 'ROUTE' THINGS
				client.send(self.__byt(self.__crypt(message)))
		except:
			pass

	# Receives message from other connection
	def recv(self):
		while(1):
			try:
				if(self.type == "DEALER"):
					if(self.receive_buffer == []):
						self.LOCK.acquire()
						continue

					message = self.receive_buffer.pop(0)
					return self.__crypt(message)

				elif(self.type == "ROUTER"):

					if(self.receive_buffer == []):
						self.LOCK.acquire()
						continue

					message, client = self.receive_buffer.pop(0)
					return (self.__crypt(message.decode()), client)
			except:
				continue

	# KTHREADED
	# Handles connection traffic
	def accept_connections(self):
		if(self.type == "ROUTER"):
			while(1):
				client, client_address = self.sock.accept()
				self.clients.append(client)
				self.ips.append(client_address)
				print(f"{client_address} Connected")
				print(len(self.clients))

				if(client in self.receive_threads.keys()):
					self.receive_threads[client].kill()

				self.receive_threads[client] = KThread(target=self.handle_receives_router, args=(client,))
				self.receive_threads[client].start()	

	# KTHREADED
	# Receives all data from clients and puts them on receive_buffer
	def handle_receives_dealer(self):
		while(1):
			message = self.sock.recv(4096)
			if(self.socket_control(message, None)):
				continue

			self.receive_buffer.append(message)
			if(self.LOCK.locked()):
				self.LOCK.release()

	# KTHREADED
	# Receives all data from clients and puts them on receive_buffer
	def handle_receives_router(self, client):
		try:
			while(client in self.clients):
				message = client.recv(4096)
				if(self.socket_control(message, client)):
					continue

				self.receive_buffer.append((message, client))
				if(self.LOCK.locked()):
					self.LOCK.release()
		except ConnectionResetError:
			self.remove_connection(client)
			print(f"{client} Disconnected")

	'''
	This function handles all 'socket controlling' operations
	Add new if's to all new operations if needed
	'''
	def socket_control(self, message, client):
		if(message == "<CLOSING>" and self.type == "ROUTER"):
			self.clients.remove(client)
			if(self.LOCK.locked()):
				self.LOCK.release()
			return True

		elif(message == "<CLOSING>" and self.type == "DEALER"):
			self.sock.shutdown(0)
			self.sock.close()
			return True

		return False

	# Totally severs connections
	def close(self):
		if(self.type == "DEALER"):
			self.sock.send(self.__byt(self.__crypt("<CLOSING>")))
			self.sock.shutdown(0)
			self.sock.close()
			self.traffic_thread.kill()
		elif(self.type == "ROUTER"):
			self.sock.shutdown(0)
			self.sock.close()
			self.ips = []
			self.clients = []
			self.traffic_thread.kill()
			for th in self.receive_threads.keys():
				self.receive_threads[th].kill()

	# Removes a connection from ROUTER sockets
	# Usually called on ConnectionResetError exception
	def remove_connection(self, client):
		if(self.type == "ROUTER"):
			self.clients.remove(client)
			self.receive_threads[client].kill()



# Raises on invalid type definition
class SocketTypeError(Exception):
	def __init__(self, invalid_type):
		self.message = str(invalid_type)

	def __str__(self):
		return f"type '{self.message}' is not valid. Try 'DEALER' or 'ROUTER' only"
