import unittest
import os

from pygoes.remote.file_downloader import FileDownloader
from pygoes.remote.file_downloader import FileDownloadSettings

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')

class TestFileDownloadSettings(unittest.TestCase):
    """
    Tests a class to contain the download details and settings
    """
    def setUp(self):
        self.url = "http://example.com/filename.txt"
        self.local_path = "/home/user/filename.txt"        
        self.settings = FileDownloadSettings(self.url, self.local_path)

    def test_that_the_settings_contain_the_source(self):
        self.assertEquals(self.settings.source, self.url)

    def test_that_the_settings_contain_the_complete_destination(self):
        self.assertEquals(self.settings.destination, self.local_path)
        
    def test_without_arguments(self):
        pass

    def test_invalid_source_path(self):
        pass
        
    def test_invalid_destination_path(self):
        pass

        
class TestDownloadingRemoteFile(unittest.TestCase):
    """
    Tests the happy path of downloading a file successfully.
    """    
    def setUp(self):
        url = "http://www.swpc.noaa.gov/ftpdir/lists/xray/Gp_xr_5m.txt"
        self.local_path = os.path.join(FIXTURES, "Gp_xr_5m.txt")
        valid_settings = FileDownloadSettings(url, self.local_path)
        self.downloader = FileDownloader(valid_settings)

    def tearDown(self):
        if os.path.exists(self.local_path):
            os.remove(self.local_path)        

    def test_there_is_no_existing_local_file(self):
        self.assertFalse(self.downloader.local_exists())
        
    def test_that_the_file__was_downloaded(self):
        self.downloader.download()
        self.assertTrue(self.downloader.local_exists())
        
