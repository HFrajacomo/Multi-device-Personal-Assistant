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
client_to_name = {}

try:
	while(1):
		message, client = s.recv()
		if(message != None and message != ""):
			if(message[0] == "{"):
				d = Device(Device.deserialize(message))
				d.register()
				name_to_client[d.name] = client
				client_to_name[client] = d.name

			else:
				target = Device.devices.get(client_to_name[client], False)
				if(target == False):
					target = client
				elif(name_to_client.get(target.target, False) == False):
					target = client
				else:
					target = name_to_client[target.target]

				s.send(message,  target)
		message = None
except KeyboardInterrupt:
	s.close()