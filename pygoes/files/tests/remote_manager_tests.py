import unittest

from remote_test_config import *
from pygoes.files.repository import RemoteManager
from urllib2 import URLError

class FakeConfig:
    def __init__(self, url=REMOTE):
        self.source = url

class TestRemoteManager(unittest.TestCase):
    """
    Test the class that is responsible for managing the remote
    data files via http.
    """
    def test_takes_a_configuration_object(self):
        self.assertTrue(RemoteManager(FakeConfig()))

    def test_requires_a_source_path_in_settings(self):
        with self.assertRaises(TypeError):
            RemoteManager()


class TestReadingRemoteFiles(unittest.TestCase):
    """
    Test the RemoteManager can handle reading remote files.
    """
    def setUp(self):
        self.remote = RemoteManager(FakeConfig())

    def test_raises_error_with_local_path_for_url(self):
        with self.assertRaises(ValueError):
            local = RemoteManager(FakeConfig(FIXTURES))
            local.read("Gp_xr_5m.txt")

    def tests_raises_error_when_url_is_not_known(self):
        with self.assertRaises(URLError):
            local = RemoteManager(FakeConfig('http://'))
            local.read("Gp_xr_5m.txt")
    
    def test_read_existing_remote_file(self):
        '''
        The named file is successfully loaded into memory.
        '''
        first_line = self.remote.read("Gp_xr_5m.txt").split('\n')[0]        
        self.assertEqual(first_line, ":Data_list: Gp_xr_5m.txt")
                
    def test_reading_missing_file_raises_helpful_error(self):
        '''
        The Manager raises a helpful message when trying 
        to read a named file that is unavailable in the 
        remote location.
        '''
        filename = "missing.txt"
        message = "%s is missing in the remote location." % filename
        try:
            self.remote.read(filename)
            self.assertFail()
        except Exception as ex:
            self.assertEquals(ex.message, message)        
