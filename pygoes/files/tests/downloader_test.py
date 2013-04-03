import unittest
from mock import *

from remote_test_config import *
from pygoes.files.downloader import Downloader
from pygoes.files.repository import RemoteManager
from pygoes.files.cache import CacheManager

class TestSingleFileDownload(unittest.TestCase):
    '''
    Test the Downloader ability to handle downloads of a 
    named file from a remote location.
    '''
    def setUp(self):
        self.remote = MagicMock()
        self.remote.read.return_value = "example content"
        cache = CacheManager(MockRemoteConfig())
        self.dl = Downloader(remote=self.remote,
                             cache=cache)

    def test_calls_are_successfully_mocked(self):
        ''' Sanity check for Mock '''
        self.assertIsInstance(self.dl.remote, MagicMock)
        
    def test_downloading_a_single_named_file(self):
        '''
        The Downloader successfully downloads a 
        named file if its available in the remote location.
        '''
        filename = "new_file.txt"
        self.dl.download(filename)
        self.dl.remote.read.assert_called_once_with(filename)
        os.remove(get_cached_path(filename))

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
        filename = "existing_file.txt"
        time_before = get_cached_mtime(filename)
        self.dl.download(filename)
        time_after = get_cached_mtime(filename)
        self.assertEqual(time_before, time_after)


if __name__ == '__main__':
    unittest.main()