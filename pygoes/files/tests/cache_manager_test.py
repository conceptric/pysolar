import unittest
from mock import *

from remote_test_config import *
from pygoes.files.repository import CacheManager

class FakeConfig:
    def __init__(self, path=FIXTURES):
        self.cache = path


class TestCacheManager(unittest.TestCase):
    """
    Test the arguments for a CacheManager.
    """
    def test_requires_a_configuration_argument(self):
        self.assertTrue(CacheManager(FakeConfig()))
        
    def test_raises_error_without_configuration_argument(self):
        with self.assertRaises(TypeError):
            CacheManager()
    
    def test_raises_error_a_url_for_local_path(self):
        with self.assertRaises(ValueError):
            CacheManager(FakeConfig(REMOTE))


class TestFileManagement(unittest.TestCase):
    """
    Test what the CacheManager knows about the Files
    """    
    def setUp(self):
        self.cache = CacheManager(FakeConfig())

    def test_knows_if_a_file_is_already_cached(self):
        self.assertTrue(self.cache.file_exists("existing_file.txt"))
        
    def test_knows_if_a_file_is_not_cached(self):
        self.assertFalse(self.cache.file_exists("missing.txt"))


class TestWriteFile(unittest.TestCase):
    """
    Test creating and writing to cached text files
    """
    def setUp(self):
        self.cache = CacheManager(FakeConfig())
        self.filename = "writing_test.txt"
        self.content = "Original"
        self.cache.write_file(self.filename, self.content)
        
    def tearDown(self):
        os.remove(get_cached_path(self.filename))
    
    def actual(self):
        return open(get_cached_path(self.filename), 'r').read()
            
    def test_writing_to_new_file(self):
        self.assertTrue(cached_file_exists(self.filename))
        self.assertEquals(self.actual(), self.content)

    def test_existing_file_cannot_be_overwritten(self):
        self.cache.write_file(self.filename, "Overwritten")
        self.assertTrue(cached_file_exists(self.filename))
        self.assertEquals(self.actual(), self.content)
        
    def test_raises_exception_with_invalid_path(self):
        with self.assertRaises(IOError):
            self.cache.write_file("wrong/path.txt", "Error")


class TestReadFile(unittest.TestCase):
    """
    Test reading the contents of a cached text file
    """
    def setUp(self):
        self.cache = CacheManager(FakeConfig())
        
    def test_reading_an_existing_named_file(self):
        expected = "This is an existing test fixture."
        actual = self.cache.read("existing_file.txt")
        self.assertEquals(actual, expected)

    def test_raises_exception_with_missing_file(self):
        with self.assertRaises(IOError):
            self.cache.read("missing.txt")

class TestSingleFileDownload(unittest.TestCase):
    '''
    Test the ability to manage the download of a named file 
    from a remote location to the local cache.
    '''
    def setUp(self):
        self.remote = MagicMock()
        self.remote.read.return_value = "example content"
        self.cache = CacheManager(get_mock_config())

    def test_calls_are_successfully_mocked(self):
        ''' Sanity check for Mock '''
        self.assertIsInstance(self.remote, MagicMock)
        
    def test_downloading_a_single_named_file(self):
        '''
        Successfully downloads a named file.
        '''
        filename = "new_file.txt"
        self.cache.download(filename, self.remote)
        self.remote.read.assert_called_once_with(filename)
        os.remove(get_cached_path(filename))

    def test_no_attempt_to_read_if_file_cached(self):
        """
        Does not read the remote source if the named file 
        has already been cached.
        """    
        self.cache.download("existing_file.txt", self.remote)
        self.assertEqual(len(self.remote.read.call_args_list), 0)
        
    def test_no_attempt_to_write_if_file_cached(self):
        """
        Does not write to the local file if  
        the named file that has already been cached.
        """    
        filename = "existing_file.txt"
        time_before = get_cached_mtime(filename)
        self.cache.download(filename, self.remote)
        time_after = get_cached_mtime(filename)
        self.assertEqual(time_before, time_after)


if __name__ == '__main__':
    unittest.main()