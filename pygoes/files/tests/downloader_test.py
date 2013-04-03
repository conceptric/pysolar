import unittest

from remote_test_config import *
from pygoes.files.downloader import Downloader

class TestSingleFileDownload(unittest.TestCase):
    '''
    Test the Downloader ability to handle downloads of a 
    named file from a remote location.
    '''
    def setUp(self):
        self.config = MockRemoteConfig()
        self.downloader = Downloader(self.config)

    def get_cached_path(self, filename):
        return os.path.join(self.config.cache, filename)
        
    def get_cached_mtime(self, filename):
        return os.path.getmtime(self.get_cached_path(filename))
        
    def test_downloading_a_single_named_file(self):
        '''
        The Downloader successfully downloads a 
        named file if its available in the remote location.
        '''
        filename = "Gp_xr_5m.txt"
        path = self.get_cached_path(filename)
        self.assertFalse(os.path.exists(path))
        self.downloader.download(filename)
        os.remove(path)
        
    def test_raises_error_with_useful_message(self):
        '''
        The Downloader raises a helpful message when trying 
        to download a named file that is unavailable in the 
        remote location.
        '''
        filename = "missing.txt"
        message = "%s is missing in the remote location." % (filename)
        try:
            self.downloader.download(filename)
            self.assertFail()
        except Exception as ex:
            self.assertEquals(ex.message, message)
            
    def test_does_nothing_if_cached_copy_exists(self):
        """
        The Downloader does nothing when trying to download 
        a named file that has already been cached.
        """    
        filename = "existing_file.txt"
        time1 = self.get_cached_mtime(filename)
        self.downloader.download(filename)
        time2 = self.get_cached_mtime(filename)
        self.assertEqual(time1, time2)

if __name__ == '__main__':
    unittest.main()