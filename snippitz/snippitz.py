import sqlite3

class Snippitz:
	def __init__(self, database):
		self.database = sqlite3.connect(database)
		self.cursor = self.database.cursor()
		self.cursor.execute("CREATE TABLE connections ( file text, relative text)")
		self.database.commit()
		
	def close(self):
		self.database.close()

	def tie(self, fileA, fileB):
		if fileA == fileB: return
		try:
			if fileB in self.list(fileA): return
		except FileNotFoundError:
			pass
		self.cursor.execute("INSERT INTO connections VALUES ('{}', '{}')".format(fileA, fileB))
		self.cursor.execute("INSERT INTO connections VALUES ('{}', '{}')".format(fileB, fileA))
		self.database.commit()
		
	def list(self, file):
		self.cursor.execute("SELECT * FROM connections WHERE file='{}'".format(file))
		l = self.cursor.fetchall()
		if l == []:
			raise FileNotFoundError("The file {} is not registered with Snippitz".format(file))
		return [i[1] for i in l]
		
	def severe(self, fileA, fileB):
		self.cursor.execute("DELETE FROM connections WHERE file='{}' AND relative='{}'".format(fileA, fileB))
		self.cursor.execute("DELETE FROM connections WHERE file='{}' AND relative='{}'".format(fileB, fileA))
		self.database.commit()