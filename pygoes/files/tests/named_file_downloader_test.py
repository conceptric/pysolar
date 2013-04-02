import unittest

from remote_test_config import *
from pygoes.files.downloader import DownloadManager

class MockRemoteConfig:
    def __init__(self):
        self.source = REMOTE
        self.cache = FIXTURES
        self.file_template = "%s_Gp_xr_5m.txt"
        
class TestDownloadManager(unittest.TestCase):
    """
    Tests the happy path of downloading a file successfully.
    """    
    def setUp(self):
        self.files = ("Gp_xr_1m.txt", "Gp_xr_5m.txt")
        self.config = MockRemoteConfig()
        self.downloader = DownloadManager(self.config)
        for file in self.files:
            path = os.path.join(self.config.cache, file)
            self.assertFalse(os.path.exists(path))

    def test_downloading_a_single_named_file(self):
        file = self.files[0]
        self.downloader.download(file)
        os.remove(os.path.join(self.config.cache, file))
        
    def test_downloading_two_named_files(self):
        self.downloader.files_by_name(self.files)
        for file in self.files:
            path = os.path.join(self.config.cache, file)
            os.remove(path)        
        
        
class TestWhenRemoteFileIsMissing(unittest.TestCase):
    """
    Tests what happens when the remote file is missing.
    """    
    def test_raises_error_with_useful_message(self):
        missing = "missing.txt"
        expected_msg = missing + " is missing in the remote location."
        try:
            DownloadManager(MockRemoteConfig()).download("missing.txt")
            self.assertFail()
        except Exception as ex:
            self.assertEquals(ex.message, expected_msg)


class TestFileAlreadyCached(unittest.TestCase):
    """
    Tests what happens when the remote file has already been cached.
    """    
    def test_does_nothing_if_cached_copy_exists(self):
        existing = "existing_file.txt"
        cached = MockRemoteConfig().cache + "/" + existing
        time1 = os.path.getmtime(cached)
        DownloadManager(MockRemoteConfig()).download(existing)
        time2 = os.path.getmtime(cached)
        self.assertEqual(time1, time2)



if __name__ == '__main__':
    unittest.main()