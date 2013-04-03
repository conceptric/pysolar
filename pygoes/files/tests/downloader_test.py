import unittest
from mock import *

from remote_test_config import *
from pygoes.files.downloader import Downloader

class TestSingleFileDownload(unittest.TestCase):
    '''
    Test the Downloader ability to handle downloads of a 
    named file from a remote location.
    '''
    def setUp(self):
        self.config = MockRemoteConfig()
        self.dl = Downloader(self.config)
        self.dl.remote.read = MagicMock()
        self.dl.cache.write_file = MagicMock()

    def test_calls_are_successfully_mocked(self):
        ''' Sanity check for Mock '''
        self.assertIsInstance(self.dl.remote.read, MagicMock)
        self.assertIsInstance(self.dl.cache.write_file, MagicMock)

    def test_downloading_a_single_named_file(self):
        '''
        The Downloader successfully downloads a 
        named file if its available in the remote location.
        '''
        filename = "new_file.txt"
        contents = "file contents"
        self.dl.remote.read.return_value = contents
        self.dl.download(filename)
        self.dl.remote.read.assert_called_once_with(filename)
        self.dl.cache.write_file.assert_called_once_with(filename, contents)

    def test_no_attempt_to_read_if_file_cached(self):
        """
        The Downloader does not read the remote source if  
        the named file has already been cached.
        """    
        self.dl.download("existing_file.txt")
        self.assertEqual(len(self.dl.remote.read.call_args_list), 0)
        
    def test_no_attempt_to_write_if_file_cached(self):
        """
        The Downloader does not write to the local cache if  
        the named file that has already been cached.
        """    
        self.dl.download("existing_file.txt")
        self.assertEqual(
            len(self.dl.cache.write_file.call_args_list), 0)


if __name__ == '__main__':
    unittest.main()