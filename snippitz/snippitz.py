import sqlite3

class Snippitz:
	def __init__(self, database):
		self.database = sqlite3.connect(database)
		self.cursor = self.database.cursor()
		self.cursor.execute("CREATE TABLE data (data text)")
		self.cursor.execute("INSERT INTO data VALUES ('unsorted')")
		self.cursor.execute("CREATE TABLE connections (file_id integer, related_data_id integer, related_connection_id integer, FOREIGN KEY (related_data_id) REFERENCES data(rowid))")
		self.database.commit()
		
	def open(self):
		pass
		
	def close(self):
		self.database.close()

	def tie_to_file(self, file_id, related_id):
		if file_id == related_id and not related_is_connection: return
		try:
			if related_id in self.list(file_id): return
		except FileNotFoundError:
			pass
		self.cursor.execute("INSERT INTO connections VALUES ('{}', '{}', NULL)".format(file_id, related_id))
		self.cursor.execute("INSERT INTO connections VALUES ('{}', '{}', NULL)".format(related_id, file_id))
		self.database.commit()
		
	def list(self, fileid):
		self.cursor.execute("SELECT * FROM connections WHERE rowid='{}'".format(fileid))
		l = self.cursor.fetchall()
		if l == []:
			raise FileNotFoundError("File ID {} is not registered with Snippitz".format(fileid))
		return [i[1] for i in l]
		
	def tie_to_connection(self, file_id, related_id):
		pass
	
	def severe(self, fileA, fileB):
		self.cursor.execute("DELETE FROM connections WHERE file='{}' AND relative='{}'".format(fileA, fileB))
		self.cursor.execute("DELETE FROM connections WHERE file='{}' AND relative='{}'".format(fileB, fileA))
		self.database.commit()
		
	def merge(self, fileA, fileB):
		fileA_connections = self.list(fileA)
		fileB_connections = self.list(fileB)
		for connection in fileA_connections:
			self.tie(fileB, connection)
		for connection in fileB_connections:
			self.tie(fileA, connection)
			
	def delete(self, file):
		connections = self.list(file)
		for connection in connections:
			self.severe(file, connection)
			
	def register(self, file, *ties):
		self.cursor.execute("INSERT INTO data VALUES ('{}')".format(file))
		self.tie_to_file(file,"unsorted")
		self.database.commit()
		
	def replace(self):
		pass
	
	def merge(self):
		pass
		
	def query(self, synapse_structure):
		pass