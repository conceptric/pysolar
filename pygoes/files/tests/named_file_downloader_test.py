import unittest

from remote_test_config import *
from pygoes.configuration import FileDownloadSettings
from pygoes.files.downloader import DownloadManager
from pygoes.files.cache import CacheManager
from pygoes.files.repository import RemoteManager

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
        self.filename = "Gp_xr_5m.txt"
        self.file_path = os.path.join(FIXTURES, self.filename)
        self.assertFalse(os.path.exists(self.file_path))

    def test_downloading_a_named_file(self):
        cache_manager = CacheManager(MockRemoteConfig())
        remote_manager = RemoteManager(MockRemoteConfig())
        downloader = DownloadManager(remote_manager, cache_manager)
        downloader.download(self.filename)
        os.remove(self.file_path)        


class TestMissingRemoteFile(unittest.TestCase):
    """
    Tests what happens when the remote file is missing.
    """    
    def test_raises_error_with_useful_message(self):
        missing = "missing.txt"
        expected_msg = missing + " is missing in the remote location."
        try:
            DownloadManager(
                RemoteManager(MockRemoteConfig()), 
                CacheManager(MockRemoteConfig())).download("missing.txt")
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
        DownloadManager(
            RemoteManager(MockRemoteConfig()), 
            CacheManager(MockRemoteConfig())).download(existing)
        time2 = os.path.getmtime(cached)
        self.assertEqual(time1, time2)



if __name__ == '__main__':
    unittest.main()