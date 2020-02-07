import os

class Path:
	def __init__(self, path):
		if(os.name == "nt"):
			self.path = path.replace("/", "\\")
		else:
			self.path = path.replace("\\", "/")

	def __str__(self):
		return self.path

	def __repr__(self):
		return self.path

	def __getitem__(self, num):
		if(os.name == "nt"):
			l = self.path.split("\\")
			if(l[-1] == ""):
				l.pop()
			return l[num]

		else:
			l = self.path.split("/")
			if(l[-1] == ""):
				l.pop()
			return l[num]