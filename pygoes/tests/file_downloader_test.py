import unittest
import os

from pygoes.remote.file_downloader import FileDownloader

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')

class TestFileDownloader(unittest.TestCase):
    """
    Tests the class that downloads requested GOES data files
    """
    def setUp(self):
        filename = "Gp_xr_5m.txt"
        source_path = "http://www.swpc.noaa.gov/ftpdir/lists/xray/"
        self.source = source_path + filename
        self.destination = os.path.join(FIXTURES, filename)        
        self.downloader = FileDownloader(self.source, self.destination)

    def test_that_the_downloader_knows_the_source(self):
        self.assertEquals(self.downloader.source, self.source)

    def test_that_the_downloader_knows_the_complete_destination(self):
        self.assertEquals(self.downloader.destination, self.destination)
        
    def test_check_remote_file_exists(self):
        self.assertTrue(self.downloader.remote_exists())