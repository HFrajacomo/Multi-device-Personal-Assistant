from kthread import KThread
import json
from time import sleep
import os

from Path import Path

class Lexer:
	def __init__(self, input_dim=20, auto_save=True, sleep_time=120):
		self.input_dim = input_dim
		self.thread_sleep = sleep_time
		self.__file_exists()
		self.auto_save = auto_save

		self.dict = self.__load()

		if(auto_save):
			self.thread = KThread(target=self.__auto_save)
			self.thread.start()

	
	# Main Lexer function to prepare input for Neural Network
	def transform(self, text):
		text = self.__prepare(text)
		words = text.split(" ")
		output = []
		zeros = 0


		# Trims max word count to input_dim
		if(len(words) > self.input_dim):
			words = words[:self.input_dim]
		else:
			zeros = self.input_dim - len(words)

		for w in words:
			if(w in self.dict.keys()):
				output.append(self.dict[w])
			else:
				self.dict[w] = len(self.dict.keys()) + 1
				output.append(self.dict[w])

		# Fills rest of input with NULL
		for i in range(0, zeros):
			output.append(0)

		return output
	
	# Removes punctuation of input text
	def __prepare(self, text):
		t = text.replace("!", "")
		t = t.replace(".", '')
		t = t.replace("?", "")
		return t

	# KTHREADED Lexer auto-save
	def __auto_save(self):
		while(1):
			for i in range(0,60):
				sleep(self.thread_sleep/60)

			with open(str(Path("src\\WordEmbeddings.txt")), "w") as f:
				json.dump(self.dict, f)

	# Saves Word Embeddings dictionary
	def save(self):
		try:
			with open(str(Path("src\\WordEmbeddings.txt")), "w") as f:
				json.dump(self.dict, f)
		except:
			raise IOError(str(Path("src\\WordEmbeddings.txt")))

	# Loads Word Embeddings dictionary
	def __load(self):
		try:
			with open(str(Path("src\\WordEmbeddings.txt")), "r") as f:
				data = json.load(f)

			return data
		except json.decoder.JSONDecodeError:
			data = {}
			return data
		except:
			raise IOError(str(Path("src\\WordEmbeddings.txt")))

	# Kills auto_save thread
	def delete(self):
		if(self.auto_save):
			self.thread.kill()
			self.save()

	# Check existance of Word Embeddings file
	def __file_exists(self):
		if(not os.path.isfile(str(Path("src\\WordEmbeddings.txt")))):
			file = open(str(Path("src\\WordEmbeddings.txt")), "w")
			file.close()

# Raises on invalid type definition
class IOError(Exception):
	def __init__(self, file):
		self.message = str(file)

	def __str__(self):
		return f"Something went wrong when opening file {self.message}"



a = Lexer(sleep_time=2)
print(a.transform("Hello, my name is Sky"))
a.delete()
