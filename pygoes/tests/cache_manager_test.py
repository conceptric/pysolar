import unittest
from config import *
from pygoes.remote.cache import CacheManager

class FakeSettings:
    cache = FIXTURES

class TestCacheManager(unittest.TestCase):
    """
    Test the class that is responsible for managing the local cache
    of data files
    """
    def setUp(self):
        self.cache = CacheManager(FakeSettings())
        
    def test_requires_a_cache_path_in_settings(self):
        self.assertTrue(self.cache)
    
    def test_knows_if_a_file_is_already_cached(self):
        self.assertTrue(self.cache.file_exists("existing_file.txt"))
        
    def test_knows_if_a_file_is_not_cached(self):
        self.assertFalse(self.cache.file_exists("missing.txt"))

class TestWriteFile(unittest.TestCase):
    """
    Test creating and writing to cached text files
    """
    def setUp(self):
        self.cache = CacheManager(FakeSettings())
        self.filename = "writing_test.txt"
        self.file_path = os.path.join(FIXTURES, self.filename)
        
    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            
    def test_writing_to_new_file(self):
        expected = "This is a test"
        self.cache.write_file(self.filename, expected)
        actual = open(self.file_path, 'r').read()
        self.assertTrue(self.cache.file_exists(self.filename))
        self.assertEquals(actual, expected)

    def test_existing_file_cannot_be_overwritten(self):
        expected = "Original"
        self.cache.write_file(self.filename, expected)
        self.cache.write_file(self.filename, "Overwritten")
        actual = open(self.file_path, 'r').read()
        self.assertTrue(self.cache.file_exists(self.filename))
        self.assertEquals(actual, expected)
        
    def test_raises_exception_with_invalid_path(self):
        with self.assertRaises(IOError):
            self.cache.write_file("wrong/path.txt", "Error")
