import os
import sys
sys.path.append('src\\')

from NetSocket import *

s = NetSocket()
s.open_connection("192.168.0.30")

s.send("Hello world")
print(s.recv().decode())

s.close()