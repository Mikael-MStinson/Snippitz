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

	def tie_data(self, file_id, related_id):
		if file_id == related_id: return
		'''try:
			if related_id in self.list(file_id): return
		except FileNotFoundError:
			pass'''
		self.cursor.execute("insert into connections values ('{}', '{}', NULL)".format(file_id, related_id))
		self.cursor.execute("insert into connections values ('{}', '{}', NULL)".format(related_id, file_id))
		self.database.commit()
		
	def list(self, rowid):
		self.cursor.execute("select related_data_id from connections where file_id='{}'".format(rowid))
		related_ids = self.cursor.fetchall()
		if related_ids == []:
			raise FileNotFoundError("File ID {} is not related to anything".format(rowid))
		return [related_id[0] for related_id in related_ids]
		
	def tie_to_connection(self, file_id, related_id):
		pass
	
	def severe_data(self, fileA, fileB):
		self.cursor.execute("delete from connections where file_id='{}' AND related_data_id='{}'".format(fileA, fileB))
		self.cursor.execute("delete from connections where file_id='{}' AND related_data_id='{}'".format(fileB, fileA))
		self.database.commit()
		self.cursor.execute("select rowid, * from connections")
		print(self.cursor.fetchall())
		
	def merge(self, fileA, fileB):
		fileA_connections = self.list(fileA)
		fileB_connections = self.list(fileB)
		for connection in fileA_connections:
			self.tie(fileB, connection)
		for connection in fileB_connections:
			self.tie(fileA, connection)
			
	def delete(self, rowid):
		self.cursor.execute("delete from data where rowid='{}'".format(rowid))
			
	def register(self, file, *ties):
		self.cursor.execute("insert into data values ('{}')".format(file))
		self.database.commit()
		self.cursor.execute("select rowid, * from data order by rowid desc limit 1")
		rowid = self.cursor.fetchall()[0][0]
		self.tie_data(1, rowid)
		return rowid
		
	def replace(self):
		pass
	
	def merge(self):
		pass
		
	def query(self, synapse_structure):
		pass