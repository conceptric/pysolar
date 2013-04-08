import unittest
from mock import *

from remote_test_config import *
from pygoes.files.repository import FileManager


class TestFileManager(unittest.TestCase):
    """
    Tests the construction of an instance of the class.
    """    
    def test_raises_exception_without_config(self):
        with self.assertRaises(TypeError):
            FileManager()

    def test_requires_configuration_argument(self):
        self.assertTrue(FileManager(get_mock_config()))


class TestMultipleFileDownloadQueries(unittest.TestCase):
    """
    Tests the class can construct download processes for 
    multiple remote files.
    """    
    def setUp(self):
        self.fmanager = FileManager(get_mock_config())
        self.fmanager.cache.download = MagicMock()
        self.mocked_method = self.fmanager.cache.download
        
    def test_download_call_is_successfully_mocked(self):
        ''' Sanity check for Mock '''
        self.assertTrue(self.fmanager.cache)
        self.assertIsInstance(self.mocked_method, MagicMock)

    def test_downloading_two_named_files(self):
        """
        Tests downloads multiple files based on file names strings.
        """    
        files = ("Gp_xr_1m.txt", "Gp_xr_5m.txt")
        expected = [call(files[0], self.fmanager.remote), 
            call(files[1], self.fmanager.remote)]
        self.fmanager.download(files)
        self.assertEqual(expected, self.mocked_method.call_args_list)

    def test_downloading_a_single_file_with_template(self):        
        """
        Tests downloads a single file based on a template 
        generated name.
        """    
        self.fmanager.download_by_template('1')
        self.mocked_method.assert_called_once_with('Gp_xr_1m.txt', 
            self.fmanager.remote)

    def test_downloading_two_files_with_template(self):
        """
        Tests downloads multiple files based on template 
        generated names.
        """    
        strings = ('1', '2')
        expected = [call('Gp_xr_1m.txt', self.fmanager.remote), 
            call('Gp_xr_2m.txt', self.fmanager.remote)]
        self.fmanager.download_by_template(strings)
        self.assertEqual(expected, self.mocked_method.call_args_list)


class TestApplyingFilenameTemplate(unittest.TestCase):
    """
    Tests the class can construct filenames using the 
    template in the configuration.
    """    
    def test_generating_two_filenames_from_template(self):
        """
        Uses the configuration template to generate filename 
        strings for the list of supplied strings.
        """    
        strings = ('1', '2')
        expected = ['Gp_xr_1m.txt', 'Gp_xr_2m.txt']
        fmanager = FileManager(get_mock_config())
        actual = fmanager.filenames_from_template(strings)
        self.assertEquals(expected, actual)

        
if __name__ == '__main__':
    unittest.main()