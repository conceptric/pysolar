import unittest
import os

from pygoes.remote.file_downloader import *

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')

class TestFileDownloadSettings(unittest.TestCase):
    """
    Tests a class to contain the download details and settings
    """
    def setUp(self):
        self.url = "http://example.com/"
        self.cache = "/home/user/"        
        self.settings = FileDownloadSettings(self.url, self.cache)

    def test_that_the_settings_contain_the_source(self):
        self.assertEquals(self.settings.source, self.url)

    def test_that_the_settings_contain_the_complete_destination(self):
        self.assertEquals(self.settings.cache, self.cache)
        
    def test_without_arguments(self):
        pass

    def test_invalid_source_path(self):
        pass
        
    def test_invalid_destination_path(self):
        pass

        
class TestNamedFileDownloader(unittest.TestCase):
    """
    Tests the happy path of downloading a file successfully.
    """    
    def setUp(self):
        self.filename = "Gp_xr_5m.txt"
        url = "http://www.swpc.noaa.gov/ftpdir/lists/xray/"
        valid_settings = FileDownloadSettings(url, FIXTURES)
        self.downloader = FileDownloader(valid_settings)

    def tearDown(self):
        file_path = os.path.join(FIXTURES, self.filename)
        if os.path.exists(file_path):
            os.remove(file_path)        

    def test_no_local_copy_of_named_file(self):
        self.assertFalse(self.downloader.local_exists(self.filename))
        
    def test_downloading_a_named_file(self):
        self.downloader.download("Gp_xr_5m.txt")
        self.assertTrue(self.downloader.local_exists(self.filename))

    def test_raises_error_if_remote_does_not_exist(self):
        missing = "missing.txt"
        expected_msg = missing + " is missing in the remote location."
        try:
            self.downloader.download("missing.txt")
            self.assertFail()
        except Exception as ex:
            self.assertEquals(ex.message, expected_msg)
        finally:
            self.assertFalse(self.downloader.local_exists(missing))
        