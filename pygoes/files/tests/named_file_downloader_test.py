import unittest

from remote_test_config import *
from pygoes.configuration import FileDownloadSettings
from pygoes.files.downloader import NamedFileDownloader
from pygoes.files.cache import CacheManager
from pygoes.files.repository import RemoteManager

VALID_SETTINGS = FileDownloadSettings(REMOTE, FIXTURES)
        
class TestNamedFileDownloader(unittest.TestCase):
    """
    Tests the happy path of downloading a file successfully.
    """    
    def setUp(self):
        self.filename = "Gp_xr_5m.txt"

    def tearDown(self):
        file_path = os.path.join(FIXTURES, self.filename)
        if os.path.exists(file_path):
            os.remove(file_path)        

    def test_downloading_a_named_file(self):
        cache_manager = CacheManager(VALID_SETTINGS)
        remote_manager = RemoteManager(VALID_SETTINGS)
        downloader = NamedFileDownloader(remote_manager, cache_manager)
        self.assertFalse(cache_manager.file_exists(self.filename))
        downloader.download(self.filename)
        self.assertTrue(cache_manager.file_exists(self.filename))


class TestMissingRemoteFile(unittest.TestCase):
    """
    Tests what happens when the remote file is missing.
    """    
    def test_raises_error_with_useful_message(self):
        missing = "missing.txt"
        expected_msg = missing + " is missing in the remote location."
        try:
            NamedFileDownloader(
                RemoteManager(VALID_SETTINGS), 
                CacheManager(VALID_SETTINGS)).download("missing.txt")
            self.assertFail()
        except Exception as ex:
            self.assertEquals(ex.message, expected_msg)


class TestFileAlreadyCached(unittest.TestCase):
    """
    Tests what happens when the remote file has already been cached.
    """    
    def test_does_nothing_if_cached_copy_exists(self):
        existing = "existing_file.txt"
        cached = VALID_SETTINGS.cache + "/" + existing
        time1 = os.path.getmtime(cached)
        NamedFileDownloader(
            RemoteManager(VALID_SETTINGS), 
            CacheManager(VALID_SETTINGS)).download(existing)
        time2 = os.path.getmtime(cached)
        self.assertEqual(time1, time2)



if __name__ == '__main__':
    unittest.main()