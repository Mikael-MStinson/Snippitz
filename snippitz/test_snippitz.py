from unittest import TestCase
from .snippitz import Snippitz

class TestSnippitz(TestCase):
	def test_tie_and_list(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		self.assertEqual(snippitz.list("file1"), ["file2"])
		snippitz.close()
	
	def test_tie_to_itself(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file1")
		snippitz.tie("file1","file2")
		self.assertEqual(snippitz.list("file1"), ["file2"])
		snippitz.close()
		
	def test_tie_to_multiple_files_and_list(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		snippitz.tie("file1","file3")
		snippitz.tie("file1","file4")
		self.assertEqual(snippitz.list("file1"), ["file2","file3","file4"])
		snippitz.close()
		
	def test_tie_and_list_from_relative_perspective(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		self.assertEqual(snippitz.list("file2"), ["file1"])
		snippitz.close()
		
	def test_tie_to_multiple_files_and_list_from_relative_perspective(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		snippitz.tie("file1","file3")
		snippitz.tie("file1","file4")
		self.assertEqual(snippitz.list("file2"), ["file1"])
		self.assertEqual(snippitz.list("file3"), ["file1"])
		self.assertEqual(snippitz.list("file4"), ["file1"])
		snippitz.close()
		
	def test_list_for_nonexistant_file(self):
		snippitz = Snippitz(database = ':memory:')
		self.assertRaises(FileNotFoundError, snippitz.list, "file")
		snippitz.close()
		
	def test_severe_and_list(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		snippitz.severe("file1","file2")
		self.assertRaises(FileNotFoundError, snippitz.list, "file1")
		self.assertRaises(FileNotFoundError, snippitz.list, "file2")
		snippitz.close()
		
	def test_duplicate_tie(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		snippitz.tie("file1","file2")
		self.assertEqual(snippitz.list("file1"), ["file2"])
		self.assertEqual(snippitz.list("file2"), ["file1"])
		snippitz.close()
		
	def test_duplicate_tie_reversed(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		snippitz.tie("file2","file1")
		self.assertEqual(snippitz.list("file1"), ["file2"])
		self.assertEqual(snippitz.list("file2"), ["file1"])
		snippitz.close()
		
	def test_severe_nonexistant_connection(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.severe("file1","file2")
		self.assertRaises(FileNotFoundError, snippitz.list, "file1")
		self.assertRaises(FileNotFoundError, snippitz.list, "file2")
		snippitz.close()
		
	def test_create_circular_relationship_and_severe_one_connection(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		snippitz.tie("file2","file3")
		snippitz.tie("file3","file4")
		snippitz.tie("file4","file1")
		self.assertEqual(snippitz.list("file1"), ["file2","file4"])
		self.assertEqual(snippitz.list("file2"), ["file1","file3"])
		self.assertEqual(snippitz.list("file3"), ["file2","file4"])
		self.assertEqual(snippitz.list("file4"), ["file3","file1"])
		snippitz.severe("file4","file1")
		self.assertEqual(snippitz.list("file1"), ["file2"])
		self.assertEqual(snippitz.list("file2"), ["file1","file3"])
		self.assertEqual(snippitz.list("file3"), ["file2","file4"])
		self.assertEqual(snippitz.list("file4"), ["file3"])
		snippitz.close()
		
	def test_merge_files_with_unique_connections(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		snippitz.tie("file1","file3")
		snippitz.tie("file4","file5")
		snippitz.tie("file4","file6")
		self.assertEqual(snippitz.list("file1"), ["file2","file3"])
		self.assertEqual(snippitz.list("file4"), ["file5","file6"])
		snippitz.merge("file1","file4")
		self.assertEqual(snippitz.list("file1"), ["file2","file3","file5","file6"])
		self.assertEqual(snippitz.list("file4"), ["file5","file6","file2","file3"])
		snippitz.close()
		
	def test_merge_files_with_shared_connections(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		snippitz.tie("file1","file3")
		snippitz.tie("file4","file3")
		snippitz.tie("file4","file5")
		self.assertEqual(snippitz.list("file1"), ["file2","file3"])
		self.assertEqual(snippitz.list("file4"), ["file3","file5"])
		snippitz.merge("file1","file4")
		self.assertEqual(snippitz.list("file1"), ["file2","file3","file5"])
		self.assertEqual(snippitz.list("file4"), ["file3","file5","file2"])
		snippitz.close()
		
	def test_merge_file_with_itself(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		self.assertEqual(snippitz.list("file1"),["file2"])
		snippitz.merge("file1","file1")
		self.assertEqual(snippitz.list("file1"),["file2"])
		
	def test_merge_connected_files(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		snippitz.tie("file1","file3")
		snippitz.tie("file2","file4")
		self.assertEqual(snippitz.list("file1"),["file2","file3"])
		self.assertEqual(snippitz.list("file2"),["file1","file4"])
		snippitz.merge("file1","file2")
		self.assertEqual(snippitz.list("file1"),["file2","file3","file4"])
		self.assertEqual(snippitz.list("file2"),["file1","file4","file3"])
		
	def test_delete_file(self):
		snippitz = Snippitz(database = ':memory:')
		snippitz.tie("file1","file2")
		snippitz.tie("file1","file3")
		self.assertEqual(snippitz.list("file1"), ["file2","file3"])
		self.assertEqual(snippitz.list("file2"), ["file1"])
		self.assertEqual(snippitz.list("file3"), ["file1"])
		snippitz.delete("file2")
		self.assertEqual(snippitz.list("file1"), ["file3"])
		self.assertRaises(FileNotFoundError, snippitz.list, "file2")
		self.assertEqual(snippitz.list("file3"), ["file1"])
		snippitz.close()
		
		