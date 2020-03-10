import os
import sys
sys.path.append('src\\')
sys.path.append('src/')

from NetSocket import *
from Device import *

s = NetSocket()
s.open_connection("192.168.0.30")
device = Device({'name':'WinDesktop', 'target':'phone'})

s.send(device.serialize())
s.send("Hello")
print(s.recv().decode())

s.close()