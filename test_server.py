import os
import sys
sys.path.append('src\\')
sys.path.append('src/')

from NetSocket import *
from Device import *

s = NetSocket(t="ROUTER")
s.open_connection("0.0.0.0")
message = None
server_device = Device({'name':'Sky_server', 'target':'None'})
name_to_client = {}

# Gets the name of a client
def map_client(client):
	for k in name_to_client.keys():
		if(name_to_client[k] == client):
			return k

# Formats string to usable format
def clean(text):
	text = text.replace("\'s", " is")
	text = text.replace("n\'t", " not")
	return text

try:
	while(1):
		message, client = s.recv()
		if(message != None and message != ""):
			if(message[0] == "<CLOSING>"):
				continue

			if(message[0] == "{"):
				d = Device(Device.deserialize(message))
				d.register()
				name_to_client[d.name] = client

			else:
				d = Device.devices.get(map_client(client), False)
				if(d == False):
					target = client
				elif(name_to_client.get(d.target, False) == False):
					target = client
				else:
					target = name_to_client[d.target]

				message = clean(message)
				s.send(message, target)
		message = None
except KeyboardInterrupt:
	s.close()