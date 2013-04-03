import unittest

from remote_test_config import *
from pygoes.files.downloader import DownloadManager
from pygoes.files.downloader import Downloader

class TestDownloadManager(unittest.TestCase):
    """
    Tests the class that handles download tasks that 
    are more complex than a single named file.
    """    
    def setUp(self):
        self.files = ("Gp_xr_1m.txt", "Gp_xr_5m.txt")
        self.config = MockRemoteConfig()
        self.dmanager = DownloadManager(Downloader(self.config), self.config)
        for afile in self.files:
            path = os.path.join(self.config.cache, afile)
            self.assertFalse(cached_file_exists(afile))

    def test_downloading_two_named_files(self):
        self.dmanager.files_by_name(self.files)
        for afile in self.files:
            os.remove(get_cached_path(afile))        

    def test_downloading_a_single_file_with_template(self):        
        self.dmanager.files_by_template('1')
        os.remove(os.path.join(self.config.cache, self.files[0]))

    def test_generating_filenames_from_template(self):
        """
        Uses the configuration template to generate filename 
        strings for the list of supplied strings.
        """    
        strings = ('20100101', '20100102')
        expected = ['Gp_xr_20100101m.txt', 'Gp_xr_20100102m.txt']
        actual = self.dmanager.filenames_from_template(strings)
        self.assertEquals(expected, actual)
        

if __name__ == '__main__':
    unittest.main()