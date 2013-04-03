import unittest

from remote_test_config import *
from pygoes.files.downloader import DownloadManager

class TestDownloadManager(unittest.TestCase):
    """
    Tests the class that handles download tasks that 
    are more complex than a single named file.
    """    
    def setUp(self):
        self.files = ("Gp_xr_1m.txt", "Gp_xr_5m.txt")
        self.config = MockRemoteConfig()
        self.dmanager = DownloadManager(self.config)
        for file in self.files:
            path = os.path.join(self.config.cache, file)
            self.assertFalse(os.path.exists(path))

    def test_downloading_two_named_files(self):
        self.dmanager.files_by_name(self.files)
        for file in self.files:
            path = os.path.join(self.config.cache, file)
            os.remove(path)        

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