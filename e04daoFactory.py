from e04Enum import InputType

class factory:
	def getInstance(self,t):
		if t == InputType.mongodb:
			from mongodb import database
			return database()
		elif t == InputType.mysql:
			from mysqldb import database
			return database()
		elif t == InputType.csv:
			from csvStore import database
			return database()
		else:
			return None