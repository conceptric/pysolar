import unittest

from config import *
from pygoes.configuration import FileDownloadSettings
from pygoes.remote.file_downloader import NamedFileDownloader
        
class TestNamedFileDownloader(unittest.TestCase):
    """
    Tests the happy path of downloading a file successfully.
    """    
    def setUp(self):
        self.filename = "Gp_xr_5m.txt"
        url = "http://www.swpc.noaa.gov/ftpdir/lists/xray/"
        valid_settings = FileDownloadSettings(url, FIXTURES)
        self.downloader = NamedFileDownloader(valid_settings)

    def tearDown(self):
        file_path = os.path.join(FIXTURES, self.filename)
        if os.path.exists(file_path):
            os.remove(file_path)        

    def test_no_local_copy_of_named_file(self):
        self.assertFalse(self.downloader.already_cached(self.filename))
        
    def test_downloading_a_named_file(self):
        self.downloader.download("Gp_xr_5m.txt")
        self.assertTrue(self.downloader.already_cached(self.filename))

    def test_raises_error_if_remote_does_not_exist(self):
        missing = "missing.txt"
        expected_msg = missing + " is missing in the remote location."
        try:
            self.downloader.download("missing.txt")
            self.assertFail()
        except Exception as ex:
            self.assertEquals(ex.message, expected_msg)
        finally:
            self.assertFalse(self.downloader.already_cached(missing))


if __name__ == '__main__':
    unittest.main()