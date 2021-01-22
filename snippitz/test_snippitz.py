from unittest import TestCase
from .snippitz import Snippitz

'''
TODO
tie_data still needs to return a rowid
register still needs to accept a *rowid argument
'''

class TestSnippitz(TestCase):
	def test_register_data(self):	
		snippitz = Snippitz(database = ':memory:')
		new_data_id = snippitz.register("data")
		self.assertEqual(new_data_id, 2)
		new_data_id = snippitz.register("data")
		self.assertEqual(new_data_id, 3)
		new_data_id = snippitz.register("data")
		self.assertEqual(new_data_id, 4)
		snippitz.close()
		
	def test_register_and_delete_data(self):
		snippitz = Snippitz(database = ':memory:')
		new_data_id = snippitz.register("data")
		self.assertEqual(new_data_id, 2)
		new_data_id = snippitz.register("data")
		self.assertEqual(new_data_id, 3)
		snippitz.unregister(2)
		new_data_id = snippitz.register("data")
		self.assertEqual(new_data_id, 4)
		snippitz.close()
	
	def test_register_data_and_list(self):
		snippitz = Snippitz(database = ':memory:')
		self.assertRaises(FileNotFoundError, snippitz.list, 1)
		snippitz.register("data")
		self.assertEqual(snippitz.list(1), [2])
		snippitz.close()
	
	def test_tie_and_list(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.tie_data(2,3)
		self.assertEqual(snippitz.list(2), [3])
		self.assertEqual(snippitz.list(3), [2])
		snippitz.close()
	
	def test_tie_to_itself(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.tie_data(2,2)
		snippitz.tie_data(2,3)
		self.assertEqual(snippitz.list(2), [3])
		self.assertEqual(snippitz.list(3), [2])
		snippitz.close()
		
	def test_tie_to_multiple_files_and_list(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.register("path/file3")
		snippitz.register("path/file4")
		snippitz.tie_data(2,3)
		snippitz.tie_data(2,4)
		snippitz.tie_data(2,5)
		self.assertEqual(snippitz.list(2), [3,4,5])
		self.assertEqual(snippitz.list(3), [2])
		self.assertEqual(snippitz.list(4), [2])
		self.assertEqual(snippitz.list(5), [2])
		snippitz.close()
		
	def test_sever_and_list(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.tie_data(2,3)
		self.assertEqual(snippitz.list(2), [3])
		self.assertEqual(snippitz.list(3), [2])
		snippitz.sever_data(2,3)
		self.assertEqual(snippitz.list(2), [1])
		self.assertEqual(snippitz.list(3), [1])
		snippitz.close()
	
	def test_duplicate_tie(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.tie_data(2,3)
		snippitz.tie_data(2,3)
		self.assertEqual(snippitz.list(2), [3])
		self.assertEqual(snippitz.list(3), [2])
		snippitz.close()
	
	def test_duplicate_tie_reversed(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.tie_data(2,3)
		snippitz.tie_data(3,2)
		self.assertEqual(snippitz.list(2), [3])
		self.assertEqual(snippitz.list(3), [2])
		snippitz.close()
	
	def test_sever_nonexistant_connection(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.sever_data(2,3)
		self.assertRaises(FileNotFoundError, snippitz.list, 2)
		self.assertRaises(FileNotFoundError, snippitz.list, 3)
		snippitz.close()
	
	def test_create_circular_relationship_and_sever_one_connection(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.register("path/file3")
		snippitz.register("path/file4")
		snippitz.tie_data(2,3)
		snippitz.tie_data(3,4)
		snippitz.tie_data(4,5)
		snippitz.tie_data(5,2)
		self.assertEqual(snippitz.list(2), [3,5])
		self.assertEqual(snippitz.list(3), [2,4])
		self.assertEqual(snippitz.list(4), [3,5])
		self.assertEqual(snippitz.list(5), [4,2])
		snippitz.sever_data(5,2)
		self.assertEqual(snippitz.list(2), [3])
		self.assertEqual(snippitz.list(3), [2,4])
		self.assertEqual(snippitz.list(4), [3,5])
		self.assertEqual(snippitz.list(5), [4])
		snippitz.close()
	
	def test_merge_files_with_unique_connections(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.register("path/file3")
		snippitz.register("path/file4")
		snippitz.register("path/file5")
		snippitz.register("path/file6")
		snippitz.tie_data(2,3)
		snippitz.tie_data(2,4)
		snippitz.tie_data(5,6)
		snippitz.tie_data(5,7)
		self.assertEqual(snippitz.list(2), [3,4])
		self.assertEqual(snippitz.list(5), [6,7])
		snippitz.merge(2,5)
		self.assertEqual(snippitz.list(2), [3,4,6,7])
		self.assertEqual(snippitz.list(5), [6,7,3,4])
		snippitz.close()
	
	def test_merge_files_with_shared_connections(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.register("path/file3")
		snippitz.register("path/file4")
		snippitz.register("path/file5")
		snippitz.tie_data(2,3)
		snippitz.tie_data(2,4)
		snippitz.tie_data(5,4)
		snippitz.tie_data(5,6)
		self.assertEqual(snippitz.list(2), [3,4])
		self.assertEqual(snippitz.list(5), [4,6])
		snippitz.merge(2,5)
		self.assertEqual(snippitz.list(2), [3,4,6])
		self.assertEqual(snippitz.list(5), [4,6,3])
		snippitz.close()
	
	def test_merge_file_with_itself(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.tie_data(2,3)
		self.assertEqual(snippitz.list(2),[3])
		snippitz.merge(2,2)
		self.assertEqual(snippitz.list(2),[3])
		snippitz.close()
	
	def test_merge_connected_files(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.register("path/file3")
		snippitz.register("path/file4")
		snippitz.tie_data(2,3)
		snippitz.tie_data(2,4)
		snippitz.tie_data(3,5)
		self.assertEqual(snippitz.list(2),[3,4])
		self.assertEqual(snippitz.list(3),[2,5])
		snippitz.merge(2,3)
		self.assertEqual(snippitz.list(2),[3,4,5])
		self.assertEqual(snippitz.list(3),[2,5,4])
		snippitz.close()
	
	def test_unregister_file(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		self.assertEqual(snippitz.list(1), [2])
		snippitz.unregister(2)
		self.assertRaises(FileNotFoundError, snippitz.list, 1)
		snippitz.close()
		
	
	def test_unregister_connected_file(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.register("path/file1")
		snippitz.register("path/file2")
		snippitz.register("path/file3")
		snippitz.tie_data(2,3)
		snippitz.tie_data(2,4)
		self.assertEqual(snippitz.list(2), [3,4])
		self.assertEqual(snippitz.list(3), [2])
		self.assertEqual(snippitz.list(4), [2])
		snippitz.unregister(3)
		self.assertEqual(snippitz.list(2), [4])
		self.assertRaises(FileNotFoundError, snippitz.list, 3)
		self.assertEqual(snippitz.list(4), [2])
		snippitz.close()
		
		