import os
import sys
sys.path.append('src\\')
sys.path.append('src/')

from NetSocket import *

s = NetSocket(t="ROUTER")
s.open_connection("0.0.0.0")
message = None

try:
	while(1):
		message, client = s.recv()
		if(message != None and message != ""):
			s.send(message, client)
		message = None
except KeyboardInterrupt:
	s.close()