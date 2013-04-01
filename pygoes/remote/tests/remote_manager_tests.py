import unittest
from pygoes.utils.errors import MissingFileError

from remote_test_config import *
from pygoes.remote.repository import RemoteManager

class FakeSettings:
    def __init__(self, url=REMOTE):
        self.source = url

class TestRemoteManager(unittest.TestCase):
    """
    Test the class that is responsible for managing the remote
    data files via http.
    """
    def setUp(self):
        self.remote = RemoteManager(FakeSettings())
        
    def test_requires_a_source_path_in_settings(self):
        self.assertTrue(self.remote)

    def test_raises_error_with_local_path_for_url(self):
        with self.assertRaises(ValueError):
            RemoteManager(FakeSettings(FIXTURES))
    
    def test_read_existing_remote_file(self):
        first_line = self.remote.read("Gp_xr_5m.txt").split('\n')[0]        
        self.assertEqual(first_line, ":Data_list: Gp_xr_5m.txt")
                
    def test_reading_missing_file_raises_helpful_error(self):
        filename = "missing.txt"
        message = "%s is missing in the remote location." % filename
        try:
            self.remote.read(filename)
            self.assertFail()
        except MissingFileError as ex:
            self.assertEquals(ex.message, message)        
