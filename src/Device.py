import json
import os
import socket
import subprocess as sp
import ast

from Path import Path
'''
This class is used as an i/o for the known_devices file.
It stores connected devices history to a server

Device.devices is a dict where the key is the name the user wants to give
and the value is the Device class
'''

class Device:
	devices = {}
	def __init__(self, serial):
		self.__check_serial(serial)

		self.name = serial['name']
		if(serial.get('iip', False) == False and serial.get('eip', False) == False):
			self.__get_ip()
		else:
			if(serial.get('iip', False) != False):
				self.iip = serial['iip']
			else:
				self.iip = ""
			if(serial.get('eip', False) != False):
				self.eip = serial['eip']				
			else:
				self.eip = ""

		if(self.iip == "" and self.eip == ""):
			raise UnadressableDevice(name)

		self.target = serial['target']

	# Check existance of serial
	def __check_serial(self, serial):
		if(serial.get("name", False) == False):
			raise UnsetName()
		if(serial.get("target", False) == False):
			raise UnsetName()

	# Registers device to devices
	def register(self):
		if(self.name in Device.devices.keys()):
			raise InvalidDeviceName(name)
		else:
			Device.devices[self.name] = self

	# Returns device from devices
	@staticmethod
	def get(name):
		if(Device.devices.get(name, False)):
			return Device.devices[name]
		else:
			raise DeviceNotRegistered(name)

	# Loads all devices from file
	@staticmethod
	def __load(self):
		try:
			with open(str(Path("src\\known_devices.txt")), "r") as f:
				self.devices = json.load(f)

			return data
		except json.decoder.JSONDecodeError:
			self.devices = {}
			return data
		except:
			raise IOError(str(Path("src\\known_devices.txt")))

	# Checks if known_devices file exists, if not, creates it
	@staticmethod
	def __check_file():
		if(not os.path.isfile(str(Path("src\\known_devices.txt")))):
			file = open(str(Path("src\\known_devices.txt")), "w")
			f.close()

	# Automatically gets IDs
	def __get_ip(self):
		self.iip = socket.gethostbyname(socket.gethostname())
		if(self.iip == '127.0.0.1'):
			self.iip = ''
	
		try:
			if(os.name == "nt"):
				self.eip = sp.check_output(["powershell.exe", "(curl ifconfig.me).Content"], universal_newlines=True)[:-1]
			else:
				self.eip = sp.check_output(["curl ifconfig.me"], universal_newlines=True)
		except:
			self.eip == ''

	def __str__(self):
		return f"Device: {self.name}\nInternal IP: {self.iip}\nExternal IP: {self.eip}\nTarget: {self.target}\n"		

	def __repr__(self):
		return f"Device: {self.name}\nInternal IP: {self.iip}\nExternal IP: {self.eip}\nTarget: {self.target}\n"


	# Returns a serialized Device
	def serialize(self):
		return f"{str({'name': self.name, 'iip': self.iip, 'eip': self.eip, 'target': self.target})}"

	# String to dict deserialization
	@staticmethod
	def deserialize(text):
		return ast.literal_eval(text)



# Raises on not defining iip or eip
class UnadressableDevice(Exception):
	def __init__(self, name):
		self.message = str(name)

	def __str__(self):
		return f"Device {self.message} is not addressable. Please set an internal or external ip"

# Raises on not defining iip or eip
class DeviceNotRegistered(Exception):
	def __init__(self, name):
		self.message = str(name)

	def __str__(self):
		return f"Device {self.message} is not registered in known_devices.txt file"

# Raises on not defining iip or eip
class InvalidDeviceName(Exception):
	def __init__(self, name):
		self.message = str(name)

	def __str__(self):
		return f"Device {self.message} is already registered"

# Raises on not defining name
class UnsetName(Exception):
	def __str__(self):
		return f"Device must have a name and a target set"
