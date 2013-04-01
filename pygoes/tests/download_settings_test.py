import unittest

from pygoes.configuration import FileDownloadSettings

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

